#!/usr/bin/env bash
set -u

BASE_URL="http://localhost:3000"
RESULTS_FILE="Testing_Results"
COOKIE_FILE="./cookies.txt"
TMP_BODY="$(mktemp)"
TEST_EMAIL="john+$(date +%s)@example.com"
TEST_PASSWORD="secure123"
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
FAILED_TEST_NAMES=""

# Reset outputs from prior runs.
: > "$RESULTS_FILE"
rm -f "$COOKIE_FILE"

write_block() {
  local text="$1"
  printf "%s\n" "$text" >> "$RESULTS_FILE"
}

json_get() {
  local json_text="$1"
  local path="$2"

  python3 - "$path" "$json_text" <<'PY'
import json
import sys

path = sys.argv[1]
raw = sys.argv[2].strip()
if not raw:
    sys.exit(1)

try:
    obj = json.loads(raw)
except Exception:
    sys.exit(1)

cur = obj
for key in path.split('.'):
    if isinstance(cur, dict) and key in cur:
        cur = cur[key]
    else:
        sys.exit(1)

if isinstance(cur, (dict, list)):
    print(json.dumps(cur))
else:
    print(cur)
PY
}

run_request() {
  local label="$1"
  local method="$2"
  local url="$3"
  local data="$4"
  local use_cookie="$5"
  local save_cookie="$6"
  local expected_statuses="${7:-200}"

  local -a curl_args
  curl_args=(-sS -X "$method" "$url" -o "$TMP_BODY" -w "%{http_code}" -H "Content-Type: application/json")

  if [[ "$use_cookie" == "yes" ]]; then
    curl_args+=(-b "$COOKIE_FILE")
  fi

  if [[ "$save_cookie" == "yes" ]]; then
    curl_args+=(-c "$COOKIE_FILE")
  fi

  if [[ -n "$data" ]]; then
    curl_args+=(-d "$data")
  fi

  local http_status=""
  local curl_exit=0
  http_status="$(curl "${curl_args[@]}" 2>>"$RESULTS_FILE")"
  curl_exit=$?

  local body
  body="$(cat "$TMP_BODY")"

  write_block "============================================================"
  write_block "TEST: $label"
  write_block "REQUEST: $method $url"
  write_block "CURL_EXIT: $curl_exit"
  write_block "HTTP_STATUS: $http_status"
  write_block "RESPONSE_BODY:"
  write_block "$body"

  local test_passed="false"
  if [[ "$curl_exit" -eq 0 && ",${expected_statuses}," == *",${http_status},"* ]]; then
    test_passed="true"
    PASSED_TESTS=$((PASSED_TESTS + 1))
  else
    FAILED_TESTS=$((FAILED_TESTS + 1))
    FAILED_TEST_NAMES+="- ${label} (expected: ${expected_statuses}, got: ${http_status}, curl_exit: ${curl_exit})\n"
  fi
  TOTAL_TESTS=$((TOTAL_TESTS + 1))

  write_block "EXPECTED_HTTP_STATUS: $expected_statuses"
  write_block "TEST_RESULT: $test_passed"
  write_block ""

  printf "%s" "$body"
}

write_block "Aquatic Pandas API Test Run"
write_block "Started: $(date)"
write_block "BASE_URL: $BASE_URL"
write_block "Generated test email: $TEST_EMAIL"
write_block ""

# Ensure an institution exists for account creation.
write_block "[Setup] Ensuring prerequisite institution exists..."
institution_id="$(docker compose exec -T db mysql -N -u pandas_user -ppandas_password aquatic_pandas -e "SELECT institution_id FROM Institution WHERE institution_name='Chase' LIMIT 1;" 2>>"$RESULTS_FILE")"

if [[ -z "$institution_id" ]]; then
  docker compose exec -T db mysql -u pandas_user -ppandas_password aquatic_pandas -e "INSERT INTO Institution (institution_name, website) VALUES ('Chase', 'https://www.chase.com');" >>"$RESULTS_FILE" 2>&1
  institution_id="$(docker compose exec -T db mysql -N -u pandas_user -ppandas_password aquatic_pandas -e "SELECT institution_id FROM Institution WHERE institution_name='Chase' LIMIT 1;" 2>>"$RESULTS_FILE")"
fi

if [[ -z "$institution_id" ]]; then
  write_block "ERROR: Could not resolve institution_id."
  write_block "Ended: $(date)"
  rm -f "$TMP_BODY"
  exit 1
fi

write_block "Resolved institution_id: $institution_id"
write_block ""

register_body="$(run_request "Register User" "POST" "$BASE_URL/auth/register" "{\"first_name\":\"John\",\"last_name\":\"Doe\",\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\",\"phone\":\"\",\"address\":\"\"}" "no" "no" "201")"

login_body="$(run_request "Login User" "POST" "$BASE_URL/auth/login" "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}" "no" "yes" "200")"

user_id="$(json_get "$register_body" "user_id" 2>/dev/null || true)"
if [[ -z "$user_id" ]]; then
  user_id="$(json_get "$login_body" "user_id" 2>/dev/null || true)"
fi
if [[ -z "$user_id" ]]; then
  user_id="$(json_get "$login_body" "user.user_id" 2>/dev/null || true)"
fi

if [[ -z "$user_id" ]]; then
  write_block "ERROR: Could not resolve user_id from register/login responses."
  write_block "Ended: $(date)"
  rm -f "$TMP_BODY"
  exit 1
fi

write_block "Resolved user_id: $user_id"
write_block ""

run_request "Current User" "GET" "$BASE_URL/auth/current-user" "" "yes" "no" "200" >/dev/null
run_request "Logout" "POST" "$BASE_URL/auth/logout" "" "yes" "no" "200" >/dev/null
run_request "Current User After Logout (Expected Unauthorized)" "GET" "$BASE_URL/auth/current-user" "" "yes" "no" "401" >/dev/null
run_request "Login Again" "POST" "$BASE_URL/auth/login" "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}" "no" "yes" "200" >/dev/null

run_request "Get User" "GET" "$BASE_URL/api/users/$user_id" "" "yes" "no" "200" >/dev/null
run_request "Update User" "PUT" "$BASE_URL/api/users/$user_id" "{\"first_name\":\"Johnny\",\"last_name\":\"Doe\",\"phone\":\"555-123-4567\",\"address\":\"123 Test St\"}" "yes" "no" "200" >/dev/null

create_account_body="$(run_request "Create Account" "POST" "$BASE_URL/api/users/$user_id/accounts" "{\"account_name\":\"Main Checking\",\"account_type\":\"Checking\",\"institution_id\":$institution_id}" "yes" "no" "201")"
account_id="$(json_get "$create_account_body" "account.account_id" 2>/dev/null || true)"

if [[ -z "$account_id" ]]; then
  write_block "ERROR: Could not resolve account_id from create account response."
  write_block "Ended: $(date)"
  rm -f "$TMP_BODY"
  exit 1
fi

write_block "Resolved account_id: $account_id"
write_block ""

run_request "Get User Accounts" "GET" "$BASE_URL/api/users/$user_id/accounts" "" "yes" "no" "200" >/dev/null
run_request "Get Account" "GET" "$BASE_URL/api/accounts/$account_id" "" "yes" "no" "200" >/dev/null
run_request "Update Account" "PUT" "$BASE_URL/api/accounts/$account_id" "{\"account_name\":\"Primary Checking\",\"account_type\":\"Checking\",\"institution_id\":$institution_id}" "yes" "no" "200" >/dev/null

create_category_body="$(run_request "Create Category" "POST" "$BASE_URL/api/users/$user_id/categories" "{\"category_name\":\"Groceries\",\"budget\":500}" "yes" "no" "201")"
category_id="$(json_get "$create_category_body" "category.category_id" 2>/dev/null || true)"

if [[ -z "$category_id" ]]; then
  write_block "ERROR: Could not resolve category_id from create category response."
  write_block "Ended: $(date)"
  rm -f "$TMP_BODY"
  exit 1
fi

write_block "Resolved category_id: $category_id"
write_block ""

run_request "Get User Categories" "GET" "$BASE_URL/api/users/$user_id/categories" "" "yes" "no" "200" >/dev/null
run_request "Get Category" "GET" "$BASE_URL/api/categories/$category_id" "" "yes" "no" "200" >/dev/null
run_request "Update Category" "PUT" "$BASE_URL/api/categories/$category_id" "{\"category_name\":\"Food\",\"budget\":650}" "yes" "no" "200" >/dev/null

create_transaction_body="$(run_request "Create Transaction" "POST" "$BASE_URL/api/accounts/$account_id/transactions" "{\"date\":\"2026-04-16\",\"payee\":\"Trader Joes\",\"memo\":\"Weekly groceries\",\"outflow\":84.22,\"inflow\":0,\"category_id\":$category_id}" "yes" "no" "201")"
transaction_id="$(json_get "$create_transaction_body" "transaction.transaction_id" 2>/dev/null || true)"

if [[ -z "$transaction_id" ]]; then
  write_block "ERROR: Could not resolve transaction_id from create transaction response."
  write_block "Ended: $(date)"
  rm -f "$TMP_BODY"
  exit 1
fi

write_block "Resolved transaction_id: $transaction_id"
write_block ""

run_request "Get Account Transactions" "GET" "$BASE_URL/api/accounts/$account_id/transactions" "" "yes" "no" "200" >/dev/null
run_request "Get Account Transactions In Date Range" "GET" "$BASE_URL/api/accounts/$account_id/transactions?start_date=2026-04-01&end_date=2026-04-30" "" "yes" "no" "200" >/dev/null
run_request "Get Transaction" "GET" "$BASE_URL/api/transactions/$transaction_id" "" "yes" "no" "200" >/dev/null
run_request "Update Transaction" "PUT" "$BASE_URL/api/transactions/$transaction_id" "{\"date\":\"2026-04-17\",\"payee\":\"Trader Joes\",\"memo\":\"Updated memo\",\"outflow\":90.00,\"inflow\":0,\"category_id\":$category_id}" "yes" "no" "200" >/dev/null
run_request "Delete Transaction" "DELETE" "$BASE_URL/api/transactions/$transaction_id" "" "yes" "no" "200" >/dev/null

run_request "Delete Category" "DELETE" "$BASE_URL/api/categories/$category_id" "" "yes" "no" "200" >/dev/null
run_request "Delete Account" "DELETE" "$BASE_URL/api/accounts/$account_id" "" "yes" "no" "200" >/dev/null
run_request "Delete User" "DELETE" "$BASE_URL/api/users/$user_id" "" "yes" "no" "200" >/dev/null

write_block "============================================================"
write_block "SUMMARY"
write_block "TOTAL_TESTS: $TOTAL_TESTS"
write_block "PASSED_TESTS: $PASSED_TESTS"
write_block "FAILED_TESTS: $FAILED_TESTS"
if [[ "$FAILED_TESTS" -gt 0 ]]; then
  write_block "FAILED_TEST_DETAILS:"
  printf "%b" "$FAILED_TEST_NAMES" >> "$RESULTS_FILE"
else
  write_block "FAILED_TEST_DETAILS: none"
fi
write_block ""

write_block "Completed: $(date)"
write_block "Results file: $RESULTS_FILE"

rm -f "$TMP_BODY"

printf "Test run complete. Results written to %s\n" "$RESULTS_FILE"

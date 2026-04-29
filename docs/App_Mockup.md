# Budgeting App Mockup

This mockup uses Mermaid to represent the app structure and home page dashboard layout.

```mermaid
flowchart TB
    %% Global app shell
    App[Budgeting App]
    TopNav[Top Toolbar / Navigation]

    App --> TopNav

    %% Toolbar links
    TopNav --> HomeLink[Home]
    TopNav --> BudgetLink[Budget]
    TopNav --> TransactionsLink[Transactions]
    TopNav --> GoalsLink[Goals]
    TopNav --> ReportsLink[Reports]
    TopNav --> SettingsLink[Settings]

    %% Home page main content
    HomeLink --> HomePage[Home Page Dashboard]

    HomePage --> WelcomeCard[Welcome + Monthly Snapshot]
    HomePage --> MoneyCard[Money Available / Account Balances]
    HomePage --> RemainingCard[Budget Remaining This Month]

    %% Graph area
    HomePage --> GraphSection[Insights & Graphs]

    GraphSection --> SpendVsBudget[Bar Chart: Spending vs Budget by Category]
    GraphSection --> MonthlyTrend[Line Chart: Income and Spending Trend]
    GraphSection --> CategorySplit[Pie Chart: Category Breakdown]
    GraphSection --> CashFlow[Area Chart: Cash Flow Over Time]

    %% Quick actions
    HomePage --> QuickActions[Quick Actions]
    QuickActions --> AddTransaction[Add Transaction]
    QuickActions --> EditBudget[Update Budget]
    QuickActions --> ViewDetails[View Detailed Report]

    %% Other pages summarized
    BudgetLink --> BudgetPage[Budget Page: category limits + adjustments]
    TransactionsLink --> TransactionsPage[Transactions Page: list, filters, add/edit]
    GoalsLink --> GoalsPage[Goals Page: savings goals + progress]
    ReportsLink --> ReportsPage[Reports Page: monthly and custom reports]
    SettingsLink --> SettingsPage[Settings Page: profile, preferences, accounts]
```

## Notes

- The home page is focused on quick financial awareness.
- The toolbar provides easy movement between core budgeting workflows.
- Graphs can be powered by real transaction and budget data from your backend.

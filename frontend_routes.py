
def register_routes(app):

    @app.route('/')
    def home():
        return render_template('index.html', title='Home')


    @app.route('/register')
    def register():
        #Pass needed data to the page
        return render_template('register.html', title='Register')

    @app.route('/login')
    def login():
        #Pass needed data to the page
        return render_template('login.html', title='Login')

    @app.route('/profile')
    def profile():
        #Pass needed data to the page
        return render_template('profile.html', title='Profile')

    @app.route('/accounts')
    def accounts():
        #Pass needed data to the page
        return render_template('accounts.html', title='Accounts')

    @app.route('/transactions')
    def transactions():
        #Pass needed data to the page
        return render_template('transactions.html', title='Transactions')

    @app.route('/budget')
    def budget():
        #Pass needed data to the page
        return render_template('budget.html', title='Budget')

    
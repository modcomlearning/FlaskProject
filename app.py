from flask import *
app = Flask(__name__)  # __name__ means main
# This secret key encrypts yur user session for security reasons
app.secret_key = 'AG_66745_hhYuo!@' # 16
@app.route('/')
def home():
    return render_template('home.html')  # run http://127.0.0.1:5000/home

import pymysql
# establish db connection
connection = pymysql.connect(host='localhost', user='root',
                             password='', database='shoes_db')
@app.route('/shoes')
def shoes():
    # create your query
    sql = "SELECT * FROM products_tbl"
    # execute/run your
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # Now use the cursor to execute your sql
    cursor.execute(sql)

    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template('shoes.html', msg = 'Out of Stock')
    else:
        rows  = cursor.fetchall()
        return render_template('shoes.html', rows = rows)


# this route will display single shoe
# this route will need a product id
@app.route('/single/<product_id>')
def single(product_id):
    # create your query, provide a %s placeholder
    sql = "SELECT * FROM products_tbl WHERE product_id = %s"
    # execute/run your
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # Now use the cursor to execute your sql
    # below you provide id to replace the %s
    cursor.execute(sql, (product_id))

    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template('single.html', msg = 'Product does not exist')
    else:
        row  = cursor.fetchone()  # NB: product id was unique, so fetch one
        return render_template('single.html', row = row)


# this is the login route
# below route accepts a GET or a POST
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        # receive the posted email and password as varaibles
        email = request.form['email']
        password = request.form['password']
        # we now move to the database and confirm if above details exist
        sql = "SELECT * FROM customers where customer_email = %s and customer_password=%s"
        # create a cursor and execute above sql
        cursor = connection.cursor()
        # execute the sql, provide email and password to fit %s placeholders
        cursor.execute(sql, (email, password))
        # check if a match was found
        if cursor.rowcount ==0:
            return render_template('login.html', error = 'Wrong Credentials')
        elif cursor.rowcount ==1:
            # create a user to track who is logged in
            # attach user email to the session
            session['user'] = email
            return  redirect('/shoes')
        else:
            return render_template('login.html', error='Error Occured, Try Later')
    else:
        return render_template('login.html')

# Create a sign up templates create fiel;ds as per customer table
@app.route('/register', methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        customer_fname = request.form['customer_fname']
        customer_lname = request.form['customer_lname']
        customer_surname = request.form['customer_surname']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_password = request.form['customer_password']
        customer_password2 = request.form['customer_password2']
        customer_gender = request.form['customer_gender']
        customer_address = request.form['customer_address']
        dob = request.form['dob']

        # validations
        import re
        if customer_password != customer_password2:
            return render_template('register.html', password = 'Password do not match')

        elif len(customer_password) < 8:
            return render_template('register.html', password='Password must 8 characters')

        elif not re.search("[a-z]", customer_password):
            return render_template('register.html', password='Must have a small letter')

        elif not re.search("[A-Z]", customer_password):
            return render_template('register.html', password='Must have a caps letter')

        elif not re.search("[0-9]", customer_password):
            return render_template('register.html', password='Must have a number')

        elif not re.search("[_@$]", customer_password):
            return render_template('register.html', password='Must have a small letter')

        elif len(customer_phone) < 10:
            return render_template('register.html', phone='Must be above 10 numbers')

        else:
            sql = "insert into customers(customer_fname, customer_lname, customer_surname, customer_email, customer_phone, customer_password, customer_gender, customer_address, dob) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = connection.cursor()
            try:
                cursor.execute(sql, (customer_fname, customer_lname, customer_surname,
                                     customer_email,customer_phone, customer_password,
                                     customer_gender, customer_address, dob))
                connection.commit()
                return render_template('register.html', success = 'Saved Successfully')
            except:
                return render_template('register.html', error='Failed')
    else:
        return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user') # clear session
    return redirect('/login')


@app.route('/reviews', methods = ['POST','GET'])
def reviews():
    if request.method =='POST':
        user = request.form['user']
        product_id = request.form['product_id']
        message = request.form['message']
        sql = "insert into reviews(user, product_id, message) values (%s, %s, %s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql, (user, product_id, message))
            connection.commit()
            return 'Success'
        except:
            return 'Failed'
    else:
        return ''
# create a table named reviews
#review_id INT PK AI   50
# user VARCHAR 100
# product_id INT 50
# message VARCHAR 200
# review_date TIMESTAMP   - default CURRENT TIME STAMP

# git link: https://github.com/modcomlearning/FlaskProject
# create a github.com account

if __name__ =='__main__':
    app.run()
# Right click run,
#http://127.0.0.1:5000/shoes

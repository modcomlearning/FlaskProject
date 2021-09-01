from flask import *
# method 2: Click on View - Tools Windows -Terminal
# Once terminal type:  pip install flask
# Create the flask Object
app = Flask(__name__)  # __name__ means main
# This is the body of your Flask Object
# This is the main defaul route
@app.route('/')
def home():
    return render_template('home.html')  # run http://127.0.0.1:5000/home


@app.route('/signin')
def signin():
    return render_template('signin.html')

# check
if __name__ =='__main__':
    app.run(debug=True)
from flask import render_template, request
import subprocess

from app import app 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/account', methods=['POST'])
def account():
    account = request.form['account_name']
    return 'hello sir, ' + account

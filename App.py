from flask import Flask, render_template, url_for,flash, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aaaaaa'
app.config['MYSQL_DB'] = 'employees'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select * from employee")
    employee = cur.fetchall()
    cur.close()
    return render_template('indexNew.html', employee= employee)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method=="POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        salary = request.form['salary']
        department = request.form['department']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee (name, email, salary, department) VALUES (%s, %s, %s, %s)", (name, email, salary, department))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/update/<string:id>', methods=['POST','GET'])
def update(id):
    if request.method=='POST':
        # id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        salary = request.form['salary']
        department = request.form['department']

        cur = mysql.connection.cursor()
        cur.execute(" UPDATE employee SET name=%s, email=%s, salary=%s, department=%s WHERE id=%s", (name, email, salary, department,id))
        flash("Data Updated Successfully", 'success')
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id=%s", (id))
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug= True)
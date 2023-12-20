from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# insearting data into students table
def insertdata():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        query = "DROP TABLE IF EXISTS students;"
        cursor.execute(query)
        print("Old table dropped!")
        query = "CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, percentage REAL, locality TEXT, roll_no INTEGER);"
        cursor.execute(query)
        print("New db student created!")
    except:
        print("something wrong here")
    query = """INSERT INTO students (name, percentage, locality, roll_no) VALUES
    ('Nur Aktar', 85.5, 'Chinpai', 15),
    ('Kuntal', 82, 'Bolpur', 77),
    ('Imran', 102.3, 'Bolpur', 14),
    ('Dhruv', 92.3, 'Bolpur', 102),
    ('Debaprya', 78.9, 'Bolpur', 23);"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    print("db updated")
insertdata()

def query_database(studentid):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = "SELECT * FROM students WHERE id = "+studentid
    cursor.execute(query)
    user_data = cursor.fetchone()
    connection.close()
    return user_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def get_data():
    user_data = ""
    studentid = request.args.get('id')
    user_data = query_database(studentid)
    if user_data != None:
        data = "Id:"+str(user_data[0])+"<br>"+"Name: "+user_data[1]+"<br>"+"Roll: "+str(user_data[4])+"<br>"+"Persentage: "+str(user_data[2])+"<br>"+"Locality: "+user_data[3]
    else:
        data = "No DATA!"
    return jsonify(data=data)

if __name__ == '__main__':
    app.run(debug=True)
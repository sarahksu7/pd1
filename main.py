from flask import Flask, render_template, request, make_response, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Function to establish connection to SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def create_table():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS doctors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, bod DATE)''')
    conn.commit()
    conn.close()

# Fetch all doctors from the database
def get_doctors():
    conn = get_db_connection()
    doctors = conn.execute('SELECT * FROM doctors').fetchall()
    conn.close()
    return doctors

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/doctors')
def doctors():
    doctors = get_doctors()
    return render_template('doctors.html', doctors=doctors)

@app.route('/create_doctor',  methods=['GET', 'POST'])
def create_doctor():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        bod = request.form['bod']

        conn = get_db_connection()
        create_table()

        # Insert form data into the database
        conn.execute("INSERT INTO doctors (name, email, bod) VALUES (?, ?, ?)", (name, email, bod))

        # Commit the transaction
        conn.commit()
        conn.close()

        flash('Doctor has been created successfully!', 'success')

        response = make_response(f"Received data: Name - {name}, Email - {email}, Birth of Date - {bod}", 201)
        return redirect(url_for('doctors'))
    else:
        return render_template('create_doctor.html')

@app.route('/remove_doctor', methods=['POST'])
def remove_doctor():
    doctor_id = request.form['doctor_id']
    
    # Connect to the SQLite database
    conn = get_db_connection()

    # Execute SQL DELETE statement to remove the record
    conn.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))

    # Commit the transaction
    conn.commit()
    conn.close()

    flash('Doctor has been removed successfully!', 'success')

    return redirect(url_for('doctors'))  # Redirect to the doctors page after removal

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

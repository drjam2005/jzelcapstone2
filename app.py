# app.py
from flask import Flask, request, render_template, redirect
import sqlite3
import sys

database = sqlite3.connect("database.db")
datacursor = database.cursor()
app = Flask(__name__)

def sort_transactions_by_date(transactions):
    return sorted(transactions, key=lambda x: x[4])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    global student_id
    student_id = request.form['student_id']
    if student_id == "adminlogin":
        database = sqlite3.connect("database.db")
        datacursor = database.cursor()
        datacursor.execute("UPDATE studentDATA SET studentPRINTED = 0")
        database.commit()
        database.close()
        return redirect("/") 
    try:
        database = sqlite3.connect("database.db")
        datacursor = database.cursor()
        datacursor.execute("SELECT * FROM studentDATA WHERE studentID = ?", (student_id,))
        database.close()
        return render_template("/password.html", studentid=student_id)
    except:
        return render_template("/error.html", error="User not found!")

@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'GET':
        return render_template('password.html', studentid=student_id)
    elif request.method == 'POST':
        try:
            database = sqlite3.connect("database.db")
            datacursor = database.cursor()
            site_password = request.form['sitepassword']
            datacursor.execute("SELECT * FROM studentDATA WHERE studentID = ?", (student_id,))
            student = datacursor.fetchone()
            database.close()
            global strand
            global name
            userid, name, balance, debt, password, strand, printed = student
            if str(password) == str(site_password):
                database = sqlite3.connect("database.db")
                datacursor = database.cursor()
                datacursor.execute("SELECT * FROM StatementOfAccounts WHERE studentID = ?", (student_id,))
                statements = sort_transactions_by_date(datacursor.fetchall())
                database.close()
                print(printed)
                if balance >= debt and printed == 0:
                    print("okay")
                    return render_template("/statements.html", transactions=statements, print=True, checker=0, user_name=name, user_id=student_id)
                else:
                    return render_template("/statements.html", transactions=statements, user_name=name, print=False, checker=1, user_id=student_id)
            else:
                return render_template("/error.html", error="Incorrect Password!")
        except:
            return render_template("/error.html", error="User not found!")


@app.route('/printPermit')
def print_pertmit():
    database = sqlite3.connect("database.db")
    datacursor = database.cursor()
    datacursor.execute("UPDATE studentDATA SET studentPRINTED = ? WHERE studentID = ?", (1, student_id))
    database.commit()
    database.close()
    if strand == "STEM12":
        STEM12_table = [('SPEC_STEM_7', 'General Biology 2'), 
                        ('SPEC_STEM_8', 'General Chemistry 2'), 
                        ('SPEC_STEM_6', 'General Physics 2'), 
                        ('CORE_IT_1', 'Media and Information Literacy'), 
                        ('CORE_PE_12-2', 'Physical Education and Health'), 
                        ('APP_RESEARCH_2', 'Research In Daily Life 2'), 
                        ('APP_RESEARCH_3', 'Research Project'), 
                        ('SPEC_STEM_9', 'Research Capstone Project')]
        strandinfo = STEM12_table
    elif strand == "ABM12":
        ABM12_table =  [('SPEC_ABM_9', 'Business Enterprise Simulation'), 
                        ('SPEC_ABM_7', 'Business Ethics and Social Responsibility'), 
                        ('SPEC_ABM_5', 'Business Finance'), 
                        ('APP_ENG_1', 'English for Academic and Professional Purposes'),  
                        ('APP_ENTREP_1', 'Entrepeneurship'), 
                        ('APP_FIL_2', 'Pagsulat sa Filipino sa Piling Larangan (Akademik)'), 
                        ('APP_RESEARCH_3', 'Research Project')]
        strandinfo = ABM12_table
    return render_template("/printPermit.html", strandinfo=strandinfo, user_name=name, user_id=student_id)
if __name__ == '__main__':
    app.run(debug=True)

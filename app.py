from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "student_portal_secret"

# =========================
# Database Configuration
# =========================

DB_FILE = "college.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def landing():
    return render_template("landing.html")

def check_login():
    return "rollno" in session

def get_student_records(table_name, rollno):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name} WHERE RollNo = ?", (rollno,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def faculty_logged_in():
    return "faculty_id" in session

@app.route("/faculty-login", methods=["GET", "POST"])
def faculty_login():
    if request.method == "POST":
        faculty_id = request.form["faculty_id"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM faculty_login WHERE FacultyID = ? AND Password = ?", (faculty_id, password))
        faculty = cur.fetchone()
        conn.close()

        if faculty:
            session["faculty_id"] = faculty_id
            session["faculty_name"] = faculty["Name"]
            return redirect("/faculty-dashboard")

        return render_template(
            "faculty_login.html",
            error="Invalid Faculty Credentials"
        )

    return render_template("faculty_login.html")

# =====================================
# FACULTY MODULES
# =====================================

@app.route("/faculty-dashboard")
def faculty_dashboard():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    conn.close()

    return render_template(
        "faculty_dashboard.html",
        faculty_name=session["faculty_name"],
        total_students=total_students
    )

@app.route("/manage-students")
def manage_students():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template(
        "manage_students.html",
        students=[dict(row) for row in students]
    )

@app.route("/add-student", methods=["GET", "POST"])
def add_student():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    if request.method == "POST":
        rollno = request.form["rollno"]
        name = request.form["name"]
        branch = request.form["branch"]
        section = request.form["section"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO students (RollNo, Name, Branch, Section, Mobile, Email) VALUES (?, ?, ?, ?, ?, ?)",
            (rollno, name, branch, section, mobile, email)
        )
        
        cur.execute(
            "INSERT INTO student_login (RollNo, Password) VALUES (?, ?)",
            (rollno, password)
        )
        
        conn.commit()
        conn.close()

        return redirect("/manage-students")

    return render_template("add_student.html")

@app.route("/manage-attendance", methods=["GET", "POST"])
def manage_attendance():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        rollno = request.form["rollno"]
        python_att = request.form["python"]
        dbms_att = request.form["dbms"]
        java_att = request.form["java"]
        cn_att = request.form["cn"]
        os_att = request.form["os"]

        conn.execute(
            "UPDATE attendance SET Python=?, DBMS=?, Java=?, CN=?, OS=? WHERE RollNo=?",
            (python_att, dbms_att, java_att, cn_att, os_att, rollno)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-attendance")

    data = conn.execute("SELECT * FROM attendance").fetchall()
    conn.close()

    return render_template(
        "manage_attendance.html",
        data=[dict(row) for row in data]
    )

@app.route("/manage-internal", methods=["GET", "POST"])
def manage_internal():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        rollno = request.form["rollno"]
        python_marks = request.form["python"]
        dbms_marks = request.form["dbms"]
        java_marks = request.form["java"]
        cn_marks = request.form["cn"]
        os_marks = request.form["os"]

        conn.execute(
            "UPDATE internal_marks SET Python=?, DBMS=?, Java=?, CN=?, OS=? WHERE RollNo=?",
            (python_marks, dbms_marks, java_marks, cn_marks, os_marks, rollno)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-internal")

    data = conn.execute("SELECT * FROM internal_marks").fetchall()
    conn.close()

    return render_template(
        "manage_internal.html",
        data=[dict(row) for row in data]
    )

@app.route("/manage-external", methods=["GET", "POST"])
def manage_external():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        rollno = request.form["rollno"]
        python_marks = request.form["python"]
        dbms_marks = request.form["dbms"]
        java_marks = request.form["java"]
        cn_marks = request.form["cn"]
        os_marks = request.form["os"]

        conn.execute(
            "UPDATE external_marks SET Python=?, DBMS=?, Java=?, CN=?, OS=? WHERE RollNo=?",
            (python_marks, dbms_marks, java_marks, cn_marks, os_marks, rollno)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-external")

    data = conn.execute("SELECT * FROM external_marks").fetchall()
    conn.close()

    return render_template(
        "manage_external.html",
        data=[dict(row) for row in data]
    )

@app.route("/manage-timetable", methods=["GET", "POST"])
def manage_timetable():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        day = request.form["day"]
        p1 = request.form["p1"]
        p2 = request.form["p2"]
        p3 = request.form["p3"]
        p4 = request.form["p4"]
        p5 = request.form["p5"]

        conn.execute(
            "UPDATE timetable SET P1=?, P2=?, P3=?, P4=?, P5=? WHERE Day=?",
            (p1, p2, p3, p4, p5, day)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-timetable")

    data = conn.execute("SELECT * FROM timetable").fetchall()
    conn.close()

    return render_template(
        "manage_timetable.html",
        data=[dict(row) for row in data]
    )

# =========================
# Login
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        rollno = request.form["rollno"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM student_login WHERE RollNo = ? AND Password = ?",
            (rollno, password)
        ).fetchone()
        conn.close()

        if user:
            session["rollno"] = rollno
            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid Roll Number or Password"
        )

    return render_template("login.html")

# =========================
# Dashboard
# =========================

@app.route("/dashboard")
def dashboard():
    if not check_login():
        return redirect("/login")

    rollno = session["rollno"]
    profile_data = get_student_records("students", rollno)

    if not profile_data:
        return redirect("/logout")

    profile = profile_data[0]

    return render_template(
        "dashboard.html",
        profile=profile
    )

# =========================
# Profile
# =========================

@app.route("/profile")
def profile():
    if not check_login():
        return redirect("/login")

    data = get_student_records("students", session["rollno"])

    return render_template(
        "profile.html",
        data=data
    )

# =========================
# Attendance
# =========================

@app.route("/attendance")
def attendance():
    if not check_login():
        return redirect("/login")

    data = get_student_records("attendance", session["rollno"])

    return render_template(
        "attendance.html",
        data=data
    )

# =========================
# Internal Marks
# =========================

@app.route("/internal")
def internal():
    if not check_login():
        return redirect("/login")

    data = get_student_records("internal_marks", session["rollno"])

    return render_template(
        "internal_marks.html",
        data=data
    )

# =========================
# External Marks
# =========================

@app.route("/external")
def external():
    if not check_login():
        return redirect("/login")

    data = get_student_records("external_marks", session["rollno"])

    return render_template(
        "external_marks.html",
        data=data
    )

# =========================
# Semester Results
# =========================

@app.route("/semester")
def semester():
    if not check_login():
        return redirect("/login")

    data = get_student_records("semester_results", session["rollno"])

    return render_template(
        "semester_results.html",
        data=data
    )

# =========================
# Fee Details
# =========================

@app.route("/fees")
def fees():
    if not check_login():
        return redirect("/login")

    data = get_student_records("fee_details", session["rollno"])

    return render_template(
        "fee_details.html",
        data=data
    )

# =========================
# Time Table
# =========================

@app.route("/timetable")
def timetable():
    if not check_login():
        return redirect("/login")

    conn = get_db_connection()
    data = conn.execute("SELECT * FROM timetable").fetchall()
    conn.close()

    return render_template(
        "timetable.html",
        data=[dict(row) for row in data]
    )

# =========================
# Backlogs
# =========================

@app.route("/backlog")
def backlog():
    if not check_login():
        return redirect("/login")

    data = get_student_records("backlogs", session["rollno"])

    return render_template(
        "backlog.html",
        data=data
    )

@app.route("/idcard")
def idcard():
    if not check_login():
        return redirect("/login")

    rollno = session["rollno"]
    profile_data = get_student_records("students", rollno)
    
    if profile_data:
        student = profile_data[0]
    else:
        student = {}

    return render_template(
        "idcard.html",
        student=student
    )

# =========================
# Logout
# =========================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# =========================
# FACULTY LOGOUT
# =========================

@app.route("/faculty-logout")
def faculty_logout():
    session.pop("faculty_id", None)
    session.pop("faculty_name", None)
    return redirect("/")

# =========================
# MANAGE FEES
# =========================

@app.route("/manage-fees", methods=["GET", "POST"])
def manage_fees():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        rollno = request.form["rollno"]
        total_fee = request.form["total_fee"]
        paid_fee = request.form["paid_fee"]
        due_fee = request.form["due_fee"]

        conn.execute(
            "UPDATE fee_details SET TotalFee=?, PaidFee=?, DueFee=? WHERE RollNo=?",
            (total_fee, paid_fee, due_fee, rollno)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-fees")

    data = conn.execute("SELECT * FROM fee_details").fetchall()
    conn.close()

    return render_template(
        "manage_fees.html",
        data=[dict(row) for row in data]
    )

# =========================
# MANAGE SEMESTER
# =========================

@app.route("/manage-semester", methods=["GET", "POST"])
def manage_semester():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        rollno = request.form["rollno"]
        semester = request.form["semester"]
        sgpa = request.form["sgpa"]
        cgpa = request.form["cgpa"]
        result = request.form["result"]

        conn.execute(
            "UPDATE semester_results SET Semester=?, SGPA=?, CGPA=?, Result=? WHERE RollNo=?",
            (semester, sgpa, cgpa, result, rollno)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-semester")

    data = conn.execute("SELECT * FROM semester_results").fetchall()
    conn.close()

    return render_template(
        "manage_semester.html",
        data=[dict(row) for row in data]
    )

# =========================
# MANAGE EVENTS
# =========================

@app.route("/manage-events")
def manage_events():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()
    data = conn.execute("SELECT * FROM events").fetchall()
    conn.close()

    return render_template(
        "manage_events.html",
        data=[dict(row) for row in data]
    )

# =========================
# MANAGE LIBRARY
# =========================

@app.route("/manage-library", methods=["GET", "POST"])
def manage_library():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        book_id = request.form["book_id"]
        book_name = request.form["book_name"]
        author = request.form["author"]
        total_copies = request.form["total_copies"]
        available_copies = request.form["available_copies"]

        conn.execute(
            "UPDATE library_books SET BookName=?, Author=?, TotalCopies=?, AvailableCopies=? WHERE BookID=?",
            (book_name, author, total_copies, available_copies, book_id)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-library")

    data = conn.execute("SELECT * FROM library_books").fetchall()
    conn.close()

    return render_template(
        "manage_library.html",
        data=[dict(row) for row in data]
    )

# =========================
# MANAGE PLACEMENTS
# =========================

@app.route("/manage-placements", methods=["GET", "POST"])
def manage_placements():
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        drive_id = request.form["drive_id"]
        company = request.form["company"]
        package = request.form["package"]
        drive_date = request.form["drive_date"]
        branches = request.form["branches"]

        conn.execute(
            "UPDATE placement_drives SET Company=?, Package=?, DriveDate=?, EligibleBranches=? WHERE DriveID=?",
            (company, package, drive_date, branches, drive_id)
        )
        conn.commit()
        conn.close()
        return redirect("/manage-placements")

    data = conn.execute("SELECT * FROM placement_drives").fetchall()
    conn.close()

    return render_template(
        "manage_placements.html",
        data=[dict(row) for row in data]
    )

# =========================
# DELETE STUDENT
# =========================

@app.route("/delete-student/<rollno>")
def delete_student(rollno):
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()
    tables_to_clear = [
        "students", "student_login", "attendance", "internal_marks", 
        "external_marks", "semester_results", "fee_details"
    ]

    for table in tables_to_clear:
        conn.execute(f"DELETE FROM {table} WHERE RollNo = ?", (rollno,))
    
    conn.commit()
    conn.close()

    return redirect("/manage-students")

# =========================
# EDIT STUDENT
# =========================

@app.route("/edit-student/<rollno>", methods=["GET", "POST"])
def edit_student(rollno):
    if not faculty_logged_in():
        return redirect("/faculty-login")

    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        branch = request.form["branch"]
        section = request.form["section"]
        mobile = request.form["mobile"]
        email = request.form["email"]

        conn.execute(
            "UPDATE students SET Name=?, Branch=?, Section=?, Mobile=?, Email=? WHERE RollNo=?",
            (name, branch, section, mobile, email, rollno)
        )
        conn.commit()
        conn.close()

        return redirect("/manage-students")
    else:
        student_row = conn.execute("SELECT * FROM students WHERE RollNo = ?", (rollno,)).fetchone()
        conn.close()
        
        student = dict(student_row) if student_row else {}

        return render_template(
            "edit_student.html",
            student=student
        )

if __name__ == "__main__":
    app.run(debug=True)
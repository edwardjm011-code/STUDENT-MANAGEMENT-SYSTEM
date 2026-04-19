from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "secretkey"

# ---------------- LOGIN DETAILS ----------------
USERNAME = "EDWARD"
PASSWORD = 12345

# ---------------- DATABASE ----------------
students = []
student_number = 1

# ---------------- CSS ----------------
style = 
<style>"""
body { font-family: Arial; background:#f4f6f9; margin:0; }
.navbar { background:#2c3e50; padding:15px; }
.navbar a { color:white; margin-right:15px; text-decoration:none; }
.container { width:80%; margin:auto; margin-top:30px; }
form { background:powderblue; padding:20px; border-radius:10px; width:300px; }
input { width:100%; padding:10px; margin:10px 0; }
button { background:#3498db; color:white; padding:10px; border:none; width:100%; }
table { width:100%; background:white; border-collapse:collapse; }
th, td { padding:10px; border:1px solid #ddd; }
th { background:#3498db; color:white; }
a.btn { padding:5px 10px; background:#2ecc71; color:white; text-decoration:none; }
a.delete { background:red; }
</style>"""


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template_string(style + """
    <div class="container">
        <h1>Student Management System</h1>
        <p>Already have an account</p>
        <a href="/login">Login</a>
        <p>If you do not have an account</p>
        <a href="/register">Register</a>
    </div>
    """)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/HOME")
        else:
            return "Invalid login! Please confirm your details!!!"

    return render_template_string(style + """
    <div class="container">
        <h1>Login</h1>
        <form method="POST">
            <input name="username" placeholder="Username">
            <input type="password" name="password" placeholder="Password">
            <button>Login</button>
        </form>
    </div>
    """)

# ---------------- DASHBOARD ----------------
@app.route("/HOME")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")

    return render_template_string(style + """
    <div class="navbar">
        <a href="/HOME">HOME</a>
        <a href="/Registration>REGISTER</a>
        <a href="/add">Add Student</a>
        <a href="/students">Students</a>
        <a href="/logout">Logout</a>
    </div>

    <div class="container">
        <h1>Dashboard</h1>
        <p>Welcome to the system</p>
    </div>
    """)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
    global student_number

    if not session.get("logged_in"):
        return redirect("/login")

    if request.method == "POST":
        students.append({
            "student_number": student_number,
            "name": request.form["name"],
            "nrc": request.form["nrc"],
            "course": request.form["course"],
            "year": request.form["year"]
        })
        student_number += 1
        return redirect("/students")

    return render_template_string(style + """
    <div class="navbar">
        <a href="/dashboard">Dashboard</a>
        <a href="/students">Students</a>
    </div>

    <div class="container">
        <h1>Add Student</h1>
        <form method="POST">
            <input name="name" placeholder="Name">
            <input name="nrc" placeholder="NRC No">
            <input name="course" placeholder="Course">
            <input name="year" placeholder="Year">
            <button>Add</button>
        </form>
    </div>
    """)

# ---------------- VIEW STUDENTS ----------------
@app.route("/students")
def view_students():
    if not session.get("logged_in"):
        return redirect("/login")

    return render_template_string(style + """
    <div class="navbar">
        <a href="/HOME">HOME</a>
        <a href="/add">Add Student</a>
        <a href="/logout">Logout</a>
    </div>

    <div class="container">
        <h1>Students</h1>

        <table>
            <tr>
                <th>Student Number</th>
                <th>Name</th>
                <th>NRC</th>
                <th>Course</th>
                <th>Year</th>
                <th>Actions</th>
            </tr>

            {% for s in students %}
            <tr>
                <td>{{ s["student_number"] }}</td>
                <td>{{ s["name"] }}</td>
                <td>{{ s["nrc"] }}</td>
                <td>{{ s["course"] }}</td>
                <td>{{ s["year"] }}</td>
                <td>
                    <a href="/edit/{{ s['student_number'] }}" class="btn">Edit</a>
                    <a href="/delete/{{ s['student_number'] }}" class="btn delete">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>
    """, students=students)

# ---------------- DELETE ----------------
@app.route("/delete/<int:student_number>")
def delete_student(student_number):
    global students
    students = [s for s in students if s["student_number"] != student_number]
    return redirect("/students")

# ---------------- EDIT ----------------
@app.route("/edit/<int:student_number>", methods=["GET", "POST"])
def edit_student(student_number):
    student = next((s for s in students if s["student_number"] == student_number), None)

    if not student:
        return "Student not found"

    if request.method == "POST":
        student["name"] = request.form["name"]
        student["nrc"] = request.form["nrc"]
        student["course"] = request.form["course"]
        student["year"] = request.form["year"]
        return redirect("/students")

    return render_template_string(style + """
    <div class="navbar">
        <a href="/Home">HOME</a>
        <a href="/students">Students</a>
    </div>

    <div class="container">
        <h1>Edit Student</h1>

        <form method="POST">
            <input name="name" value="{{ s['name'] }}">
            <input name="nrc" value="{{ s['nrc'] }}">
            <input name="course" value="{{ s['course'] }}">
            <input name="year" value="{{ s['year'] }}">
            <button>Update</button>
        </form>
    </div>
    """, s=student)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
from pathlib import Path

from flask import Flask, render_template, request, redirect
from models import db, Student

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / 'database'
DATABASE_DIR.mkdir(exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DATABASE_DIR / 'students.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student = Student(
            name=request.form['name'],
            age=request.form['age'],
            course=request.form['course'],
            email=request.form['email']
        )

        db.session.add(student)
        db.session.commit()

        return redirect('/')

    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.course = request.form['course']
        student.email = request.form['email']

        db.session.commit()

        return redirect('/')

    return render_template('edit_student.html',
                           student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

import os
from dotenv import load_dotenv  # <-- ОБОВ'ЯЗКОВО додай цей імпорт!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Student, Group, Teacher, Subject, Grade
from faker import Faker
import random
from datetime import date, timedelta


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

session.query(Grade).delete()
session.query(Student).delete()
session.query(Subject).delete()
session.query(Teacher).delete()
session.query(Group).delete()
session.commit()


groups = []
for name in ["AD-101", "AD-102", "AD-103"]:
    group = Group(name=name)
    session.add(group)
    groups.append(group)
session.commit()


teachers = []
for _ in range(4):
    teacher = Teacher(fullname=fake.name())
    session.add(teacher)
    teachers.append(teacher)
session.commit()


subjects = []
for subj_name in ["Math", "Physics", "History", "Biology", "Chemistry", "Art", "Programming"]:
    subject = Subject(name=subj_name, teacher=random.choice(teachers))
    session.add(subject)
    subjects.append(subject)
session.commit()


students = []
for _ in range(50):
    student = Student(
        fullname=fake.name(),
        group=random.choice(groups)
    )
    session.add(student)
    students.append(student)
session.commit()


for student in students:
    for subject in subjects:
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                student=student,
                subject=subject,
                grade=random.uniform(60, 100),
                date_of=fake.date_between(start_date='-1y', end_date='today')
            )
            session.add(grade)
session.commit()

print("✅ Done! Database seeded.")

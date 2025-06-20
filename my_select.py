from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from database.models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import create_engine
from sqlalchemy import func, desc, cast, Numeric

DATABASE_URL = "postgresql+psycopg2://postgres:db-university-postgres@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """5 студентів з найвищим середнім балом з усіх предметів"""
    result = (
        session.query(
            Student.fullname,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade")
        )
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result

def select_2(subject_name):
    """Студент з найвищим середнім балом з певного предмета"""
    result = (
        session.query(
            Student.fullname,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade")
        )
        .join(Grade)
        .join(Subject)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return result


from sqlalchemy import func, desc, cast, Numeric 

def select_3(subject_name):
    """Середній бал у групах з певного предмета"""
    result = (
        session.query(
            Group.name,
            func.round(cast(func.avg(Grade.grade), Numeric), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student, Grade.student_id == Student.id)
        .join(Group, Student.group_id == Group.id)
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.id)
        .all()
    )
    return result


def select_4():
    """Середній бал на потоці"""
    result = session.query(
        func.round(cast(func.avg(Grade.grade), Numeric), 2)
    ).scalar()
    return result

def select_5(teacher_id):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()

def select_6(group_id):
    """Список студентів у певній групі"""
    result = session.query(Student.fullname).filter(Student.group_id == group_id).all()
    return result

def select_7(group_id, subject_name):
    """Оцінки студентів у групі з певного предмета"""
    result = (
        session.query(Student.fullname, Grade.grade)
        .join(Grade)
        .join(Subject)
        .filter(Student.group_id == group_id, Subject.name == subject_name)
        .all()
    )
    return result

def select_8(teacher_id):
    """Середній бал, який ставить певний викладач зі своїх предметів"""
    result = (
        session.query(
            func.round(cast(func.avg(Grade.grade), Numeric), 2)
        )
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    return result

def select_9(student_id):
    """Список курсів, які відвідує певний студент"""
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    return result

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач"""
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    return result

if __name__ == "__main__":
    print(" select_1:", select_1())
    print(" select_2:", select_2("Math"))
    print(" select_3:", select_3("Math"))
    print(" select_4:", select_4())
    print(" select_5:", select_5(5))
    print(" select_6:", select_6(6))
    print(" select_7:", select_7(6, "Math"))
    print(" select_8:", select_8(51))
    print(" select_9:", select_9(51))
    print(" select_10:", select_10(52, 6))
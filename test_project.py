import pytest
from project import parse_arguments, Student, Group


# Test cases for argument parsing
def test_arguments_parsing():
    args = parse_arguments(["-f", "students.csv", "-m", "4", "-M", "6"])
    assert args.file == "students.csv"
    assert args.min == 4
    assert args.max == 6


def test_arguments_parsing_defaults():
    args = parse_arguments(["-f", "students.csv"])
    assert args.file == "students.csv"
    assert args.min == 4  # Default value
    assert args.max == 6  # Default value


def test_arguments_parsing_invalid_min_max():
    with pytest.raises(SystemExit):
        parse_arguments(["-f", "students.csv", "-m", "-1"])
    with pytest.raises(SystemExit):
        parse_arguments(["-f", "students.csv", "-M", "0"])


# Test cases for Student and Group classes
def test_student_creation():
    student = Student("Alice")
    assert student.name == "Alice"
    assert student.id == 0
    assert student.gender is None
    student2 = Student("Bob")
    assert student2.name == "Bob"
    assert student2.id == 1
    assert student2.gender is None


def test_student_name_setter():
    student = Student("Alice")
    with pytest.raises(ValueError):
        student.name = ""


def test_student_gender_setter():
    student = Student("Alice")
    with pytest.raises(ValueError):
        student.gender = "Invalid"


def test_student_id_increment():
    student1 = Student("Alice")
    student2 = Student("Bob")
    assert student2.id == student1.id + 1


def test_student_str():
    student = Student("Alice")
    assert str(student) == f"Alice ({student.id})"


def test_student_seen_students():
    student1 = Student("Alice")
    student2 = Student("Bob")
    student1.seen_students[student2.id] = 1
    assert student2.id in student1.seen_students
    assert student1.seen_students[student2.id] == 1


def test_group_creation():
    group = Group(max_students=5, min_students=3)
    assert group.max_students == 5
    assert group.min_students == 3
    assert group.students == []


def test_group_str():
    group = Group()
    student1 = Student("Alice")
    student2 = Student("Bob")
    group.students.append(student1)
    group.students.append(student2)
    assert str(group) == f"Group {group.id}: Alice ({student1.id}), Bob ({student2.id})"


def test_group_id_increment():
    group1 = Group()
    group2 = Group()
    assert group2.id == group1.id + 1


def test_group_students_list():
    group = Group()
    student1 = Student("Alice")
    student2 = Student("Bob")
    group.students.append(student1)
    group.students.append(student2)
    assert group.students == [student1, student2]


def test_group_max_students_setter():
    group = Group()
    with pytest.raises(ValueError):
        group.max_students = -1
    with pytest.raises(ValueError):
        group.max_students = 0
    with pytest.raises(ValueError):
        group.max_students = "five"


def test_group_min_students_setter():
    group = Group()
    with pytest.raises(ValueError):
        group.min_students = -1
    with pytest.raises(ValueError):
        group.min_students = 0
    with pytest.raises(ValueError):
        group.min_students = "three"


def test_group_ratio_setter():
    group = Group()
    with pytest.raises(ValueError):
        group.ratio = -0.1
    with pytest.raises(ValueError):
        group.ratio = 1.1
    with pytest.raises(ValueError):
        group.ratio = "half"

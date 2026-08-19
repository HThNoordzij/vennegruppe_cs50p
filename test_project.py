import pytest
from project import (
    parse_arguments,
    Student,
    Group,
    read_students_from_csv,
    calculate_group_sizes,
    new_groups,
    score_groups,
    save_groups_to_csv,
    save_students_to_csv,
    update_seen_students,
)


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
    assert student.id == 1
    assert student.gender is None
    student2 = Student("Bob")
    assert student2.name == "Bob"
    assert student2.id == 2
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
    assert str(student) == f"Alice ({student.gender})"


def test_student_seen_students():
    student = Student("Alice")
    assert student.seen_students == []
    student.add_seen_student("Bob")
    assert "Bob" in student.seen_students


def test_group_creation():
    group = Group()
    assert group.students == []


def test_group_str():
    group = Group()
    student1 = Student("Alice")
    student2 = Student("Bob")
    group.students.append(student1)
    group.students.append(student2)
    assert (
        str(group)
        == f"Group {group.id}, ratio: {group.ratio:.2f}: Alice ({student1.gender}), Bob ({student2.gender})"
    )


def test_group_id_increment():
    group1 = Group()
    group2 = Group()
    assert group2.id == group1.id + 1


def test_group_students_list():
    group = Group()
    student1 = Student("Alice")
    student2 = Student("Bob")
    group.students = [student1, student2]
    assert len(group.students) == 2
    assert group.students[0] == student1
    assert group.students[1] == student2


def test_group_ratio_setter():
    group = Group()
    with pytest.raises(ValueError):
        group.ratio = -0.1
    with pytest.raises(ValueError):
        group.ratio = 1.1
    with pytest.raises(ValueError):
        group.ratio = "half"


# Test cases for reading students from CSV
def test_read_students_from_csv(tmp_path):
    # Create a temporary CSV file
    csv_file = tmp_path / "students.csv"
    csv_file.write_text("name,gender,seen_students\nAlice,F,\nBob,M,\nCharlie,X,\n")

    students = read_students_from_csv(str(csv_file))
    assert len(students) == 3
    assert students[0].name == "Alice"
    assert students[0].gender == "F"


def test_read_students_from_csv_invalid_gender(tmp_path):
    # Create a temporary CSV file with an invalid gender
    csv_file = tmp_path / "students.csv"
    csv_file.write_text("name,gender,seen_students\nAlice,F,\nBob,Z,\n")

    with pytest.raises(ValueError):
        read_students_from_csv(str(csv_file))


# Test cases for calculate_group_sizes function
def test_calculate_group_sizes():
    assert calculate_group_sizes(10, 4, 6) == [5, 5]
    assert calculate_group_sizes(11, 4, 6) == [6, 5]
    assert calculate_group_sizes(12, 4, 6) == [4, 4, 4]
    assert calculate_group_sizes(13, 4, 6) == [5, 4, 4]
    assert calculate_group_sizes(14, 4, 6) == [5, 5, 4]
    assert calculate_group_sizes(15, 4, 6) == [5, 5, 5]
    assert calculate_group_sizes(16, 4, 6) == [4, 4, 4, 4]
    assert calculate_group_sizes(17, 4, 6) == [5, 4, 4, 4]
    assert calculate_group_sizes(18, 4, 6) == [5, 5, 4, 4]


def test_calculate_group_sizes_edge_cases():
    assert calculate_group_sizes(4, 4, 6) == [4]
    assert calculate_group_sizes(5, 4, 6) == [5]
    assert calculate_group_sizes(6, 4, 6) == [6]
    assert calculate_group_sizes(7, 4, 6) == [4, 3]
    assert calculate_group_sizes(8, 4, 6) == [4, 4]


def test_calculate_group_sizes_invalid_cases():
    with pytest.raises(ValueError):
        calculate_group_sizes(0, 4, 3)  # no students
    with pytest.raises(ValueError):
        calculate_group_sizes(10, 4, 3)  # max < min
    with pytest.raises(ValueError):
        calculate_group_sizes(10, 4, 4)  # max == min
    with pytest.raises(ValueError):
        calculate_group_sizes(3, 4, 6)  # students < min


# Test cases for new_groups function
def test_new_groups():
    students = [Student("Alice"), Student("Bob"), Student("Charlie"), Student("Dylan")]
    group_sizes = [2, 2]
    groups = new_groups(students, group_sizes)
    assert len(groups) == 2
    assert len(groups[0].students) == 2
    assert len(groups[1].students) == 2


def test_new_groups_with_remaining_students():
    students = [
        Student("Alice"),
        Student("Bob"),
        Student("Charlie"),
        Student("Dylan"),
        Student("Eli"),
    ]
    group_sizes = [3, 2]
    groups = new_groups(students, group_sizes)
    assert len(groups) == 2
    assert len(groups[0].students) == 3
    assert len(groups[1].students) == 2


# Test cases for score_groups function
def test_score_groups():
    students = [
        Student("Alice", "F"),
        Student("Bob", "M"),
        Student("Charlie", "F"),
        Student("Dylan", "M"),
    ]
    group_sizes = [2, 2]
    groups = new_groups(students, group_sizes)
    score = score_groups(groups)
    assert isinstance(score, float)


def test_score_groups_edge_cases():
    students = [
        Student("Alice", "F"),
        Student("Bob", "M"),
        Student("Charlie", "F"),
        Student("Dylan", "M"),
    ]
    group_sizes = [4]
    groups = new_groups(students, group_sizes)
    score = score_groups(groups)
    assert score == 0  # Perfect ratio

    students = [
        Student("Alice", "F"),
        Student("Bob", "F"),
        Student("Charlie", "F"),
        Student("Dylan", "F"),
    ]
    group_sizes = [4]
    groups = new_groups(students, group_sizes)
    score = score_groups(groups)
    assert score < 0  # All same gender, should be penalized


# Test case for save_groups_to_csv function
def test_save_groups_to_csv(tmp_path):
    students = [
        Student("Alice", "F"),
        Student("Bob", "M"),
        Student("Charlie", "F"),
        Student("Dylan", "M"),
    ]
    group_sizes = [2, 2]
    groups = new_groups(students, group_sizes)

    csv_file = tmp_path / "new_groups.csv"
    save_groups_to_csv(groups, str(csv_file))

    # Read the CSV file and check its contents
    with open(csv_file, "r") as file:
        lines = file.readlines()
        assert lines[0].strip() == "Group ID,Student Name,Gender"
        assert len(lines) == 5  # Header + 4 students


# Test case for save_students_to_csv function
def test_save_students_to_csv(tmp_path):
    students = [
        Student("Alice", "F"),
        Student("Bob", "M"),
        Student("Charlie", "F"),
        Student("Dylan", "M"),
    ]

    csv_file = tmp_path / "new_students.csv"
    save_students_to_csv(students, str(csv_file))

    # Read the CSV file and check its contents
    with open(csv_file, "r") as file:
        lines = file.readlines()
        assert lines[0].strip() == "name,gender,seen_students"
        assert len(lines) == 5  # Header + 4 students


# Test case for update_seen_students function
def test_update_seen_students():
    students = [
        Student("Alice", "F"),
        Student("Bob", "M"),
        Student("Charlie", "F"),
        Student("Dylan", "M"),
    ]
    group_sizes = [2, 2]
    groups = new_groups(students, group_sizes)

    update_seen_students(groups)

    # Check that each student has seen the other students in their group
    for group in groups:
        for student in group.students:
            for other_student in group.students:
                if student != other_student:
                    assert other_student.name in student.seen_students

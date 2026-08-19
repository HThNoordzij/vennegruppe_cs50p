import argparse
import sys
import csv

## input must contain csv with students, initially only name and gender column, seen_students will be added when groups are created
## other inputs like previous groups? or min/max number of kids per group?
## student (name, gender and previous seen students)
## group (id, students, max students, min students, boy/girl ratio)
## implement some scoring mechanism based on previous seen students and boy/girl ratio
## recursion of scoring x times, keep best scoring groups


class Student:
    id = 0

    def __init__(self, name, gender=None):
        self.id = Student.id
        Student.id += 1
        self.name = name
        self.gender = gender
        self.seen_students = {}

    def __str__(self):
        return f"{self.name} ({self.id})"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Missing name")
        self._name = name

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if gender not in (None, "M", "F", "X"):
            raise ValueError("Gender must be 'M', 'F', 'X', or None")
        self._gender = gender


class Group:
    id = 0

    def __init__(self, max_students=6, min_students=4, ratio=0):
        self.id = Group.id
        Group.id += 1
        self.max_students = max_students
        self.min_students = min_students
        self.ratio = ratio
        self.students = []

    def __str__(self):
        return f"Group {self.id}: {', '.join([str(s) for s in self.students])}"

    @property
    def max_students(self):
        return self._max_students

    @max_students.setter
    def max_students(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Maximum number of students must be a positive integer")
        self._max_students = value

    @property
    def min_students(self):
        return self._min_students

    @min_students.setter
    def min_students(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Minimum number of students must be a positive integer")
        self._min_students = value

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Ratio must be between 0 and 1")
        self._ratio = value


def main(file, min_students, max_students):
    print(f"Arguments received. File: {file}, Min: {min_students}, Max: {max_students}")
    students = read_students_from_csv(file)
    print(f"Read {len(students)} students from {file}")


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        prog="Vennegruppe",
        description="Create new groups of students based on previous groups and other parameters",
    )

    parser.add_argument("-f", "--file")
    parser.add_argument(
        "-m",
        "--min",
        type=int,
        default=4,
        choices=range(2, 20),
        help="Minimum number of students per group",
    )
    parser.add_argument(
        "-M",
        "--max",
        type=int,
        default=6,
        choices=range(2, 20),
        help="Maximum number of students per group",
    )
    return parser.parse_args(args)


def read_students_from_csv(file_path):
    students = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(Student(name=row["name"], gender=row["gender"]))
    return students


def new_groups(names): ...


def score_groups(old, new): ...


if __name__ == "__main__":
    arguments = parse_arguments(sys.argv[1:])
    main(arguments.file, arguments.min, arguments.max)

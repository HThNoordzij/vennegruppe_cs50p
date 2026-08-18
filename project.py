import argparse

## implement OOP
## input must contain csv with students
## other inputs like previous groups? or min/max number of kids per group?
## student (name, grade, current group and previous seen students)
## group (id, students, max students, min students, boy/girl ratio)
## implement some scoring mechanism based on previous seen students and boy/girl ratio
## recursion of scoring x times, keep best scoring groups


class Student:
    id = 0

    def __init__(self, name):
        self.id = Student.id
        Student.id += 1
        self.name = name

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


class Group:
    id = 0

    def __init__(self, max_students=6, min_students=4):
        self.id = Group.id
        Group.id += 1
        self.max_students = max_students
        self.min_students = min_students
        self.students = []

    def __str__(self):
        return f"Group {self.id}: {', '.join([str(s) for s in self.students])}"


def main():
    parser = argparse.ArgumentParser(
        prog="Vennegruppe",
        description="Create new groups of students based on previous groups and other parameters",
    )

    parser.add_argument("-f", "--file")
    parser.add_argument(
        "-m", "--min", type=int, default=4, help="Minimum number of students per group"
    )
    parser.add_argument(
        "-M", "--max", type=int, default=6, help="Maximum number of students per group"
    )
    args = parser.parse_args()
    print(args.file)


def new_groups(names): ...


def score_groups(old, new): ...


if __name__ == "__main__":
    main()

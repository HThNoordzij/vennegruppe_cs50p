import argparse
import csv
import random
import sys


## create new groups based on previous groups and other parameters
## implement some scoring mechanism based on previous seen students and boy/girl ratio
## recursion of scoring x times, keep best scoring groups


class Student:
    """
    A class to represent a student.

    Attributes
    ----------
        id :int
            Unique identifier for the student.
        name : str
            Name of the student.
        gender : str
            Gender of the student, can be 'M', 'F', 'X', or None.
        seen_students : dict
            A dictionary to track how many times the student has seen other students.
    """

    id = 1

    def __init__(self, name, gender=None, seen_students=None):
        self.id = Student.id
        Student.id += 1
        self.name = name
        self.gender = gender
        self.seen_students = seen_students if seen_students is not None else {}

    def __str__(self):
        return f"{self.name} ({self.gender})"

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
    """
    A class to represent a group of students.

    Attributes
    ----------
        id : int
            Unique identifier for the group.
        ratio : float
            Optional gender ratio for the group.
        students : list
            List of Student objects in the group.
    """

    id = 1

    def __init__(self, ratio=0):
        self.id = Group.id
        Group.id += 1
        self.ratio = ratio
        self.students = []

    def __str__(self):
        return f"Group {self.id}: {', '.join([str(s) for s in self.students])}"

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Ratio must be between 0 and 1")
        self._ratio = value


def main(file, min_students, max_students):

    """Read and parse students."""
    print(f"Arguments received. File: {file}, Min: {min_students}, Max: {max_students}")
    students = read_students_from_csv(file)
    print(f"Read {len(students)} students from {file}")

    """Calculate group sizes."""
    group_sizes = calculate_group_sizes(len(students), min_students, max_students)
    print(f"Number of groups: {len(group_sizes)}")
    print(f"Group sizes: {group_sizes}")

    """Create new groups."""
    groups = new_groups(students, group_sizes)
    print(f"Created {len(groups)} groups:")
    for group in groups:
        print(group)


def parse_arguments(args):
    """Parses command-line arguments."""
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
    """Reads students from a CSV file and returns a list of Student objects."""
    students = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            students.append(
                Student(
                    name=row["name"],
                    gender=row["gender"],
                    seen_students=row["seen_students"],
                )
            )
    return students


def new_groups(students, group_sizes): 
    """Creates new groups of students based on the provided group sizes."""
    random.shuffle(students)
    groups = []
    index = 0
    for size in group_sizes:
        group = Group()
        group.students = students[index : index + size]
        groups.append(group)
        index += size
    return groups


def score_groups(old, new): ...


def calculate_group_sizes(n_students, min, max):
    """Calculates the sizes of groups based on the number of students and min/max constraints."""
    if max <= min:
        raise ValueError(
            "Maximum cannot be less than or equal to minimum number of students per group."
        )
    if n_students < min:
        raise ValueError(
            "Number of students cannot be less than the minimum number of students per group."
        )

    num_groups = n_students // min
    group_size = n_students // num_groups

    if group_size > max:
        num_groups += 1
        group_size = n_students // num_groups

    groups = [group_size] * num_groups
    remaining_students = n_students % num_groups

    for i in range(remaining_students):
        groups[i] += 1

    return groups


if __name__ == "__main__":
    arguments = parse_arguments(sys.argv[1:])
    main(arguments.file, arguments.min, arguments.max)

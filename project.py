import argparse
import csv
from hashlib import new
import random
import sys


## create new groups based on previous groups and other parameters
## implement some scoring mechanism based on previous seen students and boy/girl ratio


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
        seen_students : list
            A list to track the students that the student has seen.
    """

    id = 1

    def __init__(self, name, gender=None, seen_students=None):
        self.id = Student.id
        Student.id += 1
        self.name = name
        self.gender = gender
        self.seen_students = seen_students if seen_students is not None else []

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

    def add_seen_student(self, student_name):
        """Adds a student to the seen_students list."""
        self.seen_students.append(student_name)


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

    def __init__(self, students=[], ratio=0):
        self.id = Group.id
        Group.id += 1
        self.students = students
        self.ratio = ratio

    def __str__(self):
        return f"Group {self.id}, ratio: {self.ratio:.2f}: {', '.join([str(s) for s in self.students])}"

    @property
    def students(self):
        return self._students

    @students.setter
    def students(self, students):
        if not isinstance(students, list):
            raise ValueError("Students must be a list")
        self._students = students
        self._ratio = self.calculate_ratio()

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError("Ratio must be between 0 and 1")
        self._ratio = value

    def calculate_ratio(self):
        """Calculates the gender ratio of the group."""
        if not self.students:
            return 0
        female_count = sum(1 for s in self.students if s.gender == "F")
        male_count = sum(1 for s in self.students if s.gender == "M")
        total_count = female_count + male_count
        return female_count / total_count if total_count > 0 else 0


def main(file, iterations, min_students, max_students, output_file, students_file):
    """Opening message."""
    print(
        f"Start creating vennegrupper.\n\nFile with students: {file} \
            \nMinimum number of students per group: {min_students} \
            \nMaximum number of students per group: {max_students} \
            \nNumber of iterations: {iterations} \
            \nOutput file for new groups: {output_file} \
            \nOutput file for updated students: {students_file}\n"
    )

    """Read and parse students."""
    students = read_students_from_csv(file)
    print(f"Read {len(students)} students from {file}")

    """Calculate group sizes."""
    group_sizes = calculate_group_sizes(len(students), min_students, max_students)
    print(f"Number of groups: {len(group_sizes)}")
    print(f"Group sizes: {group_sizes}\n")

    """Recursively create and score groups, keeping the best scoring groups."""
    best_groups = None
    best_score = float("-inf")
    for _ in range(iterations):
        groups = new_groups(students, group_sizes)
        score = score_groups(groups)
        if score > best_score:
            print(f"New best score: {score:.2f}")
            best_score = score
            best_groups = groups

    print(f"\nBest score after {iterations} iterations: {best_score:.2f}\n")
    print(f"Best groups:")
    for group in best_groups:
        print(group)

    """Update seen students."""
    update_seen_students(best_groups)
    print("\nUpdated 'seen_students' for each student.")

    """Save groups to CSV."""
    save_groups_to_csv(best_groups, output_file)
    print(f"\nSaved groups to {output_file}")

    """Save students to CSV."""
    save_students_to_csv(sorted(students, key=lambda x: x.name), students_file)
    print(f"Saved students to {students_file}")

    print("\nVennegrupper created successfully!")


def parse_arguments(args):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="Vennegruppe",
        description="Create new groups of students based on previous groups and other parameters",
    )

    parser.add_argument("-f", "--file")
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=100,
        help="Number of iterations for group creation and scoring",
    )
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
    parser.add_argument(
        "-o",
        "--output",
        default="new_groups.csv",
        help="Output CSV file for new groups",
    )
    parser.add_argument(
        "-s",
        "--students",
        default="new_students.csv",
        help="Output CSV file for new students",
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
                    seen_students=(
                        row["seen_students"].split(",")
                        if row["seen_students"]
                        else None
                    ),
                )
            )
    return students


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


def score_groups(groups):
    """Score new groups based on gender ratio."""
    ratio_score = 0
    for group in groups:
        if group.ratio < 0.2 or group.ratio > 0.8:
            ratio_score -= 2
        elif group.ratio < 0.3 or group.ratio > 0.7:
            ratio_score -= 1
        elif group.ratio < 0.4 or group.ratio > 0.6:
            ratio_score -= 0.5
    ratio_score = ratio_score / len(groups) if groups else 0

    """Score new groups based on how many students have seen each other before."""
    seen_score = 0
    for group in groups:
        for student in group.students:
            seen_score -= len(
                [s for s in group.students if s.name in student.seen_students]
            )
    return ratio_score + seen_score


def update_seen_students(new):
    """Updates the seen_students attribute for each student in the new groups."""
    for group in new:
        for student in group.students:
            for other_student in group.students:
                if student != other_student:
                    student.add_seen_student(other_student.name)


def save_groups_to_csv(groups, file_path):
    """Saves the groups to a CSV file."""
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Group ID", "Student Name", "Gender"])
        for group in groups:
            for student in group.students:
                writer.writerow([group.id, student.name, student.gender])


def save_students_to_csv(students, file_path):
    """Saves the students to a CSV file."""
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "gender", "seen_students"])
        for student in students:
            writer.writerow(
                [student.name, student.gender, ",".join(student.seen_students)]
            )


if __name__ == "__main__":
    arguments = parse_arguments(sys.argv[1:])
    main(
        arguments.file,
        arguments.iterations,
        arguments.min,
        arguments.max,
        arguments.output,
        arguments.students,
    )

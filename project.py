import argparse
import csv
import random
import sys
import logging

logger = logging.getLogger(__name__)


class Student:
    """
    A class to represent a student.

    Attributes
    ----------
    id : int
        Unique identifier for the student.
    name : str
        Name of the student.
    gender : str
        Gender of the student, can be 'M', 'F', 'X', or None.
    seen_students : list
        A list to track the students that the student has seen.

    Methods
    -------
    add_seen_student(student_name)
        Appends the student name to the list of seen_students
    """

    _next_id = 1

    def __init__(self, name, gender=None, seen_students=None):
        self.id = Student._next_id
        Student._next_id += 1
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
    students : list
        List of Student objects in the group.

    Properties
    ---------
    ratio : float
        Gender ratio of the group (F/M), ignoring X and None.
    """

    _next_id = 1

    def __init__(self, students=[]):
        self.id = Group._next_id
        Group._next_id += 1
        self.students = students

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
        self._ratio = self._calculate_ratio()

    @property
    def ratio(self):
        return self._ratio

    def _calculate_ratio(self):
        """Calculates the gender ratio of the group."""
        if not self.students:
            return 0
        female_count = sum(1 for s in self.students if s.gender == "F")
        male_count = sum(1 for s in self.students if s.gender == "M")
        total_count = female_count + male_count
        return female_count / total_count if total_count > 0 else 0


def main(file, iterations, min_students, max_students, output_file, students_file):
    """Opening message."""
    logging.basicConfig(
        filename="vennegruppe.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger.info(
        f"Start creating vennegrupper.\n\nFile with students: {file} \
            \nMinimum number of students per group: {min_students} \
            \nMaximum number of students per group: {max_students} \
            \nNumber of iterations: {iterations} \
            \nOutput file for new groups: {output_file} \
            \nOutput file for updated students: {students_file}\n"
    )

    """Read and parse students."""
    students = read_students_from_csv(file)
    logger.info(f"Read {len(students)} students from {file}")

    """Calculate group sizes."""
    group_sizes = calculate_group_sizes(len(students), min_students, max_students)
    logger.info(f"Number of groups: {len(group_sizes)}")
    logger.info(f"Group sizes: {group_sizes}\n")

    """Iteratively create and score groups, keeping the best scoring groups."""
    logger.info(f"Randomizing the order of students, creating unique groups.\n")

    logger.info("Scoring the girl/boy ratio per group.")
    logger.info("-2 points when ratio is less than 20/80.")
    logger.info("-1 points when ratio is less than 30/70.")
    logger.info("-0.5 points when ratio is less than 40/60.\n")

    logger.info("Scoring groups based on previous seen students within one group.")
    logger.info(
        "-1 point per previously seen student (aka -2, since it goes both ways).\n"
    )

    best_groups = None
    best_score = float("-inf")
    for _ in range(iterations):
        groups = create_new_groups(students, group_sizes)
        score = score_groups(groups)
        if score > best_score:
            logger.info(f"New best score: {score:.2f}")
            best_score = score
            best_groups = groups

    logger.info(f"Best score after {iterations} iterations: {best_score:.2f}\n")
    logger.info(f"Best groups:")
    for group in best_groups:
        logger.info(group)

    """Update seen students."""
    update_seen_students(best_groups)
    logger.info("Updated 'seen_students' for each student.")

    """Save groups to CSV."""
    save_groups_to_csv(best_groups, output_file)
    logger.info(f"Saved groups to {output_file}")

    """Save students to CSV."""
    save_students_to_csv(sorted(students, key=lambda x: x.name), students_file)
    logger.info(f"Saved students to {students_file}")

    logger.info("Vennegrupper created successfully!")


def parse_arguments(args):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="Vennegruppe",
        description="Create new groups of students based on previous groups and other parameters",
    )

    parser.add_argument(
        "-f",
        "--file",
        help="Input CSV file with students (name, gender, seen_students)",
        required=True,
    )
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
        help="Output CSV file for updated students",
    )
    return parser.parse_args(args)


def read_students_from_csv(file_path):
    """Reads students from a CSV file and returns a list of Student objects.

    Parameters
    ----------
    file_path : str
        Path to the csv file with students
        Should contain the columns:
            name : str
            gender : F, M, X, or None
            seen_students : empty or comma seperated list of names

    Returns
    -------
    list
        Containing Student objects
    """

    students = []
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        logger.info(f"Reading students from {file_path}")
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
    """Calculates the sizes of groups based on the number of students and min/max constraints.

    Parameters
    ----------
    n_students : int
        Total number of students that need to be divided into groups
    min : int
        Minimum number of students per full group
    max : int
        Maximum number of students per group

    Returns
    -------
    list
        An entry per group to be made, with an integer representing the group size

    Raises
    ------
    ValueError
        When the max is equal or smaller than the min parameter for group sizes
        When the n_students is smaller than the min size of a group

    Notes
    -----
    The algorithm attemps to create groups such that each group has size
    at least `min`, but there are combinations of parameters that can
    result in some groups being smaller than `min`. For example,
    calculate_group_sizes(7, 4, 6) will output [4, 3].
    """

    if max <= min:
        raise ValueError(
            "Maximum cannot be less than or equal to minimum number of students per group."
        )
    if n_students < min:
        raise ValueError(
            "Number of students cannot be less than the minimum number of students per group."
        )

    logger.info(
        f"Calculating group sizes for {n_students} students, with {min} - {max} per group."
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


def create_new_groups(students, group_sizes):
    """Creates new groups of students based on the provided group sizes.

    Parameters
    ----------
    students : list
        List of Student objects
    group_sizes : list
        List of integer values. Each entry corresponds to a group to be
        created and each entry's integer value will be the corresponding
        group's size.

    Returns
    -------
    list
        Containing Group objects
        The Group objects are filled with Student objects
    """

    random.shuffle(students)
    groups = []
    index_start = 0
    for size in group_sizes:
        group = Group()
        group.students = students[index_start : index_start + size]
        groups.append(group)
        index_start += size
    return groups


def score_groups(groups):
    """Score new groups based on gender ratio.

    Parameters
    ----------
    groups : list
        List of Group objects containing Student objects

    Returns
    -------
    float
        Representing the total score of the groups made, based on
            The average female / male ratio of the groups
            The number of students that have been grouped together before
    """

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


def update_seen_students(groups):
    """Updates the seen_students attribute for each student in the groups.

    Parameters
    ----------
    groups : list
        List of Group objects containing Student objects

    Returns
    -------
    None
    """

    logger.info(
        "Add current group members to 'seen_student' attribute for each Student."
    )

    for group in groups:
        for student in group.students:
            for other_student in group.students:
                if student != other_student:
                    student.add_seen_student(other_student.name)


def save_groups_to_csv(groups, file_path):
    """Saves the groups to a CSV file.

    Parameters
    ----------
    groups : list
        List of Group objects containing Students objects
    file_path : str
        Path to the csv file for new groups (will be created or overwritten)

    Returns
    -------
    None
    """

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Group ID", "Student Name", "Gender"])
        for group in groups:
            for student in group.students:
                writer.writerow([group.id, student.name, student.gender])


def save_students_to_csv(students, file_path):
    """Saves the students to a CSV file.

    Parameters
    ----------
    students : list
        List of Students objects
    file_path : str
        Path to the csv file for updated students (will be created or overwritten)

    Returns
    -------
    None
    """

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

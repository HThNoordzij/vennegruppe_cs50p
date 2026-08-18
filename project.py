import argparse

## implement OOP
## input must contain csv with students
## other inputs like previous groups? or min/max number of kids per group?
## student (name, grade, current group and previous seen students)
## group (id, students, max students, min students, boy/girl ratio)
## implement some scoring mechanism based on previous seen students and boy/girl ratio
## recursion of scoring x times, keep best scoring groups

parser = argparse.ArgumentParser(
                    prog='Vennegruppe',
                    description='Create new groups of students based on previous groups and other parameters')

parser.add_argument('-f', '--file') 
parser.add_argument('-m', '--min', type=int, default=4, help='Minimum number of students per group') 
parser.add_argument('-M', '--max', type=int, default=6, help='Maximum number of students per group')
args = parser.parse_args()


class Student:
    ...


class Group:
    ...

def main():
    print(args.file)


def new_groups(names):
    ...


def score_groups(old, new):
    ...


if __name__ == "__main__":
    main()

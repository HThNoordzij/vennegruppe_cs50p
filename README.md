# Vennegruppe

By Hanna Noordzij

#### Description:
A python script to create new friend groups (vennegruppe).

The concept “vennegruppe” is part of the anti-bullying program in Norway. The children are divided into groups of 4-5 children twice a year. The group is invited into the homes of the group members over the course of the semester. The children will be better acquainted with each other, as well as their parents and homes. This usually results in less bullying within and outside the classroom.

This script creates (new) groups. Creating these groups manually so that every child will meet all the other classmates in the course of seven years is quite difficult. The script should make it easier to create these groups, with less instances of meeting the same child in the group over and over again.

#### Get Started:

The program requires a csv file containing the students that will be grouped. The csv file should contain the columns, "name", "gender", and "seen_students". The last column can be empty or contain a list of comma seperated names of students they already met in previous groups.

The student file is provided after the "-f" or "--file". The program can be used as follows:

    python project.py -f students.csv

In case of unclarity, run:

    python project.py -h

By default, the program creates a 100 new groups and keeps the best scoring group, based on an even girl/boy ratio and most novelty within the groups. However, iterating 10000 will create better groups:

    python project.py -f students.csv -i 10000

In addition, the group size can be set using -m (--min) and -M (--max), and the output files for the groups (-o) and updated students (-s). See:

### (Optional) Arguments
-  -h, --help                       Show this help message and exit
-  -f, --file FILE                  Input CSV file with students (name, gender, seen_students)
-  -i, --iterations ITERATIONS      Number of iterations for group creation and scoring
-  -m, --min {2-19}                 Minimum number of students per group
-  -M, --max {2-19}                 Maximum number of students per group
-  -o, --output OUTPUT              Output CSV file for new groups
-  -s, --students STUDENTS          Output CSV file for updated students

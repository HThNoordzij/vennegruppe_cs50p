# Vennegruppe

By Hanna Noordzij

#### Description:
A Python script to create new friend groups (vennegruppe). 

The concept “vennegruppe” is part of the anti-bullying program in Norway. The children are divided into groups of 4-5 children twice a year. The group is invited into the homes of the group members over the course of the semester. The children will be better acquainted with each other, as well as their parents and homes. This usually results in less bullying within and outside the classroom. 

This script creates (new) groups. Creating these groups manually, so that every child will meet all the other classmates in the course of seven years, is quite challenging. The script should make it easier to create these groups, with less instances of meeting the same child in the group over and over again. 


###### Student input
A *student.csv* file is taken as input, with the ***columns*** **name**, **gender** and **seen_students**. The student's **name** should be unique for the algorithm to work optimally, for example by adding the last name of the student. The **gender** of the student can be either F, M, X, or empty, whereby only F and M are used to calculate the girl/boy ratio within each group. The **seen_students** column can be empty or contain a comma separated list of other names the student has been in a group with previously.


###### Creating groups
The program creates 100 groups and stores the best scoring group. The generated groups are written to the *new_groups.csv* file, with the columns **Group ID**, **Student Name**, and **Gender**. The students **seen_students** is updated and written to the *new_students.csv* file. The new_students.csv file can be used as the input file for the program to create new groups.


###### Scoring algorithm
The algorithm for scoring the groups is based on the girl/boy ratio of the groups and how many students within a group have already been group mates before. The goal is to have mixed groups; however, more skewed groups towards one gender are more heavily penalized than semi-mixed groups. If one is not interested in the girl/boy ratio of the groups, the gender in the students' file can be specified as "X" or "None".

When groups are made whereby the students have already been divided into groups before, meeting the same student within the new groups is penalized. The more groups that are made where students meet each other again, the lower the score. That is why the program creates 100 groups, increasing the quality of the grouping by keeping the highest scoring division. However, iterating the process of group creation 100 times is relatively little, so the user should increase the iteration to 10.000 or more for better quality groups.


###### Other use cases
Although the anti-bullying program in Norway usually creates groups of 4-5 children, the mechanism of making groups can be applied to many arenas, for school trips, university introduction weeks or team building at work. Therefore, the program includes parameters to adapt the default settings of the group sizes to range somewhere between 2 to 20 members. See "Get Started" and "(Optional) Parameters", where these and other parameters are explained.


#### Get Started:

The program requires a csv file containing the students that will be grouped. The csv file should contain the columns; "name", "gender", and "seen_students". The last column can be empty or contain a list of comma separated names of students they already met in previous groups. The name of the students should be unique, for example by adding (the first letter of) their last name.


The student file is provided after the "-f" or "--file". The program can be used as follows:

    python project.py -f students.csv


In case of unclarity, run:

    python project.py -h


By default, the program creates 100 new groups and keeps the best scoring group, based on an even girl/boy ratio and most novelty within the groups. However, iterating 10000 will create better groups than the default 100, and can be set as follows:

    python project.py -f students.csv -i 10000


In addition, the group size can be changed using -m (--min) and -M (--max), and the output files for the groups (-o) and updated students (-s) can be added. See:


### (Optional) Parameters
-  -h, --help                       Show this help message and exit
-  -f, --file FILE                  Input CSV file with students (name, gender, seen_students)
-  -i, --iterations ITERATIONS      Number of iterations for group creation and scoring
-  -m, --min {2-19}                 Minimum number of students per group
-  -M, --max {2-19}                 Maximum number of students per group
-  -o, --output OUTPUT              Output CSV file for new groups
-  -s, --students STUDENTS          Output CSV file for updated students

"""
HELLO
THIS PROGRAM WILL NEED SLOT WISE TABLE OF STUDENTS (THE TABLE SHOULD CONTAIN 2 COLUMNS; FIRST COLUMN BEING THE STUDENTS ENROLLMENT ID AND THE SECOND COLUMN BEING THE COURSE ID)
I HAVE ALREADY INCLUDED LHC CLASSROOM FILE WHICH CONTAINS INFORMATION ABOUT LHC CLASSROOMS AND THEIR CAPACITY DURING EXAMS
THIS PROGRAM WILL RETURN TABLES OF LHC ROOMS WITH SHIFT.NO INCLUDED ; WHICH WILL CONATAIN INFORMATION REGARDING THE STUDENTS AND ASSIGNED SEAT NO.

"""
print("Generating Files...")
#--------------------------------------Importing Libraries
import os
import csv
import math
import random
import pandas as pd
cwd = os.getcwd() # gives current Working Directory
slot = 'B' #Slot of the Exam
path = cwd+f'\{slot} slot exams'
try:
    os.mkdir(path)
except:
    pass
#--------------------------------------------------------------LHC rooms
folder_path = r'seating' #Add the target folder of LHC rooms
list_of_files = os.listdir(folder_path)
lhc_rooms=[] #It is a list of list which will contain the lhc room number, its file path and its total capacity(in order as mentioned)
available_seat=0
for files in list_of_files:
    q = open(f"{folder_path}\{files}")
    room=[files[:5],f"{folder_path}\{files}",(len(q.readlines()))//2]
    lhc_rooms.append(room)
    available_seat+=room[2]
#Will return the total number of seats in LHC
#Seats that can be used 
lhc_rooms.sort(key= lambda x:x[2])
lhc_rooms.reverse()
# print(lhc_rooms)
#--------------------------------------------------------------
#!!!--Assiging Courses according to its students and student strength---!!!
student_file = open("slot_course_details.csv","r") #Input File
reader = csv.reader(student_file)
student_data = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
Course = []
for row in reader:
    student_data.append([row[0],row[1]])
    Course.append(row[1])
student_data = student_data[1:]
Course = Course[1:]
# print(student_data)
# print(Course)
# -----------------------------------------------Making Student Data A dict
student_data_dct = {}
for sub in student_data:
    student_data_dct[sub[0]] = sub[1]
# print(student_data_dct)
# ---------------------------------------------
total_students= len(student_data) #It contains the total number of students in that slot
total_shifts = math.ceil(total_students/available_seat) #It contains the total number of shifts required for that particular slot
unique_courses= list(set(Course))
course_students={}#Is a dictionary containing unique courses and students enrolled in that course
qe = []
for i in range(len(unique_courses)):
    ls = [unique_courses[i],Course.count(unique_courses[i])]
    qe.append(ls)
    students=[]
    for j in range(len(student_data)):
        if student_data[j][1]==unique_courses[i]:
            students.append(student_data[j][0])
    course_students[unique_courses[i]]=students
unique_courses = qe
unique_courses.sort(key=lambda x: x[1]) #It is a list of list in which the inner list contains the data regarding the course ID and Total Number of students enrolled in that course
student_file.close()
# print(unique_courses)
# print(course_students)
#-------------------------------------------------------------------------------
#----------------------------------MAKING DOCUMENTs FOR EACH SHIFT--------------------------------------------------

i1 = len(unique_courses)-1 #A pointer for unique courses starting with courses having maximum capacity.
for j in range(total_shifts):
    shift_no = j+1
    path1 = path+f'\{shift_no} Shift'
    try:
        os.mkdir(path1)
    except:
        pass
    rough_students_each_shift = total_students//total_shifts
    actual_students = 0
    courses_in_shift = []
    while actual_students<=rough_students_each_shift and i1>=0:
        actual_students+=unique_courses[i1][1]
        courses_in_shift.append(unique_courses[i1][0])
        i1-=1
    lhc_rooms_seats={} #seat number dictionary
    seats_filled = {} #It is a dictionary where the keys are the lHC numbers and the value is a binary list where ith index denotes if the ith seat has been filled or not
    total_seats = 0 #Stores the total number of seats in all the LHCs combined
    for rooms in lhc_rooms:
        room = rooms[0]
        room_path = rooms[1]
        q1 = open(room_path)
        seats = q1.read().splitlines()
        actual_seats = []
        for seat in seats:
            if int(seat[1:])%2==1:
                actual_seats.append(seat)
        lhc_rooms_seats[room]=actual_seats
        seats_filled[room]=[0]*(len(actual_seats))
        total_seats += len(actual_seats)
    # print(total_seats)
    # print(lhc_rooms_seats)
    # print(seats_filled)
    par = 1 #a parity variable which will change with each course
    lhc_room_numbers = list(lhc_rooms_seats.keys())
    #Above variable contains list of all LHC room numbers
    seats_linear = [0]*total_seats
    even = 0
    odd = 1
    for course_name in courses_in_shift:
        student_numbers = course_students[course_name] #Has enrollment ID of the Students
        random.shuffle(student_numbers)
        j = 0
        
        if par==1:
            while j<len(student_numbers) and (even<total_seats):
                seats_linear[even] = student_numbers[j]
                j+=1
                even+=2
        else:
            while j<len(student_numbers) and odd<total_seats:
                seats_linear[odd] = student_numbers[j]
                j+=1
                odd+=2
        par*=-1
    #Seats linear filled now we will fill the dictionary seats_:filled
    ind = 0 # A variable acting as a pointer to itearte through seats_linear
    for m in range(len(lhc_room_numbers)):
        lh_room = lhc_room_numbers[m]
        seats_in_room = len(seats_filled[lh_room])
        l = 0 #A pointer
        while l<seats_in_room:
            seats_filled[lh_room][l] = seats_linear[ind]
            ind+=1
            l+=1

    #-----------------------------------------Now making documents for each shift
   
    for k in range(len(lhc_room_numbers)):
        lhc_room = lhc_room_numbers[k]
        seats_filled_in_room = seats_filled[lhc_room]
        seats_number = lhc_rooms_seats[lhc_room]
        courses=[]
        k1 =[]
        k2 =[]
        for j1 in range(len(seats_filled_in_room)):
            if seats_filled_in_room[j1]!=0:
                k1.append(seats_filled_in_room[j1])
                k2.append(seats_number[j1])
                student_data_dct[seats_filled_in_room[j1]] = [student_data_dct[seats_filled_in_room[j1]],seats_number[j1],lhc_room,shift_no]
                
        seats_filled_in_room = k1
        seats_number = k2
        for i in seats_filled_in_room:
            try:
                courses.append(student_data_dct[i][0])
            except:
                courses.append("NIL")
        dct = {"Seat No":seats_number,"Enrollement_ID":seats_filled_in_room,"Course":courses}
        df = pd.DataFrame(dct)
        df.to_excel(f"{path1}\{lhc_room}_Shift.No.{shift_no}"+".xlsx",index=False)
    #-----------------------------------------------------------Now making Documents for each subject
    path2 = path+f'\ Courses'
    try:
        os.mkdir(path2)
    except:
        pass
    for k1 in range(len(unique_courses)):
        students_in_course = course_students[unique_courses[k1][0]]
        seat_number_of_student = []
        lh = []
        shift_nos =[]
        course_name=[]
        for m1 in students_in_course:
            seat_number_of_student.append(student_data_dct[m1][1])
            lh.append(student_data_dct[m1][2])
            shift_nos.append(student_data_dct[m1][3])
            course_name.append(student_data_dct[m1][0])
        dct1 ={"Enrollment Id":students_in_course,"Seat Number":seat_number_of_student,"LHC":lh,"Shift No":shift_nos,"Course":course_name}
        df2 = pd.DataFrame(dct1)
        df2.to_excel(f"{path2}\{unique_courses[k1][0],unique_courses[k1][1]}"+".xlsx",index=False)
print("Job Done!")
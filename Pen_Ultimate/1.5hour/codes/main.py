import pandas as pd
import numpy as np
import os
import random
import csv
def crs_stud(crs,slt):
    #Returns the total student from the course
    df = pd.read_excel("../Course_Data.xlsx")
    num=0
    for ind in df.index:
        if (df["Course Code"][ind])==crs:
            num=int(df["Register"][ind])
    return num
def lh_reader_indi():
    folder_path = "../seating" #Add the target folder of LHC rooms
    list_of_files = os.listdir(folder_path)
    lhc_rooms=[] #It is a list of list which will contain the lhc room number, its file path and its total capacity(in order as mentioned)
    available_seat=0
    for files in list_of_files:
        q = open(f"{folder_path}\{files}")
        seats = 0
        m= q.readlines()
        for k in m:
            if int(k[1:])%3==1:
                seats+=1
        room=[files[:5],f"{folder_path}\{files}",seats]
        lhc_rooms.append(room)
        available_seat+=room[2]
    lhc_rooms.sort(key= lambda x:x[2])
    lhc_rooms.reverse()
    return lhc_rooms #[[LH Name,file-Path,Total seats]]
def closest_students_to_n(courses, target_students):
    n = len(courses)
    courses.sort(key=lambda x: x[1])  # Sort courses based on capacity

    dp = [[0] * (target_students + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        course_name, course_capacity,course_slot = courses[i - 1]
        for j in range(1,target_students + 1):
            
            dp[i][j] = (dp[i - 1][j]) 
            if j >= course_capacity:
                dp[i][j]= max(dp[i][j],dp[i-1][j-course_capacity]+course_capacity)

    selected_courses = []
    i = n
    j = target_students
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            selected_courses.append(courses[i - 1])
            j -= courses[i - 1][1]
        i -= 1

    selected_courses.reverse()
    return selected_courses
def Slot_reader(Slot1):
    df = pd.read_excel("../Course_Data.xlsx")
    courses=[]
    for ind in df.index:
        if Slot1 == df["Slot Name"][ind] or (Slot1+"1" == str(df["Slot Name"][ind])  or (Slot1 +"2"== str(df["Slot Name"][ind]) )):
            courses.append([df["Course Code"][ind],int(df["Register"][ind]),df["Slot Name"][ind]])
    return courses
def schedule_reader():
    df = pd.read_excel("../Exam Schedule.xlsx")
    schedule = []
    k1 = df.columns
    for ind in df.index:
        dat=[]
        for col in k1:
            dat.append(str(df[col][ind]))
        schedule.append(dat)
    return schedule
def day_slots():
    df = pd.read_excel("../Exam Schedule.xlsx")
    k1 = df.columns
    return list(k1)
def conflicting_slots():
    folder_path = "..\Constraint 1"
    lfls = os.listdir(folder_path)
    slts = [] #Contains the slots which are conflicting 
    for files in lfls:
        slts.append([files[:-5],f"{folder_path}\{files}"])
    return slts
#Some Variables-------------------
available_seat=0
folder_path = "..\seating" #Add the target folder of LHC rooms
list_of_files = os.listdir(folder_path)
for files in list_of_files:
    q = open(f"{folder_path}\{files}")
    seats = 0
    m= q.readlines()
    for k in m:
        if int(k[1:])%2==1:
            seats+=1
    room=[files[:5],f"{folder_path}\{files}",seats]
    available_seat+=room[2]
#--LHC room Reader--------------------
def lh_reader():
    folder_path = "..\seating" #Add the target folder of LHC rooms
    list_of_files = os.listdir(folder_path)
    lhc_rooms=[] #It is a list of list which will contain the lhc room number, its file path and its total capacity(in order as mentioned)
    available_seat=0
    for files in list_of_files:
        q = open(f"{folder_path}\{files}")
        seats = 0
        m= q.readlines()
        for k in m:
            if int(k[1:])%2==1:
                seats+=1
        room=[files[:5],f"{folder_path}\{files}",seats]
        lhc_rooms.append(room)
        available_seat+=room[2]
    lhc_rooms.sort(key= lambda x:x[2])
    lhc_rooms.reverse()
    return lhc_rooms #[[LH Name,file-Path,Total seats]]
#--------------------
#Generator for a particular Day
def generator_day(req_day):
    # day = req_day[0]
    slot_courses={}
    slot_count={} #Number of shifts for each slot
    slots=set()
    for m in req_day[1:]:
        if str(m) == "nan":
            continue
        elif ("and" not in m):
            slots.add(m)
            try:
                slot_count[m]+=1
            except:
                slot_count[m]=1
        else:
            k1 = m.split()
            slots.add(k1[0])
            slots.add(k1[2])
            try:
                slot_count[k1[0]]+=1
            except:
                slot_count[k1[0]]=1
            try:
                slot_count[k1[2]]+=1
            except:
                slot_count[k1[2]]=1
    for slot in slots:
        slot_courses[slot]=Slot_reader(slot)
    slot_students_num={} #Total Number of students in that slot
    for j in slot_courses:
        k1 = slot_courses[j]
        num = 0
        for i in k1:
            num+=i[1]
        slot_students_num[j]=num
        num = 0
    shifts = req_day[1:]
    shifts.sort(key = lambda x:len(x))
    shifts.reverse()
    # print(shifts)
    shift_course={}#shift Courses for each dictionary [[course,slot]]
    for i2 in range(len(shifts)):
        shift_slt = shifts[i2]
        lst =[] #list of list of courses
        if shift_slt =="nan":
            shift_course[f"SHIFT--{i2+1}"]= lst
        elif "and" not in shift_slt:
            courses  = slot_courses[shift_slt]
            rough_students = int(slot_students_num[shift_slt])
            if slot_count[shift_slt]>1:
                rough_students = int(slot_students_num[shift_slt]//slot_count[shift_slt])
            req_courses = closest_students_to_n(list(courses),rough_students+20)
            for i1 in req_courses:
                courses.remove(i1)
            slot_courses[shift_slt]=courses
            for i3 in req_courses:
                lst.append([i3[0],i3[2]])
            shift_course[f"SHIFT--{i2+1}"]= lst
        else:
            slts = shift_slt.split()
            slt1 = slts[0]
            slt2 = slts[2]
            cnft_slt = conflicting_slots()
            fil_path=""
            for m2 in cnft_slt:
                if slt1 in m2[0]:
                    fil_path=m2[1]
                    break
            try:
                df1 = pd.read_excel(fil_path)
                conflt_courses = [] #[[course,course_slot]]
                col_nam = df1.columns
                for ind in df1.index:
                    ls = []
                    for col in col_nam:
                        ls.append(df1[col][ind])
                    conflt_courses.append(ls)
            except:
                conflt_courses=[]
            courseSlt1 = slot_courses[slt1]
            courseSlt2 = slot_courses[slt2]
            updated_courseSlt1 = courseSlt1[:]
            for m4 in conflt_courses:
                crs = m4[0]
                for j2 in range(len(updated_courseSlt1)):
                    if updated_courseSlt1[j2][0]==crs:
                        updated_courseSlt1.pop(j2)
                        break
            rough_students1 = int(slot_students_num[slt1])
            if slot_count[slt1]>1:
                rough_students1 = int(slot_students_num[slt1]//slot_count[slt1])
            rough_students2 = int(slot_students_num[slt2])
            if slot_count[slt2]>1:
                rough_students2 = int(slot_students_num[slt2]//slot_count[slt2])
            req_courses1 = closest_students_to_n(list(updated_courseSlt1),min(rough_students1,available_seat-rough_students2-20)+20)
            req_courses2 = closest_students_to_n(list(courseSlt2),rough_students2+20)
            for i1 in req_courses1:
                courseSlt1.remove(i1)
            slot_courses[slt1]=courseSlt1
            for i3 in req_courses1:
                lst.append([i3[0],i3[2]])
            for i1 in req_courses2:
                courseSlt2.remove(i1)
            slot_courses[slt2]=courseSlt2
            for i3 in req_courses2:
                lst.append([i3[0],i3[2]])
            shift_course[f"SHIFT--{i2+1}"]= lst
            #Complete this part and you are done..................... Done Actually
            #Great Now tomorrow check for shifts with course only
    return shift_course
# print(generator_day(schedule_reader()[0]))
#---------------------------------------------------------------------------------------------- Shift Dct Generator
# print((day_slots()))
# print(schedule_reader())
def shift_dct_generator(Slt, crslist,shift):
    if Slt=="nan":
        pass
    #--------------------
    elif "indi" == Slt:
        file_name = f"../SlotList/{Slt}.csv"
        student_file = open(file_name,"r") #Input File
        reader = csv.reader(student_file)
        student_data = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
        Course = []
        for row in reader:
            if [row[0],Slt] in crslist:
                student_data.append([row[1],row[0]])
                Course.append(row[0])
        student_data = student_data
        Course = Course
        student_file.close()
        #------------------Making a Student Data Dict
        student_data_dct = {}
        for sub in student_data:
            student_data_dct[sub[0]] = sub[1] #This student data dict contains all information for a particular student
         # ---------------------------------------------
        total_students = len(student_data)
        unique_courses= list(set(Course))
        course_students={}#Is a dictionary containing unique courses and students enrolled in that course as a list
        qe=[]
        for i in range(len(unique_courses)):
            ls = [unique_courses[i],Course.count(unique_courses[i])]
            qe.append(ls)
            students=[]
            for j in range(len(student_data)):
                if student_data[j][1]==unique_courses[i]:
                    students.append(student_data[j][0])
            course_students[unique_courses[i]]=students
        unique_courses = qe
        unique_courses.sort(key=lambda x: x[1])
        tot_stud = total_students
        #------------------------Making Document for the shift
        courses_in_shift = []
        for crs in crslist:
            courses_in_shift.append(crs[0])
        lhc_rooms = lh_reader_indi()
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
                if int(seat[1:])%3==1:
                    actual_seats.append(seat)
            lhc_rooms_seats[room]=actual_seats
            seats_filled[room]=[0]*(len(actual_seats))
            total_seats += len(actual_seats)
        shift_course_list =[]#It will be a list of list behaving exactly like unique course
        for j in courses_in_shift:
            shift_course_list.append([j,len(course_students[j])])
        shift_course_list.sort(key=lambda x: x[1])
        shift_course_list.reverse()
        par = 1 #a parity variable which will change with each course
        lhc_room_numbers = list(lhc_rooms_seats.keys())
        #Above variable contains list of all LHC room numbers
        seats_linear = [0]*total_seats
        even = 0
        odd = 1
        print(len(lhc_rooms),total_seats,tot_stud)
        for course_name in courses_in_shift:
            student_numbers = course_students[course_name] #Has enrollment ID of the Students
            random.shuffle(student_numbers)
            j = 0
            while j<len(student_numbers) and (even<total_seats):
                seats_linear[even] = student_numbers[j]
                j+=1
                even+=1
                tot_stud-=1
        ind=0
        for m in range(len(lhc_room_numbers)):
            lh_room = lhc_room_numbers[m]
            seats_in_room = len(seats_filled[lh_room])
            l = 0 #A pointer
            while l<seats_in_room:
                seats_filled[lh_room][l] = seats_linear[ind]
                ind+=1
                l+=1
        for k in range(len(lhc_room_numbers)):
            lhc_room = lhc_room_numbers[k]
            seats_filled_in_room = seats_filled[lhc_room]
            seats_number = lhc_rooms_seats[lhc_room]
            for j1 in range(len(seats_filled_in_room)):
                if seats_filled_in_room[j1]!=0:
                    student_data_dct[seats_filled_in_room[j1]] = [student_data_dct[seats_filled_in_room[j1]],lhc_room,seats_number[j1],shift,Slt]
                    
        print(f"Left student in {Slt} {shift} is {tot_stud}")
        return student_data_dct
    elif "and" not in Slt:
        file_name = f"../SlotList/{Slt}.csv"
        student_file = open(file_name,"r") #Input File
        reader = csv.reader(student_file)
        student_data = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
        Course = []
        for row in reader:
            if [row[0],Slt] in crslist:
                student_data.append([row[1],row[0]])
                Course.append(row[0])
        student_file.close()
        try:
            file_name1 = f"../SlotList/{Slt}1.csv"
            student_file1 = open(file_name1,"r") #Input File
            reader1 = csv.reader(student_file1)
            student_data1 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
            Course1 = []
            for row in reader1:
                if [row[0],Slt+"1"] in crslist:
                    student_data1.append([row[1],row[0]])
                    Course1.append(row[0])
            student_data+=student_data1
            Course+=Course1
            student_file1.close()
        except:
            pass
        try:
            file_name2 = f"../SlotList/{Slt}2.csv"
            student_file2 = open(file_name2,"r") #Input File
            reader2 = csv.reader(student_file2)
            student_data2 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
            Course2 = []
            for row in reader2:
                if [row[0],Slt+"2"] in crslist:
                    student_data2.append([row[1],row[0]])
                    Course2.append(row[0])
            student_data+=student_data2
            Course+=Course2
            student_file2.close()
        except:
            pass
        #------------------Making a Student Data Dict
        student_data_dct = {}
        for sub in student_data:
            student_data_dct[sub[0]] = sub[1] #This student data dict contains all information for a particular student
        # ---------------------------------------------
        total_students = len(student_data)
        unique_courses= list(set(Course))
        course_students={}#Is a dictionary containing unique courses and students enrolled in that course as a list
        qe=[]
        for i in range(len(unique_courses)):
            ls = [unique_courses[i],Course.count(unique_courses[i])]
            qe.append(ls)
            students=[]
            for j in range(len(student_data)):
                if student_data[j][1]==unique_courses[i]:
                    students.append(student_data[j][0])
            course_students[unique_courses[i]]=students
        unique_courses = qe
        unique_courses.sort(key=lambda x: x[1])
        tot_stud = total_students
        #------------------------Making Document for the shift
        courses_in_shift = []
        for crs in crslist:
            courses_in_shift.append(crs[0])
        lhc_rooms = lh_reader()
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
        shift_course_list =[]#It will be a list of list behaving exactly like unique course
        for j in courses_in_shift:
            shift_course_list.append([j,len(course_students[j])])
        shift_course_list.sort(key=lambda x: x[1])
        shift_course_list.reverse()
        print(len(lhc_rooms),total_seats,tot_stud)
        #--------------------------------------------------------
        lh_cap = [] #Stores a real time capacity of lhc rooms
        for i9 in range(len(lhc_rooms)):
            lh_cap.append([lhc_rooms[i9][0],len(lhc_rooms_seats[lhc_rooms[i9][0]])])
        st_num = tot_stud #Just making a copy of total students
        total_rooms = len(lhc_rooms) #number of rooms
        i7 =0 #An iterator for traversing lhc rooms
        while(st_num>0 and i7<total_rooms):  
            course1 = shift_course_list[0][0]
            num_course1 = shift_course_list[0][1]
            st_course1 = course_students[course1]
            random.shuffle(st_course1)
            course2=0
            num_course2=0
            lh = lhc_rooms[i7][0]
            cap_room = len(lhc_rooms_seats[lh])
            i3 = 0 #An iterator for traversing taken lh seats
            i4 = 0 #An iterator for traversing course1 students
            i5 = 0 #An iterator for traversing course2 students
            st_course2=[]
            try:
                if shift_course_list[1][1]!=0:
                    course2 = shift_course_list[1][0]
                    num_course2=shift_course_list[0][1]
                    st_course2=course_students[course2]
                    random.shuffle(st_course2)
            except:
                pass
            if course2!=0:
                dummy_seats=seats_filled[lh]
                while i3<cap_room and i4+i5<num_course1+num_course2:
                    if i3%2==0 and i4<num_course1:
                        try:
                            dummy_seats[i3]=(st_course1[0])
                            student_data_dct[st_course1[0]]= [student_data_dct[st_course1[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt]
                            i4+=1
                            st_course1.pop(0)
                            st_num-=1
                            tot_stud-=1
                        except:
                            
                            pass #Course filled actually
                    elif i3%2==1 and i5<num_course2:
                        try:
                            dummy_seats[i3]=(st_course2[0])
                            student_data_dct[st_course2[0]]= [student_data_dct[st_course2[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt]
                            i5+=1
                            st_course2.pop(0)
                            st_num-=1
                            tot_stud-=1
                        except:
                            
                            pass
                    i3+=1
                    seats_filled[lh] = dummy_seats
                course_students[course1] = st_course1
                course_students[course2] = st_course2
                shift_course_list[0][1] = len(st_course1)
                shift_course_list[1][1] = len(st_course2)
                shift_course_list.sort(key=lambda x: x[1])
                shift_course_list.reverse()
                seat_numbers = lhc_rooms_seats[lh]
                st_assigned = seats_filled[lh]
                st_course =[]
                for j in st_assigned:
                    try:
                        st_course.append(student_data_dct[j][0])
                    except:
                        st_course.append(0)
                # dct = {"Seat number":seat_numbers,"Enrollment_ID":st_assigned,"Course":st_course}
                # df = pd.DataFrame(dct)
                # df.to_csv(f"{path1}\{lh}_Shift.No.{shift_no}"+".csv",index=False)
            else:
                dummy_seats=seats_filled[lh]
                while i3<cap_room:
                    if i3%2==0 and i4<num_course1:
                        try:
                            dummy_seats[i3]=(st_course1[0])
                            student_data_dct[st_course1[0]]= [student_data_dct[st_course1[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt]
                            i3+=1
                            st_course1.pop(0)
                            st_num-=1
                            tot_stud-=1
                        except:
                            pass #Course filled actually
                    i3+=1
                    seats_filled[lh] = dummy_seats
                course_students[course1] = st_course1
                shift_course_list[0][1] = len(st_course1)
                shift_course_list.sort(key=lambda x: x[1])
                shift_course_list.reverse()
                seat_numbers = lhc_rooms_seats[lh]
                st_assigned = seats_filled[lh]
                st_course=[]
                for j8 in st_assigned:
                    # st_course.append(student_data_dct[j][0])
                    try:
                        st_course.append(student_data_dct[j8][0])
                    except:
                        st_course.append(0)
                # dct = {"Seat number":seat_numbers,"Enrollment_ID":st_assigned,"Course":st_course}
                # df = pd.DataFrame(dct)
                # df.to_csv(f"{path1}\{lh}_Shift.No.{shift_no}"+".csv",index=False) 
            lh_cap[i7][1]= cap_room- min(cap_room,(i4+i5))
            i7+=1
        i8 =0 #A pointer for LHC room
        lh_cap.sort(key=lambda x:x[1])
        lh_cap.reverse()
        while shift_course_list[0][1]!=0 and lh_cap[0][1]!=0:
            crs = shift_course_list[0][0]
            crs_st = course_students[crs]
            k2 = len(crs_st)
            k4 = lh_cap[0][1]
            lh_req = lh_cap[0][0]
            seats_req = seats_filled[lh_req]
            j3=0
            # print(crs_st)
            while(j3<len(seats_req) and (len(crs_st)>0)):
                if seats_req[j3]==0:
                    seats_req[j3] = crs_st[0]
                    student_data_dct[crs_st[0]]=[student_data_dct[crs_st[0]],lh_req,lhc_rooms_seats[lh_req][j3],shift,Slt]
                    crs_st.pop(0)
                    j3+=2
                    st_num-=1
                    tot_stud-=1
                    k4-=1
                    k2-=1
                else:
                    j3+=1
            lh_cap[0][1]=k4
            course_students[crs]=crs_st
            shift_course_list[0][1]=k2
            lh_cap.sort(key=lambda x:x[1])
            lh_cap.reverse()
            shift_course_list.sort(key=lambda x: x[1])
            shift_course_list.reverse()
        print(f"Left student in {Slt} {shift} is {tot_stud}")
        return student_data_dct
    else:
        slts = Slt.split()
        Slt1 = slts[0]
        Slt2 =slts[2]
        file_name = f"../SlotList/{Slt1}.csv"
        student_file = open(file_name,"r") #Input File
        reader = csv.reader(student_file)
        student_data = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
        Course = []
        for row in reader:
            if [row[0],Slt1] in crslist:
                student_data.append([row[1],row[0]])
                Course.append(row[0])
        student_file.close()
        try:
            file_name1 = f"../SlotList/{Slt1}1.csv"
            student_file1 = open(file_name1,"r") #Input File
            reader1 = csv.reader(student_file1)
            student_data1 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
            Course1 = []
            for row in reader1:
                if [row[0],Slt1+"1"] in crslist:
                    student_data1.append([row[1],row[0]])
                    Course1.append(row[0])
            student_data+=student_data1
            Course+=Course1
            student_file1.close()
        except:
            pass
        try:
            file_name2 = f"../SlotList/{Slt1}2.csv"
            student_file2 = open(file_name2,"r") #Input File
            reader2 = csv.reader(student_file2)
            student_data2 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course Enrolled
            Course2 = []
            for row in reader2:
                if [row[0],Slt1+"2"] in crslist:
                    student_data2.append([row[1],row[0]])
                    Course2.append(row[0])
            student_data+=student_data2
            Course+=Course2
            student_file2.close()
        except:
            pass
        file_name1 = f"../SlotList/{Slt2}.csv"
        student_file1 = open(file_name1,"r") #Input File
        reader = csv.reader(student_file1)
        student_data_1 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course_1 Enrolled
        Course_1 = []
        for row in reader:
            if [row[0],Slt2] in crslist:
                student_data_1.append([row[1],row[0]])
                Course_1.append(row[0])
        student_file1.close()
        try:
            file_name1 = f"../SlotList/{Slt2}1.csv"
            student_file1 = open(file_name1,"r") #Input File
            reader1 = csv.reader(student_file1)
            student_data_11 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course_1 Enrolled
            Course_11 = []
            for row in reader1:
                if [row[0],Slt2+"1"] in crslist:
                    student_data_11.append([row[1],row[0]])
                    Course_11.append(row[0])
            student_data_1+=student_data_11
            Course_1+=Course_11
            student_file1.close()
        except:
            pass
        try:
            file_name2 = f"../SlotList/{Slt2}2.csv"
            student_file2 = open(file_name2,"r") #Input File
            reader2 = csv.reader(student_file2)
            student_data_12 = [] #It is a list of list in which the inner list will contain the data of student's Enrollment ID and Course_1 Enrolled
            Course_12 = []
            for row in reader2:
                if [row[0],Slt2+"2"] in crslist:
                    student_data_12.append([row[1],row[0]])
                    Course_12.append(row[0])
            student_data_1+=student_data_12
            Course_1+=Course_12
            student_file2.close()
        except:
            pass        
        #------------------Making a Student Data Dict
        student_data_dct = {}
        for sub in student_data:
            student_data_dct[sub[0]] = sub[1] #This student data dict contains all information for a particular student
        student_data_dct_1 = {}
        for sub in student_data_1:
            student_data_dct_1[sub[0]] = sub[1] #This student data dict contains all information for a particular student
        # ---------------------------------------------
        total_students = len(student_data)
        unique_courses= list(set(Course))
        course_students={}#Is a dictionary containing unique courses and students enrolled in that course as a list
        qe=[]
        for i in range(len(unique_courses)):
            ls = [unique_courses[i],Course.count(unique_courses[i])]
            qe.append(ls)
            students=[]
            for j in range(len(student_data)):
                if student_data[j][1]==unique_courses[i]:
                    students.append(student_data[j][0])
            course_students[unique_courses[i]]=students
        unique_courses = qe
        unique_courses.sort(key=lambda x: x[1])
        tot_stud = total_students

        # ---------------------------------------------
        total_students_1 = len(student_data_1)
        unique_courses_1= list(set(Course_1))
        only_unique_courses_1= unique_courses_1[:]
        course_students_1={}#Is a dictionary containing unique courses and students enrolled in that course as a list
        qe_1=[]
        for i in range(len(unique_courses_1)):
            ls = [unique_courses_1[i],Course_1.count(unique_courses_1[i])]
            qe_1.append(ls)
            students=[]
            for j in range(len(student_data_1)):
                if student_data_1[j][1]==unique_courses_1[i]:
                    students.append(student_data_1[j][0])
            course_students_1[unique_courses_1[i]]=students
        unique_courses_1 = qe_1
        unique_courses_1.sort(key=lambda x: x[1])
        tot_stud_1 = total_students_1
        #-------------------Making Documents for the shift
        lhc_rooms = lh_reader()
        lhc_rooms_seats={} #seat number dictionary
        seats_filled = {}
        total_seats = 0
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
        print(len(lhc_rooms),total_seats,tot_stud,tot_stud_1,"Mixed Slots")
        #Deciding LHC rooms for slot 2-----------
        lhc_rooms_1 = [['lh316', '..\\seating\\lh316seq', 82], ['lh310', '..\\seating\\lh310seq', 82], ['lh308', '..\\seating\\lh308seq', 82]]
        for rm in lhc_rooms_1:
            lhc_rooms.remove(rm)
        #----------------------------------------
        courses_in_shift = []
        for crs in crslist:
            courses_in_shift.append(crs[0])
        shift_course_list =[]#It will be a list of list behaving exactly like unique course
        for j in courses_in_shift:
            try:
                shift_course_list.append([j,len(course_students[j])])
            except:
                pass
        shift_course_list.sort(key=lambda x: x[1])
        shift_course_list.reverse()
        #--------------------------------------
        courses_in_shift_1 = []
        for crs in crslist:
            if crs[0] in only_unique_courses_1:
                courses_in_shift_1.append(crs[0])
        shift_course_list_1 =[]
        for j in courses_in_shift_1:
            try:
                shift_course_list_1.append([j,len(course_students_1[j])])
            except:
                pass
        shift_course_list_1.sort(key=lambda x: x[1])
        shift_course_list_1.reverse()
        #------------------------------------------
        lh_cap_1 = [] #Stores a real time capacity of lhc rooms
        for i9 in range(len(lhc_rooms_1)):
            lh_cap_1.append([lhc_rooms_1[i9][0],len(lhc_rooms_seats[lhc_rooms_1[i9][0]])])
        st_num_1 = tot_stud_1 #Just making a copy of total students
        total_rooms_1 = len(lhc_rooms_1) #number of rooms
        i7 =0 #An iterator for traversing lhc rooms
        while(st_num_1>0 and i7<total_rooms_1):
            course1 = shift_course_list_1[0][0]
            num_course1 = shift_course_list_1[0][1]
            st_course1 = course_students_1[course1]
            random.shuffle(st_course1)
            course2=0
            num_course2=0
            lh = lhc_rooms_1[i7][0]
            cap_room = len(lhc_rooms_seats[lh])
            i3 = 0 #An iterator for traversing taken lh seats
            i4 = 0 #An iterator for traversing course1 students
            i5 = 0 #An iterator for traversing course2 students
            st_course2=[]
            try:
                if shift_course_list_1[1][1]!=0:
                    course2 = shift_course_list_1[1][0]
                    num_course2=shift_course_list_1[0][1]
                    st_course2=course_students_1[course2]
                    random.shuffle(st_course2)
            except:
                pass
            if course2!=0:
                dummy_seats=seats_filled[lh]
                while i3<cap_room and i4+i5<num_course1+num_course2:
                    if i3%2==0 and i4<num_course1:
                        try:
                            dummy_seats[i3]=(st_course1[0])
                            student_data_dct_1[st_course1[0]]= [student_data_dct_1[st_course1[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt2]
                            i4+=1
                            st_course1.pop(0)
                            st_num_1-=1
                            tot_stud_1-=1
                        except:                         
                            pass #Course filled actually
                    elif i3%2==1 and i5<num_course2:
                        try:
                            dummy_seats[i3]=(st_course2[0])
                            student_data_dct_1[st_course2[0]]= [student_data_dct_1[st_course2[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt2]
                            i5+=1
                            st_course2.pop(0)
                            st_num_1-=1
                            tot_stud_1-=1
                        except:
                            
                            pass
                    i3+=1
                    seats_filled[lh] = dummy_seats
                course_students_1[course1] = st_course1
                course_students_1[course2] = st_course2
                shift_course_list_1[0][1] = len(st_course1)
                shift_course_list_1[1][1] = len(st_course2)
                shift_course_list_1.sort(key=lambda x: x[1])
                shift_course_list_1.reverse()
                seat_numbers = lhc_rooms_seats[lh]
                st_assigned = seats_filled[lh]
                st_course =[]
                for j in st_assigned:
                    try:
                        st_course.append(student_data_dct_1[j][0])
                    except:
                        st_course.append(0)
                # dct = {"Seat number":seat_numbers,"Enrollment_ID":st_assigned,"Course":st_course}
                # df = pd.DataFrame(dct)
                # df.to_csv(f"{path1}\{lh}_Shift.No.{shift_no}"+".csv",index=False)
            else:
                dummy_seats=seats_filled[lh]
                while i3<cap_room:
                    if i3%2==0 and i4<num_course1:
                        try:
                            dummy_seats[i3]=(st_course1[0])
                            student_data_dct_1[st_course1[0]]= [student_data_dct_1[st_course1[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt2]
                            i3+=1
                            st_course1.pop(0)
                            st_num_1-=1
                            tot_stud_1-=1
                        except:
                            pass #Course filled actually
                    i3+=1
                    seats_filled[lh] = dummy_seats
                course_students_1[course1] = st_course1
                shift_course_list_1[0][1] = len(st_course1)
                shift_course_list_1.sort(key=lambda x: x[1])
                shift_course_list_1.reverse()
                seat_numbers = lhc_rooms_seats[lh]
                st_assigned = seats_filled[lh]
                st_course=[]
                for j8 in st_assigned:
                    # st_course.append(student_data_dct_1[j][0])
                    try:
                        st_course.append(student_data_dct_1[j8][0])
                    except:
                        st_course.append(0)
                # dct = {"Seat number":seat_numbers,"Enrollment_ID":st_assigned,"Course":st_course}
                # df = pd.DataFrame(dct)
                # df.to_csv(f"{path1}\{lh}_Shift.No.{shift_no}"+".csv",index=False) 
            lh_cap_1[i7][1]= cap_room- min(cap_room,(i4+i5))
            i7+=1
        i8 =0 #A pointer for LHC room
        lh_cap_1.sort(key=lambda x:x[1])
        lh_cap_1.reverse()
        # print(student_data_dct_1)
        while shift_course_list_1[0][1]!=0 and lh_cap_1[0][1]!=0:
            crs = shift_course_list_1[0][0]
            crs_st = course_students_1[crs]
            k2 = len(crs_st)
            k4 = lh_cap_1[0][1]
            lh_req = lh_cap_1[0][0]
            seats_req = seats_filled[lh_req]
            j3=0
            # print(crs_st)
            while(j3<len(seats_req) and (len(crs_st)>0)):
                
                if seats_req[j3]==0:
                    seats_req[j3] = crs_st[0]
                    student_data_dct_1[crs_st[0]]=[student_data_dct_1[crs_st[0]],lh_req,lhc_rooms_seats[lh_req][j3],shift,Slt2]
                    crs_st.pop(0)
                    j3+=2
                    st_num_1-=1
                    tot_stud_1-=1
                    k4-=1
                    k2-=1
                else:
                    j3+=1
            lh_cap_1[0][1]=k4
            course_students_1[crs]=crs_st
            shift_course_list_1[0][1]=k2
            lh_cap_1.sort(key=lambda x:x[1])
            lh_cap_1.reverse()
            shift_course_list_1.sort(key=lambda x: x[1])
            shift_course_list_1.reverse()
        print(f"Left student in {Slt2} {shift} is {tot_stud_1}")
        #------------------------------------------
        lh_cap = [] #Stores a real time capacity of lhc rooms
        for i9 in range(len(lhc_rooms)):
            lh_cap.append([lhc_rooms[i9][0],len(lhc_rooms_seats[lhc_rooms[i9][0]])])
        st_num = tot_stud #Just making a copy of total students
        total_rooms = len(lhc_rooms) #number of rooms
        i7 =0 #An iterator for traversing lhc rooms
        while(st_num>0 and i7<total_rooms):  
            course1 = shift_course_list[0][0]
            num_course1 = shift_course_list[0][1]
            st_course1 = course_students[course1]
            random.shuffle(st_course1)
            course2=0
            num_course2=0
            lh = lhc_rooms[i7][0]
            cap_room = len(lhc_rooms_seats[lh])
            i3 = 0 #An iterator for traversing taken lh seats
            i4 = 0 #An iterator for traversing course1 students
            i5 = 0 #An iterator for traversing course2 students
            st_course2=[]
            try:
                if shift_course_list[1][1]!=0:
                    course2 = shift_course_list[1][0]
                    num_course2=shift_course_list[0][1]
                    st_course2=course_students[course2]
                    random.shuffle(st_course2)
            except:
                pass
            if course2!=0:
                dummy_seats=seats_filled[lh]
                while i3<cap_room and i4+i5<num_course1+num_course2:
                    if i3%2==0 and i4<num_course1:
                        try:
                            dummy_seats[i3]=(st_course1[0])
                            student_data_dct[st_course1[0]]= [student_data_dct[st_course1[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt1]
                            i4+=1
                            st_course1.pop(0)
                            st_num-=1
                            tot_stud-=1
                        except:
                            
                            pass #Course filled actually
                    elif i3%2==1 and i5<num_course2:
                        try:
                            dummy_seats[i3]=(st_course2[0])
                            student_data_dct[st_course2[0]]= [student_data_dct[st_course2[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt1]
                            i5+=1
                            st_course2.pop(0)
                            st_num-=1
                            tot_stud-=1
                        except:
                            
                            pass
                    i3+=1
                    seats_filled[lh] = dummy_seats
                course_students[course1] = st_course1
                course_students[course2] = st_course2
                shift_course_list[0][1] = len(st_course1)
                shift_course_list[1][1] = len(st_course2)
                shift_course_list.sort(key=lambda x: x[1])
                shift_course_list.reverse()
                seat_numbers = lhc_rooms_seats[lh]
                st_assigned = seats_filled[lh]
                st_course =[]
                for j in st_assigned:
                    try:
                        st_course.append(student_data_dct[j][0])
                    except:
                        st_course.append(0)
                # dct = {"Seat number":seat_numbers,"Enrollment_ID":st_assigned,"Course":st_course}
                # df = pd.DataFrame(dct)
                # df.to_csv(f"{path1}\{lh}_Shift.No.{shift_no}"+".csv",index=False)
            else:
                dummy_seats=seats_filled[lh]
                while i3<cap_room:
                    if i3%2==0 and i4<num_course1:
                        try:
                            dummy_seats[i3]=(st_course1[0])
                            student_data_dct[st_course1[0]]= [student_data_dct[st_course1[0]],lh,lhc_rooms_seats[lh][i3],shift,Slt1]
                            i3+=1
                            st_course1.pop(0)
                            st_num-=1
                            tot_stud-=1
                        except:
                            pass #Course filled actually
                    i3+=1
                    seats_filled[lh] = dummy_seats
                course_students[course1] = st_course1
                shift_course_list[0][1] = len(st_course1)
                shift_course_list.sort(key=lambda x: x[1])
                shift_course_list.reverse()
                seat_numbers = lhc_rooms_seats[lh]
                st_assigned = seats_filled[lh]
                st_course=[]
                for j8 in st_assigned:
                    # st_course.append(student_data_dct[j][0])
                    try:
                        st_course.append(student_data_dct[j8][0])
                    except:
                        st_course.append(0)
                # dct = {"Seat number":seat_numbers,"Enrollment_ID":st_assigned,"Course":st_course}
                # df = pd.DataFrame(dct)
                # df.to_csv(f"{path1}\{lh}_Shift.No.{shift_no}"+".csv",index=False) 
            lh_cap[i7][1]= cap_room- min(cap_room,(i4+i5))
            i7+=1
        i8 =0 #A pointer for LHC room
        lh_cap.sort(key=lambda x:x[1])
        lh_cap.reverse()
        while shift_course_list[0][1]!=0 and lh_cap[0][1]!=0:
            crs = shift_course_list[0][0]
            crs_st = course_students[crs]
            k2 = len(crs_st)
            k4 = lh_cap[0][1]
            lh_req = lh_cap[0][0]
            seats_req = seats_filled[lh_req]
            j3=0
            # print(crs_st)
            while(j3<len(seats_req) and (len(crs_st)>0)):
                if seats_req[j3]==0:
                    seats_req[j3] = crs_st[0]
                    student_data_dct[crs_st[0]]=[student_data_dct[crs_st[0]],lh_req,lhc_rooms_seats[lh_req][j3],shift,Slt1]
                    crs_st.pop(0)
                    j3+=2
                    st_num-=1
                    tot_stud-=1
                    k4-=1
                    k2-=1
                else:
                    j3+=1
            lh_cap[0][1]=k4
            course_students[crs]=crs_st
            shift_course_list[0][1]=k2
            lh_cap.sort(key=lambda x:x[1])
            lh_cap.reverse()
            shift_course_list.sort(key=lambda x: x[1])
            shift_course_list.reverse()
        # print(shift_course_list)
        print(f"Left student in {Slt1} {shift} is {tot_stud}")
        return student_data_dct,student_data_dct_1
#--------------------------------------------------------------------------------------------------File Generator
def make_file():
    scd = schedule_reader()
    dyslt = day_slots()
    dyslt=dyslt[1:]
    dct={"Enrollment Number":[],"Day":[],"Shift":[],"Slot":[],"Course":[],"LHC NO.":[],"Seat-Number":[]}
    for day in scd:
        dy = day[0]
        crsdct = (generator_day(day))
        day = day[1:]
        day_order=[]
        for i in range(len(day)):
            day_order.append([day[i],i])
        day_order.sort(key=lambda x:len(x[0])) #shifts.sort(key = lambda x:len(x))
        day_order.reverse()
        dct_req={}
        mna = list(crsdct.keys())
        for j in range(len(day_order)):
            try:
                dct_req[day_order[j][1]] = mna[j]
            except:
                pass
        cwd = os.getcwd() # gives current Working Directory
        path = cwd+f'/Courses in shift'
        try:
            os.mkdir(path)
        except:
            pass
        try:
            os.mkdir(path+f"/{dy}")
            path = path+f"/{dy}"
        except:
            pass
        for j1 in range(len(day)):
            shift= dyslt[j1]
            slot = day[j1]  
            print(dy,slot,shift) 
            try:       
                crslist=crsdct[dct_req[j1]]
            except:
                crslist=[]
            if "indi" in slot:
                tormv =[]
                for crs in crslist:
                    if crs[1]!=slot:
                        tormv.append(crs)
                for m1 in tormv:
                    crslist.remove(m1)
            if slot=="indi":
                crslist=[["MTL100","indi"]]
            if crslist==[]:
                continue
            #-------------------------------------------------------
            # print(crslist)
            dct3={"Courses":[],"Strength":[]}
            for crs in crslist:
                dct3["Courses"]+=[crs[0]]
                dct3["Strength"]+=[crs_stud(crs[0],slot)]
            df4 = pd.DataFrame(dct3)
            df4.to_csv(f"{path}/{dy} Shift-{j1+1}.csv",index=False)
            #------------------------------------------------------
            if slot=="nan":
                pass
            elif "and" not in slot:
                dct1 = shift_dct_generator(slot,crslist,shift)
                l1=[]
                l2=[]
                l3=[]
                l4=[]
                l5=[]
                l6=[]
                l7=[]
                try:
                    for j2 in dct1:
                        l1.append(j2)
                        l2.append(dy)
                        l3.append(shift)
                        l4.append(dct1[j2][4])
                        l5.append(dct1[j2][0])
                        l6.append(dct1[j2][1])
                        l7.append(dct1[j2][2])
                    dct["Enrollment Number"]+=l1
                    dct["Day"]+=l2
                    dct["Shift"]+=l3
                    dct["Slot"]+=l4
                    dct["Course"]+=l5
                    dct["LHC NO."]+=l6
                    dct["Seat-Number"]+=l7
                except:
                    pass
            elif "and" in slot:
                dct1,dct2 = shift_dct_generator(slot,crslist,shift)
                l1=[]
                l2=[]
                l3=[]
                l4=[]
                l5=[]
                l6=[]
                l7=[]
                try:
                    for j2 in dct1:
                        l1.append(j2)
                        l2.append(dy)
                        l3.append(shift)
                        l4.append(dct1[j2][4])
                        l5.append(dct1[j2][0])
                        l6.append(dct1[j2][1])
                        l7.append(dct1[j2][2])
                    dct["Enrollment Number"]+=l1
                    dct["Day"]+=l2
                    dct["Shift"]+=l3
                    dct["Slot"]+=l4
                    dct["Course"]+=l5
                    dct["LHC NO."]+=l6
                    dct["Seat-Number"]+=l7
                except:
                    pass
                try:
                    l1=[]
                    l2=[]
                    l3=[]
                    l4=[]
                    l5=[]
                    l6=[]
                    l7=[]
                    for j2 in dct2:
                        l1.append(j2)
                        l2.append(dy)
                        l3.append(shift)
                        l4.append(dct2[j2][4])
                        l5.append(dct2[j2][0])
                        l6.append(dct2[j2][1])
                        l7.append(dct2[j2][2])
                    dct["Enrollment Number"]+=l1
                    dct["Day"]+=l2
                    dct["Shift"]+=l3
                    dct["Slot"]+=l4
                    dct["Course"]+=l5
                    dct["LHC NO."]+=l6
                    dct["Seat-Number"]+=l7
                except:
                    pass  
            print("--"*50)   
    df2 = pd.DataFrame(dct)
    df2.to_csv("MEGAFILE.csv",index=False)
# print(generator_day(schedule_reader()[4]))
make_file()
# print(lh_reader())

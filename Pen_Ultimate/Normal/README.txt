1. Put LHC seat files in "seating" folder and the file should be like 'lhabcseq'.
2. Slot Files should be in "SlotList" folder and the format should be like "{slotCharacter}.csv".
3. Exam Schedules should be in "Exam Schedule.xlsx" and four some shifts where only one course is to be conducted keep the slot name as indi.(Eg. MTL100)
	---For some shifts where 2 slots are to be organised in together, the slot naming should be like "A and T".
4. As said above, some shifts will have 2 slot exams being conducted together, so there were some courses which were conflicing with each other; Those course list were kept in "Constraint 1" folder and the file format is like "A and T.xlsx".
5. All the course related data were put up in "Course_Data.xlsx".
6. The half semester courses which were scheduled for second half of the semester were removed from Course_Data File.
7. Some courses needed 1 hour and 30 min slot, those were also removed as they will be workedout seperately. After that we can join the csv sheets.
----------------------
Run the main.py file in codes folder and it will generate the csv sheet
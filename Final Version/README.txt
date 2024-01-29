1. Put LHC seat files in "seating" folder and the file should be like 'lhabcseq'.
2. Slot Files should be in "SlotList" folder and the format should be like "{D1S6}.csv".
3. All the course related data were put up in "Course_Data.xlsx". (Please mantain the format otherwise the code might not work perfectly)
4. The half semester courses which were scheduled for second half of the semester were removed from Course_Data File.
5. Some courses needed 1 hour and 30 min slot, those need to be removed from course data as they will be workedout seperately. After that we can join the csv sheets.
----------------------
Run the main.py file in codes folder and it will generate the csv sheet
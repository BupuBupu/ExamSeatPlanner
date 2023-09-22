import os
import pandas as pd
def delete_folder(path):
    # Check if the path exists and is a directory
    if os.path.exists(path) and os.path.isdir(path):
        # Get a list of files and subdirectories in the folder
        items = os.listdir(path)
        
        # Loop through the items
        for item in items:
            item_path = os.path.join(path, item)
            
            # Check if it's a file and delete it
            if os.path.isfile(item_path):
                os.remove(item_path)
            # If it's a directory, recursively delete it
            elif os.path.isdir(item_path):
                delete_folder(item_path)
        
        # Once the folder is empty, use os.rmdir to delete it
        os.rmdir(path)
def slotlist_generator(course_data,registration):
    cwd = os.getcwd()
    path = cwd+f'\SlotList'
    try:
        os.mkdir(path)
    except:
        pass
    df = pd.read_excel(course_data)
    col = df.columns
    shifts = list(set(df[col[1]]))
    shifts.sort()
    courses_in_shift={} #A dictionary storing 
    for sft in shifts:
        lst = []
        for ind in df.index:
            if df[col[1]][ind]==sft:
                lst.append(df[col[0]][ind])
        courses_in_shift[sft] = lst
    df1 = pd.read_excel(registration)
    col1 = df1.columns
    for shift in shifts:
        courses = courses_in_shift[shift]
        students = []
        course = []
        for ind in df1.index:
            if df1[col1[0]][ind] in courses:
                course.append(df1[col1[0]][ind])
                students.append(df1[col1[1]][ind])
        dct1 ={"Course Code":course,"Enrollment Number":students}
        df3 = pd.DataFrame(dct1)
        df3.to_csv(f"{path}\{shift}.csv",index=False)
    return path


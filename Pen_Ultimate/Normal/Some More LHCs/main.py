s1 = [517,519,521,602,604,606,611,613,615,619,621,623]
s2=[518,520,603,605,612,614,620,622]
seat1=[]
seat2=[]
for i in "ABCDEF":
    for j in range(1,11):
        seat1.append(f"{i}{j}\n")
for i1 in "ABCDE":
    for j1 in range(1,7):
        seat2.append(f"{i1}{j1}\n")
for m in s1:
    f1 =open(f"lh{m}seq", "w")
    f1.writelines(seat1)
    f1.close()
for m1 in s2:
    f2 = open(f"lh{m1}seq","w")
    f2.writelines(seat2)
    f2.close()

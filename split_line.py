gt_path = "classnames.names"


f = open(gt_path, "r")
lines = f.readlines()
f_new = open("myfile.txt", "x")


for line in lines:
    splited_line = line.split(" - ")[1]
    f_new.write(splited_line)



f.close()
f_new.close()
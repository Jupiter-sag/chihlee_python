import csv
#reader:list，內置dictionary
with open("考試分數_3年6班.csv","r",encoding="utf-8") as file:
    reader=csv.DictReader(file)
    print(type(reader))
    for row in reader:
        if int(row['數學'])>90:
         print(row['學生姓名'])
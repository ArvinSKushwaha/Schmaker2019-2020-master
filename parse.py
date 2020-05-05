import csv

with open("Sem2.csv") as f:
    courses = list(csv.reader(f))[1:]
    course_names = [i[0] for i in courses]
    names = []
    for i in sorted(course_names):
        course_numbers = i.split(' ')[0]
        course_name = " ".join(i.split(' ')[1:])
        names.append(f"<option value=\"{i}\"></option>")
        with open(f"Schedule\\Semester2\\{course_numbers}.txt", "w") as f2:
            f2.write(course_name + "\n")
            for meetings in set([m[-1] for m in filter(lambda x: x[0]==i, courses)]):
                f2.write(meetings + "\n")
    print("\n".join(sorted(list(set(names)))))
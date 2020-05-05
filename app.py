from flask import Flask, request, render_template, url_for, jsonify
from multiprocessing import Pool, cpu_count
# from functools import reduce
from itertools import product
from json import dumps
from math import floor
from pprint import pprint

def gpa_val(x):
    try:
        numbs = int(x[-4:]) if(x[-1].isdigit()) else int(x[-5:-1])
        if(numbs >= 3000 and numbs < 3500):
            return 4.5
        if(numbs >= 3500 and numbs < 4000):
            return 4.75
        if(numbs >= 4000):
            return 5
        else:
            return None
    except BaseException as e:
        print(e)
        return None

def minutes(sched):
    if('L' == sched[1]):
        return 40
    if(sched[1] in '12345'):
        return 50
    else:
        return 0

def parseSchedule(meetings):
    block = meetings[0]
    if(block not in 'ABCDEFGHI'):
        return []
    blocks = []
    for i in range(len(meetings[1:])):
        if(not meetings[i+1] in 'ABCDEFGHI'):
            if(block+meetings[i+1] != "GL"):
                blocks.append(block+meetings[i+1])
            else:
                if(meetings[i] == "3"):
                    blocks.append(block+"L1")
                if(meetings[i] == "5"):
                    blocks.append(block+"L2")
        else:
            block = meetings[i+1]
    return blocks

def safe(scheds):
    sum = []
    for i in scheds:
        # print(i)
        sum += parseSchedule(i) if i else []
    # print(sum)
    if(len(set(sum)) == len(sum)):
        return True
    return False

app = Flask(__name__)

@app.route("/use_times", methods = ['GET', 'POST'])
def home():
    with open("counter.txt") as f:
        return jsonify({'ip': request.remote_addr, 'counts': f.read()})
    
@app.route("/", methods = ['GET', 'POST'])
def home2():
    if(request.method == "GET"):
        with open("counter.txt", "r") as f:
            c = int(f.read())
        with open("counter.txt", "w") as f:
            f.write(str(c + 1))
        return render_template("index.2.html")
    if(request.method == "POST"):
        r = request.form
        rows = len(r)//2
        classes = [[],[]]
        cnames = [[],[]]
        # print(r)
        for i in range(rows):
            # print(f'Choice{i+1}')
            tri1 = r.get(f'sem1Choice{i+1}').split(' ')
            if(tri1[0]):
                classes[0].append(tri1[0])
            tri2 = r.get(f'sem2Choice{i+1}').split(' ')
            if(tri2[0]):
                classes[1].append(tri2[0])
        sem1_meetings = [open(f'Schedule/Semester1/{i}.txt', 'r').read().splitlines()[1:]  for i in classes[0]]
        sem2_meetings = [open(f'Schedule/Semester2/{i}.txt', 'r').read().splitlines()[1:] for i in classes[1]]
        # print(tri1_meetings)
        # print('\n'.join([repr([parseSchedule(x) for x in i]) for i in tri1_meetings]))
        # print([list(i) for i in product(*tri1_meetings)])
        # print([safe(x) for x in product(*tri1_meetings)])
        sems = [map(safe,product(*sem1_meetings)), map(safe,product(*sem2_meetings))]
        sem1_success = any(sems[0])
        sem2_success = any(sems[1])
        print(sem1_meetings, sem2_meetings)
        numpos = [len(list(i)) for i in sems]
        numpos = f"Semester 1: {numpos[0]} combinations<br>Semester 2: {numpos[1]} combinations"
        success = [sem1_success, sem2_success]
        schedules = [[]]
        schedule = schedules[0]
        num1, num2 = 0, 0
        if(all(success)):
            for i in product(*sem1_meetings):
                if(safe(i)):
                    num1 += 1
                    schedule.append(i)
            for i in product(*sem2_meetings):
                if(safe(i)):
                    num2 +=1
                    schedule.append(i)
            for i in range(len(schedule)):
                if('VS' in schedule[i]):
                    schedule[i] = list(schedule[i])
                    index = schedule[i].index('VS')
                    schedule[i].pop(index)
                    classes[i].pop(index)
            schedule = [[(parseSchedule(pattern), classname) for pattern,classname in zip(*i)] for i in zip(schedule, classes)]
            print(schedule)
            if(len(schedule[0]) == 0):
                num1 = 0
            if(len(schedule[1]) == 0):
                num2 = 0
        schedule2 = [{
            'A1':'Free Time',
            'A2':'Free Time',
            'A3':'Free Time',
            'A4':'Free Time',
            'B1':'Free Time',
            'B2':'Free Time',
            'B4':'Free Time',
            'B5':'Free Time',
            'C1':'Free Time',
            'C3':'Free Time',
            'C4':'Free Time',
            'C5':'Free Time',
            'D1':'Free Time',
            'D2':'Free Time',
            'D3':'Free Time',
            'D5':'Free Time',
            'E1':'Free Time',
            'E2':'Free Time',
            'E3':'Free Time',
            'E4':'Free Time',
            'E5':'Free Time',
            'F1':'Free Time',
            'F3':'Free Time',
            'F4':'Free Time',
            'F5':'Free Time',
            'G1':'Free Time',
            'G3':'Free Time',
            'G4':'Free Time',
            'G5':'Free Time',
            'H1':'Free Time',
            'H2':'Free Time',
            'H3':'Free Time',
            'H4':'Free Time',
            'I1':'Free Time',
            'I2':'Free Time',
            'I3':'Free Time',
            'I4':'Free Time',
            'AL':'Free Time',
            'BL':'Free Time',
            'CL':'Free Time',
            'DL':'Free Time',
            'EL':'Free Time',
            'FL':'Free Time',
            'GL1':'Free Time',
            'GL2':'Free Time',
        },{
            'A1':'Free Time',
            'A2':'Free Time',
            'A3':'Free Time',
            'A4':'Free Time',
            'B1':'Free Time',
            'B2':'Free Time',
            'B4':'Free Time',
            'B5':'Free Time',
            'C1':'Free Time',
            'C3':'Free Time',
            'C4':'Free Time',
            'C5':'Free Time',
            'D1':'Free Time',
            'D2':'Free Time',
            'D3':'Free Time',
            'D5':'Free Time',
            'E1':'Free Time',
            'E2':'Free Time',
            'E3':'Free Time',
            'E4':'Free Time',
            'E5':'Free Time',
            'F1':'Free Time',
            'F3':'Free Time',
            'F4':'Free Time',
            'F5':'Free Time',
            'G1':'Free Time',
            'G3':'Free Time',
            'G4':'Free Time',
            'G5':'Free Time',
            'H1':'Free Time',
            'H2':'Free Time',
            'H3':'Free Time',
            'H4':'Free Time',
            'I1':'Free Time',
            'I2':'Free Time',
            'I3':'Free Time',
            'I4':'Free Time',
            'AL':'Free Time',
            'BL':'Free Time',
            'CL':'Free Time',
            'DL':'Free Time',
            'EL':'Free Time',
            'FL':'Free Time',
            'GL1':'Free Time',
            'GL2':'Free Time',
        }
        ]
        for i in schedule2:
            for j in i.keys():
                i[j] = ''
        tot = []
        for i in classes:
            tot+=i
        tot = [gpa_val(i) for i in tot]
        n = 0
        c = 0
        for i in tot:
            if(i):
                n += i
                c += 1
        gpa = n/c
            
        if(all(success)):
            for semester in range(2):
                for i in range(len(schedule[semester])):
                    ctuple = schedule[semester][i]
                    for i in ctuple[0]:
                        schedule2[semester][i] = ctuple[1]
            # pprint(schedule2)
        sems = [0,0,0]
        if(schedule):
            for i in range(2):
                for j in schedule[i]:
                    for k in j[0]:
                        sems[i] += minutes(k)
            n = f"Semester 1: {floor(sems[0]/60)} hrs {sems[0]%60} min<br>Semester 2: {floor(sems[1]/60)} hrs {sems[1]%60} min<br>"
        else:
            n = "Conflicts Found"
        print(n)
        gpa = str(round(gpa,2))
        gpa = gpa if('.' in gpa) else gpa + '.0'
        print([num1, num2])
        return dumps([success, schedule2, gpa, n, numpos, [num1, num2]])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)
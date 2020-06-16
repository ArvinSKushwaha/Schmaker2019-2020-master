from flask import Flask, request, render_template, url_for, jsonify
from multiprocessing import Pool, cpu_count
from functools import reduce
from operator import add
from itertools import product
from json import dumps
from math import floor
from pprint import pprint

KEYS = ["A1", "A2", "A3", "A4", "B1", "B2", "B4", "B5", "C1", "C3", "C4", "C5", "D1", "D2", "D3", "D5", "E1", "E2", "E3", "E5", "F1", "F3", "F4", "F5", "G1", "G3", "G5", "H1", "H2", "H3", "H4", "I1", "I2", "I3", "I4", "AL", "BL", "CL", "DL", "EL", "FL", "GL1", "GL2"]

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
    sched = parse(sched)
    time = 0
    for i in sched:
        if('L' == i[1]):
            time += 40
        if(i[1] in '12345' and not i[0] in 'M'):
            time += 50
        else:
            time += 0
    return time

def parse(meetings):
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

def unique(arr):
    return len(arr) == len(set(arr))

def safe(combo):
    if(len(combo) == 0): return True
    m = reduce(add, map(parse, combo))
    return unique(m)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
@app.route("/", methods = ['GET', 'POST'])
def home2():
    if(request.method == "GET"):
        with open("SemesterOptions.txt") as f:
            return render_template("index.yeet.html", option=f.readlines())
    if(request.method == "POST"):
        r = request.form
        rows = len(r)//2
        pprint(r)

        success = []
        combo_count = []
        time_taken = [0, 0]
        schedules = []

        for semester in range(1, 3):
            classes = []
            for choice in range(1, rows+1):
                option = f"sem{semester}Choice{choice}" # Generates the keys for the request.form dictionary
                try:
                    classes.append(r.get(option).split()[0]) # Gives a list of class IDs
                except IndexError:
                    pass # Allow for blank spaces
            options_per_class = []
            for c in classes:
                try:
                    with open(f"Schedule/Semester{semester}/{c}.txt", "r") as f: # Opens the file containing the meeting patterns
                        options_per_class.append([i.strip() for i in f.readlines()[1:]]) # Load class options
                except:
                    options_per_class.append([" "]) # Allow for blank spaces
            class_combinations = product(*options_per_class)
            possible_combos = []
            for combo in class_combinations:
                if(safe(combo)):
                    possible_combos.append(combo)
            combination_count = len(possible_combos) if all(classes) else 0
            combo_count.append(combination_count)
            if(combination_count > 0 or not all(classes)):
                success.append(True)
            else:
                success.append(False)
            if(combination_count > 0):
                for class_ in possible_combos[0]:
                    time_taken[semester-1] += minutes(class_)
            
            schedule = []
            for curr_opt in possible_combos:
                curr_sched = dict()
                for key in KEYS:
                    curr_sched.update([(key, '')])
                for c, meet in zip(classes, curr_opt):
                    for key in parse(meet):
                        curr_sched[key] = c
                schedule.append(curr_sched)
            schedules.append(schedule)
        pprint(schedules)
        time_taken = f"Semester 1: {time_taken[0]//60} hrs {time_taken[0]%60} min<br>Semester 2: {time_taken[1]//60} hrs {time_taken[1]%60} min<br>"
        x = dumps([success,schedules,time_taken,combo_count])
        return x
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
import random
import math
import os

def lcm(x,y):
    return x*y/(math.gcd(x,y))

def mod(a,b,c):
    return (a%b) is c

def add(a,b,c):
    return a+b is c

def equal(a,b):
    return a is b

def notequal(a,b):
    return not equal(a,b)

def divisible(a,b):
    return (a%b) is 0

def even(x):
    return x%2 == 0

def odd(x):
    return x%2 == 1

def prime(x):
    if(x is 1):
        return False
    for i in range(2,int(math.sqrt(x))+1):
        if(x%i is 0):
            return False
    return True

def less(a,b):
    return a<b

def greater(a,b):
    return a>b

def line(x,y):
    return x + y

def constraint(a,b):
    return equal(a,b)

def root(x):
    return math.sqrt(x)

def square(x):
    return x*x

def coprime(a,b):
    if(a<b):
        a,b = b,a
    if(a%b is 0):
        return False
    for i in range(2,int(math.sqrt(a)+1)):
        if(a%i):
            if(b%i is 0):
                return False
            x = a//i
            if(b%x is 0):
                return False
    return True

all_question = dict()

def extract_variable_name(question, variable_names):
    #----Here Name of all variable has been extracted----#
    for i in range(0,len(question)):
        if(question[i] != '#') :
            continue
        i  = i + 1;
        temp = ""
        while(i<len(question) and question[i] is not ' ' and question[i] is not '\t'):
            temp += question[i]
            i = i + 1;
        if(temp not in variable_names):
            variable_names.append(temp)
   
    #print(variable_names)
    for i in range(0,len(variable_names)):
        if('\t' in variable_names[i]):
            print("entered")
            variable_names[i] = variable_names[i].replace('\t','')

def get_category_of_each_variable(variable_names, all_constraints):
    #----Here whether a variable is a integer or an object is determined----#
    #integerClass = [x for x in all_constraints if "int" in x]
   # objectClass = [x for x in all_constraints if "object" in x]
   # print(integerClass)
   # print(objectClass)
    #integers_split = []
    #all_int_var = []
    #if(len(integerClass)):
     #   integers_split = str(integerClass[0])
      #  integers_split = integers_split.replace(',',' ')
       # integers_split = integers_split.replace('(',' ')
        #integers_split = integers_split.replace(')',' ')
        #integers_split = integers_split.split()
        
        
   # if(len(objectClass)>0):
    #    object_split =  str(objectClass[0])
     #   object_split= object_split.replace(',', ' ')
      #  object_split = object_split.replace('(', ' ')
       # object_split = object_split.replace(')', ' ')
        #object_split = object_split.split()
    
   
    #for i in range(1,len(integers_split)):
     #   all_int_var.append(integers_split[i])
    #all_object_var = []
    #for i in range(0,len(variable_names)):
     #   if(variable_names[i] in all_int_var):
      #      continue
       # all_object_var.append(variable_names[i])
    #print(all_int_var)
    #print(all_object_var)
    #return all_int_var, all_object_var
    all_int_var = []
    all_object_var = []
    toDelete = []
    toAdd = []
    for i in range(0, len(all_constraints)):
        constraint = all_constraints[i]
        if("int" in constraint):
            constraint = constraint.replace('(',' ')
            constraint = constraint.replace(')',' ')
            constraint = constraint.replace(',',' ')
            constraint = constraint.split()
            toAdd.append('range(' + constraint[1]+','+constraint[2]+','+constraint[3]+')')
            toDelete.append(all_constraints[i])
            all_int_var.append(constraint[1])
        if("float" in constraint):
            constraint = constraint.replace('(',' ')
            constraint = constraint.replace(')',' ')
            constraint = constraint.replace(',',' ')
            constraint = constraint.split()
            toAdd.append('precision(' + constraint[1] + ',' + constraint[2]+')')
            toAdd.append('range(' + constraint[1] + ',' + constraint[3] + ',' + constraint[4] + ')')
            toDelete.append(all_constraints[i])
            all_int_var.append(constraint[1])
    for i in range(0, len(toDelete)):
        all_constraints.remove(toDelete[i])
    for i in range(0, len(toAdd)):
        all_constraints.append(toAdd[i])
    for i in range(0,len(variable_names)):
        if(variable_names[i] not in all_int_var):
            all_object_var.append(variable_names[i])
    return all_int_var, all_object_var

def generate_int_var(all_int_var,pure_variable_function, new_variable_value):
    for i in range(0,len(all_int_var)):
        variable = all_int_var[i]
       # print(variable)
        tempD = pure_variable_function[variable]
        temp = [s for s in tempD if "range" in s]
        temp = str(temp[0])
        temp = temp.replace('(',' ')
        temp = temp.replace(')', ' ')
        temp = temp.replace(',',' ')
        temp = temp.split()
        l,r = int(temp[2]),int(temp[3])
        flag = True
        val = 0
        cnt = 0
        while flag :
            cnt = cnt + 1
            if(cnt is 10000):
                return False
            val = random.randint(l,r)
            flag = False
            temp = [s for s in tempD if "precision" in s]
            if(len(temp)):
                temp2 = str(temp[0])
                temp2 = temp2.replace('(',' ')
                temp2 = temp2.replace(')', ' ')
                temp2 = temp2.replace(',',' ')
                temp2 = temp2.split()
                val += random.randint(0,pow(10,int(temp2[2])))/(pow(10,int(temp2[2])))
            for j in range(0,len(tempD)):
                temp2 = tempD[j]
                if("range" in temp2 or "precision" in temp2):
                    continue
                temp2 = temp2.replace(variable, str(val))
               # print(temp2)
                if(eval(temp2) is False):
                    flag = True
                    break
        #print(val)
        new_variable_value[variable] = str(val)
    return True
    
def generate_object_variable(all_object_variable, pure_variable_function, new_variable_value):
    for i in range(0,len(all_object_variable)):
        variable = all_object_variable[i]
        tempD = pure_variable_function[variable]
        if(len(tempD) is 0):
            continue
        temp = str(tempD[0])
        temp = temp.replace('(', ' ')
        temp = temp.replace(')', ' ')
        temp = temp.replace(',',' ')
        temp = temp.split()
        sz = len(temp)-2;
        val = 1 + random.randint(1,sz)
        new_variable_value[variable] = temp[val]
    return True
    
def possible(new_variable_value, variable_names, dependent_function_variable):
    dependent_function_variables = list(dependent_function_variable)
    for i in range(0,len(dependent_function_variables)):
        function = dependent_function_variables[i]
        for j in range(0,len(variable_names)):
            if(variable_names[j] in function):
                function = function.replace(variable_names[j],new_variable_value[variable_names[j]])
        if(eval(function) is False):
            return False
    return True
    
def generate_question(question, constraint, qid):
    variable_names = []
    extract_variable_name(question, variable_names)
    #print(variable_names)
    all_constraints = constraint.split()
    all_int_var, all_object_var = get_category_of_each_variable(variable_names, all_constraints)
   
    #----Pure Variable Function are extraced---#
    pure_variable_function = dict()
    for i in range(0,len(variable_names)):
        pure_variable_function[variable_names[i]] = []
        for j in range(0,len(all_constraints)):
            if("int" in all_constraints[j] or "object" in all_constraints[j]):
                continue;
            if(variable_names[i] in all_constraints[j]):
                flag = True
                for k in range(0,len(variable_names)):
                    if(i is k):
                        continue
                    if(variable_names[k] in all_constraints[j]):
                        flag = False
                if(flag):
                    pure_variable_function[variable_names[i]].append(all_constraints[j])
    print(pure_variable_function)
    
    #----Done Extracting Pure Variable Functions---#
    #----Extracting Depending Variable Function---#
    dependent_variable_function = set()
    for i in range(0,len(variable_names)):
        for j in range(0,len(all_constraints)):
            if("int" in all_constraints[j] or "object" in all_constraints[j]):
                continue;
            if(variable_names[i] not in all_constraints[j]):
                continue
            if(variable_names[i] in all_constraints[j]):
                flag = False
                for k in range(0,len(variable_names)):
                    if(i is k):
                        continue;
                    if(variable_names[k] in all_constraints[j]):
                        flag = True;
                if(flag):
                    dependent_variable_function.add(all_constraints[j])
    #print(dependent_variable_function)
    #----Done Extracting Dependent variable function----#
    new_variable_value = dict()
    #print(all_int_var)
    iterations = 0
    while True : 
        flag1 = generate_int_var(all_int_var, pure_variable_function,new_variable_value)
        #print(new_variable_value)
        flag2 = generate_object_variable(all_object_var, pure_variable_function, new_variable_value)
       # print(new_variable_value)
        if(possible(new_variable_value,variable_names, dependent_variable_function)):
            break
        new_variable_value.clear()
        iterations = iterations + 1
        if(iterations is 50000 or flag1 is False or flag2 is False):
            return "No Question Can be generated Out of given constraints"
        
    temp_que = question.split()
    generated_question = temp_que
    for i in range(0,len(variable_names)):
        variable = variable_names[i]
        for j in range(0,len(generated_question)):
            word = generated_question[j]
            if(variable in word and '#' in word and (len(variable)+1 is len(word))):
                generated_question[j] = new_variable_value[variable]
    output = ""
    for i in range(0,len(generated_question)):
        output += generated_question[i] + ' '
    if(qid in all_question):
        all_question[qid].append(output)
    else :
        all_question[qid] = []
        all_question[qid].append(output)
    return output
    

import tkinter as tk

window = tk.Tk()
window.title("Similiar Problem Generation")
window.geometry("800x600")
window.grid()

label = tk.Label(window, text = "Question ID")
label.grid(row=0,column = 0, pady = 5)

entry = tk.Entry()
entry.grid(row = 0, column=1, pady =5)

label1 = tk.Label(window, text = "Enter the quesion")
label1.grid(row=2,column=0, pady = 5)

entry1 = tk.Text(window, height = 8, width = 70)
entry1.grid(row=2,column=1,pady=5)

label2 = tk.Label(window, text = "Enter the Constraints")
label2.grid(row=3,column=0,pady = 5)

entry2 = tk.Text(window, height=8, width = 70)
entry2.grid(row=3, column=1,pady = 5)

#tex.config(state=NORMAL)

def save_question():
     question1 = str(entry1.get("1.0","end-1c"))
     constraint1 = str(entry2.get("1.0","end-1c"))
     qid = str(entry.get())
     #cwd = os.getcwd()
     qidqf = qid+'Question.txt'
     qidcf = qid+'Constraint.txt'
     f = open(qidqf, 'w')
     f.write(question1)
     f.close
     f = open(qidcf,'w')
     f.write(constraint1)
     f.close() 
     entry.delete(0,tk.END)
     entry1.delete(1.0,tk.END)
     entry2.delete(1.0,tk.END)
     entry3.delete(1.0,tk.END)
   #  entry3.delete('1.0',tk.END)
     return 
     

def take_input():
    question1 = str(entry1.get("1.0","end-1c"))
    constraint1 = str(entry2.get("1.0","end-1c"))
    qid = str(entry.get())
    entry3.delete('1.0',tk.END)
    entry3.insert(1.0,generate_question(question1, constraint1,qid))
    #entry3.insert(1.0,"Good to go")
    #entry3.insert(1.0,constraint1)
    return

def retrieve():
    qid = entry.get()

    qidqf = qid+'Question.txt'
    qidcf = qid+'Constraint.txt'
    if(os.path.exists(qidqf) and os.path.exists(qidcf)):
        file1 = open(qidqf,"r")
        question1 = file1.read()
        file1.close()
        file1 = open(qidcf,"r")
        constraint1 = file1.read()
        file1.close()
        entry3.delete(1.0,tk.END)
        entry1.delete(1.0,tk.END)
        entry2.delete(1.0,tk.END)
        entry1.insert(1.0,question1)
        entry2.insert(1.0,constraint1)
    else:
        entry3.delete(1.0,tk.END)
        entry1.delete(1.0,tk.END)
        entry2.delete(1.0,tk.END)
        entry1.insert(1.0,"Not entered yet")
        entry2.insert(1.0,"Not entered yet")
    return 
    

button1 = tk.Button(window, text = "Sample Question", command = take_input)
button1.grid(row=4,column=1,pady=5)

label3 = tk.Label(window, text = "Similar Question")
label3.grid(row=5,column=0,pady=5)

entry3 = tk.Text(window, height=6, width = 70)
entry3.grid(row=5, column = 1,pady = 5)

button2 = tk.Button(window, text="Save", command = save_question)
button2.grid(row=6,column=1,pady=5)

button3 = tk.Button(window, text = "Browse", command = retrieve)
button3.grid(row=1, column=1,pady=5)

def clear_all():
     entry3.delete(1.0,tk.END)
     entry1.delete(1.0,tk.END)
     entry2.delete(1.0,tk.END)
     entry.delete(0,tk.END)

def save_sq():
    fileName = str(entry.get()) + " Sample Question.txt"
    Newfile = open(fileName, "w")
    Newfile.write(str(entry3.get(1.0,tk.END)))
    Newfile.close()
   # clear_all()
    return

button5 = tk.Button(window, text = "Save Sample Question", command = save_sq)
button5.grid(row=7, column = 1, pady = 5)     
     
button4 = tk.Button(window,text = "Clear",command = clear_all)
button4.grid(row=8, column=1,pady=5)
window.mainloop()
import unittest
import sys
import os 
sys.path.append(os.path.join('./production/logic'))
from entry import Entry 
from plan import Plan 
from routine import Routine

#TODO: turn this into class because of today l.12 & co

standard = Entry("00:05","standard")
besonders = Entry("00:06","besonders")

def createPlan(self,string:str):
    plan = Plan("today")
    special_element = None

    for i,e in enumerate(string):
        if e == 'E':
            ele = addToPlan(self,plan,i,string,Entry)
            if not ele == None:
                special_element = ele
        elif e=="R":
            addToPlan(self,plan,i,string,Routine)
    return plan,special_element

def addToPlan(self,plan,index,string,classType):
    element = []
    if not len(string) == index+1:
        n_char = string[index+1]
        if n_char.isdigit():
            c = int(n_char)
            for i in range(c):
                addTypeToPlan(self,plan,classType)
        elif  n_char == 'S' and classType == Entry:
            ele = besonders.clone()
            plan.add(ele)
            return ele
        else:        
            addTypeToPlan(self,plan,classType)
    else:        
        addTypeToPlan(self,plan,classType)

def addTypeToPlan(self,plan,classType):
    if classType is Routine:
        plan.add(self.routine)
    else:
        plan.add(standard.clone())

def test_listByInstance(self,step_list,instances:str):
    if instances[0].isdigit():
        self.assertEqual(len(step_list),int(instances[0]))
        instances = instances[1:]

    for i,e in enumerate(instances):
        if e == 'E':
            self.assertEqual(step_list[i].__class__,Entry)
        elif e=="R":
            self.assertEqual(step_list[i].__class__,Routine)
        else:
            pass

"""A utils class that helps to create plans and templates from text"""
try:
    from plan import Plan
    from routine import Routine
    from entry import Entry 
    import ParseText
except:
    from .plan import Plan
    from .routine import Routine
    from .entry import Entry 
    from . import ParseText

def parsePlanFromFileText(text):
    text = text.split("\n")
    theme = text[0]
    struc = generateStructure(text[2:])

    content_start_index = len(struc)+3
    content = text[content_start_index:]

    entries = ParseText.planLines_toEntries(content)

    plan = combineEntriesAndStructure(theme,struc,entries)
    # TODO: teste diese Bedingung ab
    if len(entries) > 0:
        plan.start = entries[0].start
        plan.updateStarts(entries[0].start,0)
    return plan

class Structure():

    def __init__(self,start,theme,count):
        self.start = start
        self.theme = theme
        self.count = count


def combineEntriesAndStructure(theme:str,structure:list,entries:list):
    entrie_index = 0
    plan = Plan(theme)
    for struc in structure:
        if struc.count == 1:
            plan.add(entries[entrie_index])
            entrie_index += 1
        elif struc.count >1:
            r = Routine(struc.theme)
            r.start = struc.start
            c = struc.count
            for i in range(c):
                r.add(entries[entrie_index+i])
            entrie_index+=c
            plan.add(r)
    return plan

def generateStructure(lines:list):
    struc = []
    for line in lines:
        eNSI = getEndNumberStartIndex(line)
        if not eNSI == 0:
            start = line[:5]
            theme = line[6:eNSI-1]
            count = int(line[eNSI:])
            struc.append(Structure(start,theme,count))
        else: 
            return struc
    print("everything parsed")
    return struc

def getEndNumberStartIndex(line:str):
    for i,char in enumerate(reversed(line)):
        if not char.isdigit():
            return -i
    return 0

def parseRoutineFromFileText(text:str):
    try:
        theme = text.split("\n")[0]
        r = Routine(theme)
        r.update(text[1:])
        return r
    except RuntimeError as err:
        print('parseRoutineFromFileText error',err)
        return Routine("parseRoutineFromFileText error")

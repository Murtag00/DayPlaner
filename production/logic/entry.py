class Entry():

    def __init__(self,duration:str,theme:str,start=None):
        self.duration = duration
        self.theme = theme
        self.start = start
    
    def clone(self):
        return Entry(self.duration,self.theme,self.start)
    
    def toString(self):
        return str(self.getText()+" "+ self.duration)

    def info(self):
        return str("Theme: "+self.theme+". Duration: "+self.duration+"\n")

    def getText(self):
        if self.start == None:
            return self.theme
        else:
            return str(self.start+" "+ self.theme)


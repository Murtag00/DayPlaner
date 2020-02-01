import kivy
kivy.require('1.11.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.recycleview import RecycleView
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window, Keyboard

import datetime

import sys
sys.path.append(".\\production\\logic")
# sys.path.append("production\\gui\\middle")#needs to be connected! to a full path!

from plan import Plan
from template import Template
from middle.rvTemplates import RV_Templates
from middle.planner import Planner
import Load
import os

try:
    templates = Load.loadTemplateDir("material\\") #on testing
except:
    templates = []
    try:
        os.mkdr("material\\")
    except:
        print("error cant mkdr")
# templates = Load.loadTemplateDir("E:\\Python\\DayPlaner\\material")
#templates = loadTemplateDir("material")

class DayPlannerGUI(Widget):

    b_save = ObjectProperty()
    b_load = ObjectProperty()

    template_list = ObjectProperty()
    planner = ObjectProperty()

    t_name = ObjectProperty()
    t_location = ObjectProperty()

    PLANNING = 0
    TEMPLATING = 1

    def __init__(self):
        super().__init__()
        data = self.template_list.rv_list.data
        for index,temp in enumerate(templates):
            data.append({'text': temp.getThemeDuration(),
            "on_press": self.getAddTemp(temp)})
        self.time = (datetime.datetime.today()+datetime.timedelta(days=1)).strftime("%d.%m.%Y")
        self.t_name.text= self.time
        self.mode = DayPlannerGUI.PLANNING
        self.loadPlan()

        keyboard = Window.request_keyboard(self._keyboard_released,self)
        keyboard.bind(on_key_down = self.on_key_down)
        self.planner.b_mode.on_press = self.changeMode

    def _keyboard_released(self):
        self.focus = False

    def on_key_down(self,window,keycode,text,modifiers):
        #print(keycode)
        if "ctrl" in modifiers:
            char = keycode[1]
            if  not char == None:
                switcher = {
                '#':self.planner.updateWidgets,
                'n':self.incrementDay,
                'p':self.decrementDay,
                'spacebar':self.planner.update,
                't':self.setInputToTime}
                if self.mode == DayPlannerGUI.PLANNING:
                    switcher['s']=self.savePlan
                    switcher['l']=self.loadPlan
                else:
                    switcher['s']=self.saveTemplate
                func = switcher.get(char) 
                if not func == None:
                    func()

    def incrementDay(self):
        (days,months,years) = self.time.split(".")
        new_time = datetime.date(int(years),int(months),int(days))+ datetime.timedelta(days=1)
        self.time = new_time.strftime("%d.%m.%Y")
        if self.mode == DayPlannerGUI.Planning:
            self.setInputToTime()

    def decrementDay(self):
        (days,months,years) = self.time.split(".")
        new_time = datetime.date(int(years),int(months),int(days))- datetime.timedelta(days=1)
        self.time = new_time.strftime("%d.%m.%Y")
        if self.mode == DayPlannerGUI.Planning:
            self.setInputToTime()

    def setInputToTime(self):
        self.planner.t_theme.text=self.time
        self.t_name.text=self.time


    def getAddTemp(self,temp):
        def addTemp():
            temp_2 = self.planner.atOrSet(temp)
        return addTemp    

    def savePlan(self):
        if self.mode == self.PLANNING:
            path = "plans\\"+self.planner.plan.theme
            Load.save(path,self.planner.plan.getFileText())

    
    def loadPlan(self):
        if self.mode == self.PLANNING:
            path = "plans\\"+self.t_location.text + self.t_name.text
            plan = Load.parsePlan(Load.loadText(path))
            self.planner.setPlan(plan)

    def saveTemplate(self):
        path = "material\\"+self.planner.template.theme+"template"
        Load.save(path,self.planner.template.getFileText())

    def changeMode(self):
        t = self.planner.b_mode.text
        if t == "P/T":
            self.mode = DayPlannerGUI.TEMPLATING
            self.planner.changeMode()
            self.b_load.opacity = 0
            self.t_name.opacity = 0
            self.b_save.text="save template"
            self.b_save.on_press = self.saveTemplate
        else:
            self.mode = DayPlannerGUI.PLANNING
            self.planner.changeMode()
            self.b_load.opacity = 1
            self.t_name.opacity = 1
            self.b_save.text="save plan"
            self.b_save.on_press = self.savePlan

class MainGUIApp(App):

    def build(self):
        return DayPlannerGUI()


if __name__ == '__main__':
    MainGUIApp().run()
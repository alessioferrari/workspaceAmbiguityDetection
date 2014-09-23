from Tkinter import *
import threading
class progressBar():
    def __init__(self):
        self.pp=pBar()
        self.pp.percent=0
        self.pp.start()
    def setPercent(self,perc):
        self.pp.setPercent(perc)
    def getPercent():
        return self.pp.percent
class pBar(threading.Thread):
    def run(self):
        self.main=Tk()
        self.frame=Frame(self.main)
        self.frame.pack()
        self.label = Label(self.frame,text="")
        self.label.pack()
        self.title="Analysis"
        self.main.title(self.title)
        self.imm=Canvas(self.frame,height=20,width=300)
        self.imm.pack()
        self.back=self.imm.create_rectangle(1,3,300,20)
        self.barr=self.imm.create_rectangle(1,1,1,20,fill="darkgreen")
        self.refresh()
        self.main.mainloop()
    def refresh(self):
        self.imm.coords(self.barr,1,1,self.percent*3,20)
        self.label.configure(text=str(self.percent)+"%")
        self.main.title(self.title+" - "+str(self.percent)+"%")
        if self.percent>=100:
            self.main.quit()
        self.main.after(100, self.refresh)
    def setPercent(self,perc):
        self.percent=perc
#!/usr/bin/env python
""" test display of tableDice.pov """

import Tkinter as Ttk
import os, sys, getopt, time, datetime
import subprocess

class Die:
    """
    select a value 1-6 from a menu or radiobutton
    toggle red/white
    display chosen die
    """
    def __init__(self, num, master, myframe, val=6, red=True):
	self.val=Ttk.IntVar()
        self.val.set(val)
	self.red=Ttk.BooleanVar()
        self.red.set(red)
        top=Ttk.Frame(myframe)
	label=Ttk.Label(top,text='%d'%num)

	menub=Ttk.Menubutton(top, textvariable=self.val, relief=Ttk.RAISED)
	#menub.menu=Ttk.Menu(menub, tearoff=0)
        amenu=Ttk.Menu(menub, tearoff=0)
        menub.config(menu=amenu)
        #a=menub.menu.add_radiobutton(label='None', variable=self.val, value=0)
        a=amenu.add_radiobutton(label='None', variable=self.val, value=0)
        for ii in range(6):
            #a=menub.menu.add_radiobutton(label='%d'%(ii+1), variable=self.val, value=ii+1)
            a=amenu.add_radiobutton(label='%d'%(ii+1), variable=self.val, value=ii+1)
	self.redbutton = Ttk.Button(top, command=self.toggleRed)
        self.toggleRed();

        label.grid(row=0)
        menub.grid(row=1)
	self.redbutton.grid(row=2)
        top.grid(row=0,column=num-1)
    def getVal(self):
	return self.val.get()
    def getRed(self):
	return self.red.get()
    def toggleRed(self):
        rw= not self.red.get()
        self.red.set(rw)
        if rw:
            self.redbutton.configure(bg='red', text='Red', fg='white')
        else:
            self.redbutton.configure(bg='white', text='White', fg='black')


def computeString():
    """
    From all dice shown, use values to compute the string
    that will go to tableDice.pov
    """

class App:
    def __init__(self, master):
	# frame for dice
        diceFrame=Ttk.Frame(master)
        diceFrame.pack(side=Ttk.TOP)
	# label for string
        self.result=Ttk.IntVar()
        self.result.set('')
        self.resultLab = Ttk.Label(master, textvariable=self.result)
        self.resultLab.pack(side=Ttk.TOP)
	# canvas for picture
        self.imView=Ttk.Canvas(master)
        self.imView.pack(side=Ttk.TOP)
	# picture
        self.img=Ttk.PhotoImage(file='tableDice.gif')
        self.imgID=self.imView.create_image(0,0, image=self.img, anchor='nw')
        #self.imView.bind('<Button 1>', self.selectDice)
	# button to make picture
        self.pushMe=Ttk.Button(master, text='Make it so, No. 1', command=self.seeTableDice)
        self.pushMe.pack(side=Ttk.TOP)
	# six dice
        self.diceb=[Die(ii+1, self, diceFrame, ii+1) for ii in range(6)]
        self.seeTableDice()

    def seeTableDice(self):
        num=0
        for cc in self.diceb:
            sel=0 if cc.getRed() else 1
            val=cc.getVal()
            num=num*14 + val+7*sel
        print ' => num, ',num
        seeTableDice(num)
        self.img=Ttk.PhotoImage(file='tableDice.gif')
        self.imView.itemconfig(self.imgID,image=self.img)

def seeTableDice(num=0):
    command1= 'povray +H%d +W%d -GA -D +A +K%d tableDice.pov'%(dtw ,dtw*1.333,num)
    command2= 'convert tableDice.png tableDice.gif'
    subprocess.call(command1,shell=True)
    subprocess.call(command2,shell=True)

if __name__ == '__main__':
    dtw=250
    root = Ttk.Tk()
    #seeTableDice()
    root.title('testTableDice')
    app = App(root)
    root.mainloop()


#!/usr/bin/env python
""" test partitioned display of tableDice.pov.
    Further development from original testTable.py
    to use the tableDice.pov input file as a template
    to run run POVray multiple times to generate smaller images
    that can be stitched together to form the full image.
"""



import Tkinter as Ttk
import os, sys, getopt, time, datetime
import subprocess
import math
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

top=[]
bottom=[]
camera=[]
angle=0
lookat=[]
eye=[]
sky=[]
def getpovIn():
    ''' read pov input file in sections '''
    global eye,lookat,sky,angle
    filep=open('tableDice.pov')
    for line in filep:
        if 'camera {' not in line: top.append(line)
        else:
            camera.append(line)
            break
    for line in filep:
        if '}' not in line:
            fields = line.strip().split(None,1)
            # toss comments
            # find data for eye, look_at, angle, sky, AR
            if fields[0] == 'location':
                eye=getvec(fields[1])
            elif fields[0] == 'look_at':
                lookat = getvec(fields[1])
            elif fields[0] == 'sky':
                sky = getvec(fields[1])
            elif fields[0] == 'angle':
                angle = float(fields[1])
        else:
            camera.append(line)
            break
    for line in filep:
        bottom.append(line)

    print len(bottom)
    print eye
    print lookat
    print sky
    #sys.exit(1)

def getvec(fields):
    ''' extract three components of a vector from three fields.
        Eliminate '<', and ','
    '''
    return [float(each.replace('<','').replace(',','').replace('>','')) for each in fields.split(',')]

def subpov(i=1,xd=-1,yd=-1):
    ''' substitute values for camera parameters and generate subregion pov file
    '''
    lambdaI=angle*0.5
    EL = []
    elen=0
    slen=0
    for ind in range(3):
        part=lookat[ind]-eye[ind]
        EL.append(part)
        elen+=part*part
        slen+=sky[ind]*sky[ind]
    elen=math.sqrt(elen)
    slen=math.sqrt(slen)
    print 'elen, slen:',elen,slen
    # R= el/|el| X sky
    R=[]
    rlen=0
    for ind in range(3):
        part=EL[(ind+1)%3]/elen*sky[(ind+2)%3]/slen \
            -EL[(ind+2)%3]/elen*sky[(ind+1)%3]/slen 
        R.append(part)
        rlen+=part*part
    print R, rlen
    rlen=math.sqrt(rlen)
    # Lprime = Lorig + |EL| * tan(lambdaI)*R + 3/4*|EL|*tan(lambdaI)*sky
    Lprime=[]
    for ind in range(3):
        part=lookat[ind] + elen*math.tan(lambdaI*math.pi/180.)*(R[ind]/rlen*xd + 0.75*sky[ind]/slen*yd)
        Lprime.append(part)

    filep=open('tableDice%1d.pov'%i,'wb')
    for each in top:
        filep.write(each)
    filep.write(camera[0])
    filep.write('    location <%f, %f, %f>\n'%(eye[0],eye[1],eye[2]))
    filep.write('    sky <%f, %f, %f>\n'%(sky[0],sky[1],sky[2]))
    filep.write('    look_at <%f, %f, %f>\n'%(Lprime[0],Lprime[1],Lprime[2]))
    filep.write('    angle %f\n'%lambdaI)
    filep.write('    up y*.75\n    right -x\n  }\n')
    for each in bottom:
        filep.write(each)

def seeTableDice(num=0,dtw=250):
    # parse pov file
    getpovIn()
    # for each partition
    # here hardwired to 4
    # substitute subregion parameters into pov file
    subpov(1,-1, 1)
    subpov(2, 1, 1)
    subpov(3,-1,-1)
    subpov(4, 1,-1)
    # run pov to generate subimage - this could be parallelized to good advantage
    #command1= 'povray +H%d +W%d -GA -D +A +K%d tableDice.pov'%(dtw ,dtw*1.333,num)
    command1= 'povray +H%d +W%d -GA -D +A +K%d tableDice1.pov'%(dtw/2 ,dtw*2/3,num)
    subprocess.call(command1,shell=True)
    command1= 'povray +H%d +W%d -GA -D +A +K%d tableDice2.pov'%(dtw/2 ,dtw*2/3,num)
    subprocess.call(command1,shell=True)
    command1= 'povray +H%d +W%d -GA -D +A +K%d tableDice3.pov'%(dtw/2 ,dtw*2/3,num)
    subprocess.call(command1,shell=True)
    command1= 'povray +H%d +W%d -GA -D +A +K%d tableDice4.pov'%(dtw/2 ,dtw*2/3,num)
    subprocess.call(command1,shell=True)
    # assemble images into final
    #command2= 'convert tableDice.png tableDice.gif'
    command2= 'montage tabledice[1234].png  -geometry %dx%d tableDice.gif'%(dtw*2/3, dtw/2)
    subprocess.call(command2,shell=True)

if __name__ == '__main__':
    dtw=250
    root = Ttk.Tk()
    #seeTableDice()
    root.title('testTableDice')
    app = App(root)
    root.mainloop()


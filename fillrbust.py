#!/usr/bin/env python
""" play Fill 'R Bust"""
# fillrbust.py
# encode the rules for fillrbust
#  v0 - June 27, 2017
#    Text UI
#  v1 - July 5
#    added GUI
#    most functionality implemented; much not tested; look for beta testers
#  v2 - July 7
#    added ai player
#  v2.1 - July 12
#    assigned risk paramer to ai player
#  v2.2 - July 19
#    added risk parameters for rolling dice, taking vengeance, continuing a turn
#  v2.3 - July 25
#    mostly bug fixes
#  v3 - July 29
#    provide help with game play, GUI
#    show dice as unrolled after draw card
#    disabled selection of dice during MustBust
#    >, < keys increase/decrease font size in instructionbox
#  v3.2 - July 30
#    help on individual buttons
#  v3.3 - Mar 2, 2018
#    delete or rename player selected by right button
#        delete player if new name is null
#        change from real to AI not implemented, yet
#        ERROR if current player is deleted in the middle of the turn
#    extend game after win
#        Winner banner has "Extend Game" button
#    play again after win
#        Winner banner has "new Game" button
#  v3.4 - April 14, 2019
#    change background colors of frames and buttons where dice, cards and instructions
#       - a1, a2, cardframe, diceframe, scoreframe, optionsframe, 
#  v3.5 - March 1, 2020
#    save and resume game
#    FIX VENGEANCE
#       - gui allows one to take the points and quit
#       - fixed
#    option to select dice display at runtime
#       (if you know the available option names:
#       Orig, FreeCad, POV, Reflect, Trans, Big
#    FIX new game after end
#       - dont remember previous score and add it to first score of new game
#       - fixed
#  dev:
#  TODO:
#    FIX ai play when aiName is first player
#       - only problem is first play; does not run ai.
#    make colors more attractive
#    FIX name delete:
#       - even if current player is deleted mid-turn
#    add option to Game menu to delete a player
#    FIX name change:
#	- enable switch to/from AI
#    show dice probabilities
#    play with remote player
#    draw dice nicer
#       o group retained dice seperately
#       o draw thrown dice in a group other than a (boring) row

import random
from collections import OrderedDict
from copy import deepcopy
import tkinter as Ttk
from tkinter.scrolledtext import ScrolledText
import os, sys, getopt, time, datetime
import subprocess

about='    fillrbust.py\n \
A computer controlled version of Fill\'RBust\n\n \
    version 3.5'
therules='see official rules from Bowman Games Inc: instr.pdf\n \
Fill\'RBust uses six standard cubic dice and 54 cards (as described below)\n \
It is turn based.\n \
\n \
A \'fill\' is when all six dice are scoreable (see dice scoring below).\n \
A \'bust\' is when the dice are rolled and none are scoreable.\n \
RULE 1. You Must turn over a DRAW CARD before each turn and after each "FILL". \
The card you turn over will determine your course of play. \
How you play each card is explained later under PLAYING THE DRAW CARDS.\n \
\n \
RULE 2: You MUST score every time you toss the dice. After turning over a card, you begin your turn by tossing all six dice.\n \
You score by tossing 1s, 5s, any triples or a straight (1,2,3,4,5 and 6 thrown in a single toss of all six dice).\n  \
\n \
Dice scoring:\n \
        1 = 100\n \
        5 = 50\n \
        three of a kind = 100x N, except three 1\'s = 1000\n \
        straight (in a single roll)= 1500\n \
\n \
RULE 3: \n \
 After each toss you MUST remove some or all of the scoring dice.  \
 Set aside all the scoring dice you have chosen and add up their points. \
 You  can  decide  to  take  these  points and  add  them  to the  scoresheet  ending your   turn.  \
 Or,  you  can  take  a chance  and  try to  score  more  points with the remaining  dice.\n \
\n \
 HOW TO SCORE A FILL\n \
If you can continue to score on every toss of the dice, and you eventually set aside all six dice, YOU HAVE SCORED A  "FILL". \
After scoring a "FILL" you can decide to take the points scored during that turn and add them to the scoresheet, ending your turn. \
Or, you can take a chance and try to score more points by turning over another DRAW CARD and start by tossing all six dice again.  \
There is no limit to the number of "FILLS" that may be scored in a turn.\n \
\n \
WHAT IS A "BUST"?\n \
 If on any toss you DO NOT roll any scoring dice, that toss is a "BUST". \
 When you "BUST" during a turn, you lose ALL the points you scored in that turn. \
 (Exception is during MUST BUST, see below) \
 You do not lose any points that were already added to the scoresheet.  \
 After a "BUST", your turn ends and you pass the dice to the next player.\n \
\n \
Cards:\n \
    Bonus 300, 400, 500\n \
    	if filled, get additional bonus points\n \
    Fill 1000\n \
    	no score unless filled; add 1000 bonus points\n \
    DoubleTrouble\n \
    	no score unless filled twice. Score is doubled and added to scoresheet.\n \
    	turn can continue without risk to these points.\n \
    Must Bust\n \
    	no risk; a bust just ends the turn; you still get the points\n \
        continue rolling until no scoring dice, ie BUST.\n \
        all scorable dice must be accepted as they are rolled.\n \
    No Dice\n \
    	forfeit turn immediately\n \
    Vengeance 2500\n \
    	must fill to score\n \
        if filled, player gets score and leader loses 2500 points.\n \
        After Vengeance fill, player may continue turn without risk of points just made.\n \
\n \
 12- 300 pt. "BONUS" cards\n \
 10- 400 pt. "BONUS" cards\n \
  8- 500 pt. "BONUS" cards\n \
  4- MUST BUST cards\n \
  6- FILL 1000 cards\n \
  4- VENGEANCE 2500 cards\n \
  8- NO DICE cards\n \
  2- DOUBLE TROUBLE cards'
theGUI='The Graphical User Interface (GUI) has been developed to lead you through the game. \
On the left are the buttons that you use to play the game: the cards, the dice, \
and two buttons to select an appropriate action when there is a decision to make. \
On the right is the information to show you who is winning (and who is/are not).\n\n \
The first part of every turn is to draw a card.  Press the deck of cards and you get a new card \
if that is the appropriate next step. Look in the instruction window at the bottom; it will guide you. \
The rules dictate what you can do for each card. The option buttons below the dice help you actually do it. \
Typically, after drawing a card, you want to roll the dice, so there is an option button that says "Roll Dice". \
Click it. The dice will indicate what was rolled. Any dice that might score are highlighted. \
Clicking on the dice will highlight/de-highlight them. The potential score will change based on your selection. \
Highlighted dice will be reserved; the rest will be rolled (if that is an allowed choice). \
Again, see the instruction window below; it will tell you. \
When you roll again, dice you highlighted will be moved to the right and shown in a fence, \
and the result of rolling the remaining unhighlighted dice will be shown on the left.\n\n \
When you decide to take a score, it will be posted on the scoresheet to the right \
and the next player gets a turn. The new player\'s name will turn green. \
(Only scores are posted; nobody likes to be reminded of their failures.)\n\n \
The "Game" menu at the top allows you to add players and change the ultimate score that wins the game. \
Any player name that starts with "ai" will be computer controlled. \
So Aiden and Aisha, don\'t forget to capitalize the first letter of your name. \
A number (1-9) appended to the end of an aiName will indicate how much risk that ai player is willing to accept \
when deciding to roll again, take vengeance, continue after a Fill, etc. \
'
diceHelp='             Dice:\n \
The dice are displayed and modeled as typical cubic dice. \n \
Clicking any unrolled die will generate the first roll using all six dice. \
Subsequent to the first roll, clicking will select and de-select the individual dice to be reserved for scoring. \
Selected dice are shown red and will not be rolled. \
Of the rolled dice, at least one must be reserved for scoring (it\'s a rule). \
Dice that were reserved and not rolled are displayed with a yellow border and grouped to the right.'
cardHelp='             Card:\n \
The cards are displayed and modeled as a shuffled Fill\'RBust deck. \
When it is appropriate to draw a card, clicking on the card will show the next card in the shuffled deck. \
When all 54 cards have been exhausted, the deck is reshuffled.'
optionHelp='           Option Buttons:\n \
There are two option buttons because there are usually two options from which the player must choose. \
The effect of clicking the option depends on the state of the game. \
The button text describes the effect consisely. \
The instruction box below them describe the decision a bit more. \
Sometimes there is only one option, so one button is disabled.'
goalHelp='You can change the score at which someone is called the winner\n \
(and the rest are not).\n \
At the end of the game, ie when someone\'s score exceeds the goal and the \'Winner\' screen appears,\n \
right clicking in it will allow you to change the goal. This allows for sore losers!'
playerHelp='Any time during a game, another player can jump in - with zero score of course.\n\n \
Prepending \'ai\' to a name makes that player computer controlled. \
A number at the end of an ai player name indicates the risk that player will accept for decisions \
such as whether to roll again, take vengeance, or continue after a FILL. Default value is 5. \
Right click allows name change. ERROR ALERT: can\'t change player from real to AI.'
quitHelp=' Doh! It quits; goes away; exits; beats a hasty retreat, makes like a tree and leaves, makes like a buffalo turd and hits the dusty trail.\n\nWhich part of quit don\'t you understand?'
helpHelp='Obviously you found that \'specific\' help describes individual buttons.\n \
\'Rules\' describes the rules of the game.\n \
\'Synopsis\' describes how the game is implemented with this Graphical User Interface'

class Player:
    """
    Player defined by age, score,
      and 'artificial-ness'
    """
    def __init__(self,name,score=0):
        self.name=name
        self.score=score
        self.isai=False
    def update(self,score):
        self.score+=score
        if self.score < 0:
            self.score=0

class AIPlayer(Player):
    """
    Computer controlled player
       to make choices based of an assignment of risk
    """
    def __init__(self,name,risker=5, score=0):
        Player.__init__(self,name, score=score)
        self.risker=risker
        self.isai=True
    def listResp(self,risky='y',conservative='n'):
        return ''
    def rollRisk(self, ndice):
        """
        decide whether to roll or not
        """
        #Use probability of a favorable roll
        p=1.-.66667**ndice
        return p
    def ynResp(self,risky='y',conservative='n',rtype=None,debug=False):	#{
        """
        risky or conservative = 1 or 0
        """
        import math
        if testing:
            prompt='  respond risky =',risky,' or conservative =',conservative
            return int(raw_input(prompt))
        # base number = 10
        prob=10
        risker=self.risker
        nrisk=1
        dprint='player risk=',self.risker
        if debug:
            print('rtype in ynResp:',type(rtype),rtype)
        if type(rtype) is dict:
            if rtype['name'] == 'roll':
                # factor in number of dice for roll probability
                rprob= self.rollRisk(rtype['ndice'])*10
                risker+=rprob
                nrisk+=1
                dprint+=' roll risk is',rprob
                if debug:
                    print(' prob of scoring with %d dice is %f'%(rtype['ndice'],rprob))
            if rtype['name'] is not 'vengeance':
                # factor in the points at risk
                # linear such that r(0)=10, r(1000)=0
                pprob=max(0.,10.-rtype['score']*.01)
                risker+=pprob
                nrisk+=1
                dprint+=' point risk is',pprob
            # relative to the leaders score
            # quadratic with log of ratio player:leader such that
            #r(.1)=10, r(10)=10, r(1)=1
            app=rtype['app']
            if app.maxScore > 0 and app.pui[app.player].player.score>0:
                rtio=math.log10(float(app.pui[app.player].player.score)/float(app.maxScore))
                nprob=9*rtio*rtio +1
            else:
                nprob=3
            risker+=nprob
            nrisk+=1
            dprint+=' nearness to leader risk is',nprob
            # and how close leader is to winning
            #linear with ratio of leader to goal score
            cprob=float(app.maxScore)/float(app.goal.cget('text'))*10
            if app.player in app.leadingPlayers:
                cprob=10-cprob
            risker+=cprob
            nrisk+=1
            dprint+=' nearness to goal risk is',cprob
            if debug:
                print(dprint)
        if random.triangular(0,10,risker/nrisk)>5:
            if debug: print('Respyn says ',risky)
            return risky
        else:
            if debug: print('Respyn says ',conservative)
            return conservative
    #}

def respond(player, question='y n'):
    if players[player].isai:
        # parse potential answer from question
        print(question,)
        answers=question.split()
        if answers[0]=='list':
            response=players[player].listResp()
        else:
            response= answers[players[player].ynResp(1,0)]
            response= players[player].ynResp(answers[0])
        print('%s said %s'%(player,response))
        return response 
    else:
        response= raw_input(question)
        if response == 'q': sys.exit(0)
        return response

class Cards:
    def __init__(self,deck=[]):
        if len(deck)==0:
            self.deck=self.shuffle()
        else:
            self.deck=deck
    def shuffle(self):
        '''build a random deck of 54 cards'''
        deck= [each for each in range(54)]
        random.shuffle(deck)
        return deck
    def draw(self):
        '''remove a card and return its type'''
        id=self.deck.pop()
        if debug: print("DEBUG: %d card left in deck after card %d (=%s) was drawn"%(len(self.deck), id, ctype(id)))
        if len(self.deck)<1:
            self.deck=self.shuffle()
        return id

def ctype(id):
    if id<12: return "Bonus 300"
    if id<22: return "Bonus 400"
    if id<30: return "Bonus 500"
    if id<34: return "Must Bust"
    if id<40: return "Fill 1000"
    if id<44: return "Vengeance"
    if id<52: return "No Dice"
    return "Double Trouble"

#states
NEXTPLAYER=1
DRAWCARD=2
DREWVENGEANCE=3
ROLLFIRST=4
ROLLSOME=5
FILLED=6
BUSTED=7
ROLLED=8
MUSTBUST=9
DOUBLETROUBLE=10
WINNER=11

def outscore(orig,index,slen):
    '''rip out slen characters of orig string starting at index'''
    sdti=''
    sdti=orig[:index]
    for ii in range(slen):
        sdti+='x'
    sdti+=orig[index+slen:]
    return sdti

class Dice:
    def __init__(self):
        '''Initialize a set of six dice.
           Define what is scoreable.
           Roll all six and reserve none.
           '''
        self.score=0
        self.reserved=[]
        self.dice=self.roll()
        self.scores=OrderedDict()
        self.scores['111']=1000
        self.scores['222']=200
        self.scores['333']=300
        self.scores['444']=400
        self.scores['555']= 500
        self.scores['666']=600
        self.scores['123456']=1500
        self.scores['1']=100
        self.scores['5']=50
    def roll(self):
        '''pick a random number 1-6
           for each die that has not been reserved.
           return the new and the reserved.'''
        num=6-len(self.reserved)
        dice=sorted([random.randint(1,6) for ii in range(num)])
        return dice+self.reserved
    def str2dice(self,dstr):
        '''Convert the string of numbers to a list of numbers'''
        numtoroll=6-len(self.reserved)
        self.dice=[int(ii) for ii in dstr[:numtoroll]]+self.reserved
    def reserve(self,dstr):
        ''' reserve the listed dice for scoring'''
        #print('reserve ',dstr)
        for each in dstr:
            self.reserved.append(int(each))
    def scored(self, dlist):
        ''' Return the score
            and the portion of list that scores'''
        global debug
        stdice=''
        dlist.sort()
        if debug: print('given dlist:', dlist)
        for ii in range(len(dlist)-1,-1,-1):  # backward
            if dlist[ii]>6-len(self.reserved)-1:
               del(dlist[ii])	#dont count something reserved from before
        if debug: print('used dlist:', dlist)
        for each in dlist:
            stdice+='%d'%self.dice[each]
        score=0
        used=''
        plist=[]
        for each in self.scores.keys():
            nomore=False
            while not nomore:
                index=stdice.find(each)
                if index < 0:
                    nomore=True
                    continue
                # score a part and mark it out
                score+=self.scores[each]
                stdice=outscore(stdice,index,len(each))
                used+=each
                for ind in range(len(each)):
                    plist.append(index+ind)
        return score,used,plist

class App:
    def __init__(self, master,names=[],goal=0, scores=[], current=""):
        ''' init process is to set the goal score and the players'''
        self.master=master
        if len(names)==0 or goal==0:
            self.suf=self.mkAddPlayer(self.master,names)
        else:
            self.startplay(names,goal,scores,current)
        self.master.bind('<Key-d>', self.setDebug)
    def mkAddPlayer(self,master,names=[]):
        ''' GUI to add a player and/or set winning score'''
        suf=Ttk.Frame(master)
        suf.pack()
        self.a1=Ttk.Frame(suf)
        self.b1=Ttk.Frame(suf)
        self.labels=Ttk.Label(self.a1,text='Set winning score:')
        self.scoreg=Ttk.StringVar()
        entrgoal=Ttk.Entry(self.a1,textvariable=self.scoreg)
        self.labels.pack(side=Ttk.LEFT)
        entrgoal.pack(side=Ttk.LEFT)
        labelp=Ttk.Label(self.b1,text='add a player:')
        self.play2=Ttk.StringVar()
        entrplay=Ttk.Entry(self.b1,textvariable=self.play2)
        labelp.pack(side=Ttk.LEFT)
        entrplay.pack(side=Ttk.LEFT)
        entrplay.bind('<Key-Return>',self.addplay)
        self.listplay=Ttk.StringVar()
        self.playlist=Ttk.Listbox(suf,height=5,width=16, \
           listvariable=self.listplay)
        self.goplay=Ttk.Button(suf,text='Go Play', command=self.startplay)
        self.a1.pack(side=Ttk.TOP)
        self.b1.pack(side=Ttk.TOP)
        self.playlist.pack(side=Ttk.TOP)
        self.goplay.pack(side=Ttk.TOP)
        for each in names:
            self.playlist.insert(Ttk.END,each)
        return suf
    def addplay(self, event):
        eent=self.play2.get()
        #print('add: ',eent)
        self.playlist.insert(Ttk.END,eent)
        self.play2.set('')
    def startplay(self, names=[],goal=None,scores=[],current=""):
        ''' get list of players and goal from startup frame,
            and build play GUI'''
        if len(names)==0:
            names= self.playlist.get(0,Ttk.END)
            try:
                goal=int(self.scoreg.get())
            except ValueError:
                print('input the score to win')
                self.labels.configure(fg='red')
                return
            self.suf.destroy()
        self.reinit(self.master,goal=goal,
                    names=[each for each in names]
                    ,scores=scores, whogoesfirst=current)
    def reinit(self, master \
        ,goal=5000 \
        ,names=['Audrey','Nancy'] \
        ,scores=[0, 0] \
        ,cards=[] \
        ,whogoesfirst=""):
        ''' Given setup parameters (goal and player list),
            build the playing gui and start the game.
            The initial state is DRAWCARD'''
        
        global deck, state, orig_button_color
        self.names=names
        deck=Cards(cards)
        state=DRAWCARD
        a1 = Ttk.Frame(master, bg='black')
        b1 = Ttk.Frame(master,height=80)
        a1.pack(side=Ttk.TOP)
        b1.pack(side=Ttk.TOP,fill=Ttk.BOTH,expand=True)

        a2 = Ttk.Frame(a1, bg='black')
        b2 = Ttk.Frame(a1)
        a2.pack(side=Ttk.LEFT)
        b2.pack(side=Ttk.LEFT)

        self.menuframe = Ttk.Frame(a2, relief=Ttk.SUNKEN, borderwidth=2)
        self.cardframe = Ttk.Frame(a2, bg='black')
        self.diceframe = Ttk.Frame(a2, bg='black')
        scoreframe = Ttk.Frame(a2, bg='black')
        self.optionsframe = Ttk.Frame(a2, bg='black')
        self.menuframe.pack(side=Ttk.TOP,expand=True, fill=Ttk.X)
        self.cardframe.pack(side=Ttk.TOP)
        self.diceframe.pack(side=Ttk.TOP)
        scoreframe.pack(side=Ttk.TOP)
        self.optionsframe.pack(side=Ttk.TOP)

        # menu bar
        gamemenub = Ttk.Menubutton(self.menuframe, text='Game')
        helpmenub = Ttk.Menubutton(self.menuframe, text='Help')
        filler=Ttk.Label(self.menuframe,text=' ')
        gamemenub.pack(side=Ttk.LEFT)
        helpmenub.pack(side=Ttk.LEFT)
        filler.pack(side=Ttk.LEFT, expand=True)
        self.gamemenu=Ttk.Menu(gamemenub,tearoff=0)
        self.gamemenu.add_command(label='New Player', command=self.addplayerGui)
        self.gamemenu.add_command(label='Winning Score', command=self.resetgoal)
        self.gamemenu.add_command(label='Save Game', command=self.savegame)
        self.gamemenu.add_command(label='Quit', command=sys.exit)
        gamemenub.configure(menu=self.gamemenu)
        self.helpmenu=Ttk.Menu(helpmenub,tearoff=0)
        self.helpmenu.add_command(label='Rules', command=self.showRules)
        self.helpmenu.add_command(label='Synopsis', command=self.showSynopsis)
        self.helpmenu.add_command(label='specific', command=self.helpGui)
        self.helpmenu.add_command(label='about', command=self.showAbout)
        helpmenub.configure(menu=self.helpmenu)

        # show dice
        # load the images
        #nums={}
        #nums[1]='one'
        #nums[2]='two'
        #nums[3]='three'
        #nums[4]='four'
        #nums[5]='five'
        #nums[6]='six'
        #nums['undie']='undie'
        nums=list(enumerate(['undie','one','two','three','four','five','six']))
        self.flagsup=[]
        self.flagdown=[]
        #for num in range(1,7):
        for num,name in nums:
            #self.flagsup.append(Ttk.PhotoImage(file='%s.gif'%nums[num]))
            self.flagsup.append(Ttk.PhotoImage(file='%s/%s.gif'%(dicedir,name)))
            self.flagdown.append(Ttk.PhotoImage(file='%s/%sb.gif'%(dicedir,name)))
        self.diceb=[Die(self) for ii in range(6)]

        # show card
        self.cardimage={}
        self.cardimage['title'         ]=Ttk.PhotoImage(file='%s/title.gif'%carddir)
        self.cardimage['Must Bust'     ]=Ttk.PhotoImage(file='%s/mustbust.gif'%carddir)
        self.cardimage['Bonus 500'     ]=Ttk.PhotoImage(file='%s/bonus500.gif'%carddir)
        self.cardimage['Bonus 400'     ]=Ttk.PhotoImage(file='%s/bonus400.gif'%carddir)
        self.cardimage['Bonus 300'     ]=Ttk.PhotoImage(file='%s/bonus300.gif'%carddir)
        self.cardimage['Fill 1000'     ]=Ttk.PhotoImage(file='%s/fill1000.gif'%carddir)
        self.cardimage['Vengeance'     ]=Ttk.PhotoImage(file='%s/vengeance.gif'%carddir)
        self.cardimage['No Dice'       ]=Ttk.PhotoImage(file='%s/nodice.gif'%carddir)
        self.cardimage['Double Trouble']=Ttk.PhotoImage(file='%s/doubletrouble.gif'%carddir)
        self.card=Ttk.Button(self.cardframe,image=self.cardimage['title'],command=self.drawcard,highlightcolor='black',highlightbackground='black',bd=0)
        self.card.pack()

        # show options
        self.options=(Ttk.Button(self.optionsframe,text='option1'),Ttk.Button(self.optionsframe,text='option2'))
        for but in self.options:
            but.pack(side=Ttk.TOP)
        self.setoptions()

        # show current scoreing
        self.pscore=Ttk.StringVar()
        self.tscore=Ttk.StringVar()
        self.tscore.set('% 4d'%0)
        self.pscore.set('% 4d'%0)
        plabel=Ttk.Label(scoreframe,bg='black',fg='white',text='potential score=')
        tlabel=Ttk.Label(scoreframe,bg='black',fg='white',text='     running score=')
        self.scorepl=Ttk.Label(scoreframe,bg='black',fg='white',textvariable=self.pscore)
        self.scoretl=Ttk.Label(scoreframe,bg='black',fg='white',textvariable=self.tscore)
        plabel.pack(side=Ttk.LEFT)
        self.scorepl.pack(side=Ttk.LEFT)
        tlabel.pack(side=Ttk.LEFT)
        self.scoretl.pack(side=Ttk.LEFT)

        # show players
        self.goal=Ttk.Button(b2, text='%d'%goal, command=self.resetgoal)
        orig_button_color=self.goal.cget("background")
        self.playersframe=Ttk.Frame(b2,height=240)
        self.goal.pack(side=Ttk.TOP)
        self.playersframe.pack(side=Ttk.TOP)
        self.pui={}
        if len(scores) < len(names):
            for each in self.names:
                self.pui[each]=Pui(self.playersframe,self,each)
                self.pui[each].nbut.configure(command=self.addplayerGui)
        else:
            for each in range(len(self.names)):
                self.pui[self.names[each]]=Pui(self.playersframe,self,self.names[each],scores[each])
                self.pui[self.names[each]].nbut.configure(command=self.addplayerGui)
        if whogoesfirst == "":
            self.player=self.names[0]
        else:
            self.player=whogoesfirst
        self.pui[self.player].setnext()
        self.maxScore=self.pui[self.player].player.score
        self.leadingPlayers=deepcopy(self.names)

        # show instructions
        self.iFont=10
        self.instructionbox=ScrolledText(b1,height=8,wrap=Ttk.WORD, font=('Times',self.iFont))
        self.instructionbox.pack(fill=Ttk.BOTH, expand=1)
        self.instructionbox.insert(Ttk.END, "Hey %s, It is your turn."%self.player)
        self.instructionbox.insert(Ttk.END, "\n Draw a card.")
        self.master.bind('<Key-i>', self.inspectW)
        self.master.bind('<Key->>', self.fontUp)
        self.master.bind('<Key-less>', self.fontDn)
        self.master.bind('<Key-R>', self.deScore)
        self.master.bind('<Key-c>', self.cheat)

    def deScore(self,event=None):
        '''reset scores'''
        for each in self.pui.keys():
            self.pui[each].scores.set('0')
            self.pui[each].player.score=0
            self.pui[each].total.set('0')
        self.maxScore=0

    def fontUp(self,event):
        self.iFont+=1
        self.iFont=min(25,self.iFont)
        self.instructionbox.configure(font=('Times',self.iFont))

    def fontDn(self,event):
        self.iFont-=1
        self.iFont=max(4,self.iFont)
        self.instructionbox.configure(font=('Times',self.iFont))

    def say_hi(self):
        print("hi there, everyone! %s"%self.player)

    def addplayerGui(self):
        '''Pop up a window to add a player to the pui'''
        wx=self.master.winfo_x()
        wy=self.master.winfo_y()
        self.apwin=Ttk.Toplevel(self.master)
        self.apwin.wm_title("Add a player")
        self.suf=self.mkAddPlayer(self.apwin)
        self.apwin.update()
        dy=self.apwin.winfo_height()
        dx=self.apwin.winfo_width()
        self.apwin.geometry('%dx%d+%d+%d'%(dx,dy,wx,wy))
        self.goplay.configure(command=self.addplayers)

    def resetgoal(self):
        ''' '''
        wx=self.master.winfo_x()
        wy=self.master.winfo_y()
        self.goalf=Ttk.Toplevel(self.master)
        self.egoal=Ttk.Entry(self.goalf)
        self.egoal.pack()
        self.goalf.update()
        dx=self.goalf.winfo_width()
        dy=self.goalf.winfo_height()
        self.goalf.geometry('%dx%d+%d+%d'%(dx,dy,wx,wy))
        self.egoal.bind('<Return>', self.setgoal)

    def setgoal(self,event):
        self.goal.configure(text='%d'%int(self.egoal.get()))
        self.goalf.destroy()

    def addplayers(self, debug=False):
        newnames=self.playlist.get(0,Ttk.END)
        for each in newnames:
            self.addplayer(each,debug=debug)
        self.apwin.destroy()

    def addplayer(self,name,debug=False):
        if debug: print(self.names)
        self.pui[name]=Pui(self.playersframe,self,name)
        self.names.append(name)
        if debug: print(self.names)

    def getnewLeaders(self):
        maxs=self.pui[self.names[0]].player.score
        leads=[self.names[0]]
        for player in self.names[1:]:
            if self.pui[player].player.score>maxs:
                maxs=self.pui[player].player.score
                leads=[player]
            elif self.pui[player].player.score==maxs:
                leads.append(player)
        self.maxScore=maxs
        if self.leadingPlayers[0] != leads[0] :
            print('New leader(s):')
            for former in leads:
                print(former,' ',)
            print('\n replaces ',)
            for former in self.leadingPlayers:
                print(former, ' ',)
            print('\n as leading player')
        self.leadingPlayers=deepcopy(leads)

    def updatescore(self,name,score):
        if score == 0: return
        self.pui[name].updatescore(score)
        # check for high scorer
        formerHi=self.leadingPlayers
        if self.pui[name].player.score > self.maxScore:
            self.maxScore=self.pui[name].player.score
            self.leadingPlayers=[name]
            if formerHi[0] != name:
                #print('New max score %d\nformer leader, %s, supplanted by %s'%(self.maxScore,formerHi[0],name))
                self.instructionbox.insert(Ttk.END, '\n With a score of %d, %s has taken the lead.'%(self.maxScore,name))
        elif self.pui[name].player.score == self.maxScore:
            self.leadingPlayers.append(name)

    def scoreNquit(self):
        '''add score to player, and set new player'''
        global tscore, pscore,state
        player=self.player
        #print(player,tscore,pscore)
        self.updatescore(player,tscore+pscore)
        # check for winner
        #print('goal is ',self.goal.cget('text'), int(self.goal.cget('text')))
        if self.pui[player].player.score > int(self.goal.cget('text')):
            state=WINNER
            self.setoptions()
        else:
            self.nextplayer()

    def nextplayer(self):
        global state,pscore,tscore
        self.pui[self.player].shownotnext()
        tscore=0
        pscore=0
        self.pscoreset(pscore)
        self.tscoreset(tscore)
        state=NEXTPLAYER	
        for ii in range(len(self.names)):
            if self.player == self.names[ii]:
                self.player=self.names[((ii+1)%len(self.names))]
                break
        else:
            print(self.player,' not in ',)
            for each in self.names:
               print(each,)
        self.setoptions()

    def testguimod(self,player):
        for name in ['Must Bust','Bonus 500','Vengeance','Fill 1000','No Dice']:
            self.card.configure(image=self.cardimage[name])
            self.master.update()
            time.sleep(2)
        for roll in [range(1,7), range(6,0,-1), [1,6,5,2,3,4]]:
            self.updatedice(roll)
            self.master.update()
            time.sleep(1)
        return 0

    def turnoffgui(self):
        self.card.configure(command=self.donothing)
        self.options[0].configure(command=self.donothing)
        self.options[1].configure(command=self.donothing)

    def turnongui(self):
        self.card.configure(command=self.drawcard)

    def aiplayer(self):
        ''' '''
        global tscore,pscore
        #print('\n%s is a computeragent'%self.player)
        self.turnoffgui()
        pscore=0
        tscore=self.playserial(self.player)
        #tscore=self.testguimod(self.player)
        self.turnongui()
        self.scoreNquit()

    def newcard(self,name):
        self.card.configure(image=self.cardimage[name])

    def getdice(self,rolled):
        '''Return the values of the selected dice'''
        picked=[]
        for die in range(rolled):
            if self.diceb[die].selection() == True:
                picked.append(die)
        #print('picked in getdice: ',picked)
        return picked

    def scoreDie(self):
        '''get the values of the selected dice
           and determine their score'''
        global pscore, dice, preserve
        rolled=6-len(dice.reserved)
        picked=self.getdice(rolled)
        dlist=[int(a) for a in picked]
        pscore,preserve,dummy=dice.scored(dlist)
        if pscore<1:
            self.instructionbox.insert(Ttk.END,'\nYou must keep enough to score someting; it\'s a rule')
            self.instructionbox.see(Ttk.END)
            dlist=[int(a) for a in range(rolled)]
            self.updatedice(dice.dice,dice.reserved,dlist)
            pscore,preserve,dummy=dice.scored(dlist)
            self.updatedice(dice.dice,dice.reserved,dummy)
        self.pscore.set('% 4d'%pscore)
        #print('scoreDie NOTDONE')

    def updatedice(self,rolled,reserved=[],dlist=[]):
        '''revise dice buttons per roll results and choice to score'''
        global dice, card
        for each in range(len(rolled)):
            self.diceb[each].button.configure(image=self.flagdown[rolled[each]], \
                selectimage=self.flagsup[rolled[each]], \
                # highlightbackground='grey', \
                 highlightbackground='black', \
                indicatoron=0, relief=Ttk.SUNKEN, bd=0, command=self.scoreDie)
            self.diceb[each].button.deselect()
            if card == 'Must Bust':
                self.diceb[each].button.configure(command=self.donothing)
        for each in dlist:
            self.diceb[each].button.select()
            if card == 'Must Bust':
                self.diceb[each].button.configure(image=self.flagsup[rolled[each]])
        enrolled=len(rolled)-len(reserved)
        for each in range(len(reserved)):
            self.diceb[each+enrolled].button.configure(image=self.flagsup[reserved[each]], \
            selectimage=self.flagsup[reserved[each]], indicatoron=0, relief=Ttk.SUNKEN, \
            bd=5,highlightbackground='red',command=self.donothing)

    def drawcard(self):
        global state,deck,card,gtesting
        if state == DRAWCARD:
            card=ctype(deck.draw())
            if gtesting:
                tcard = raw_input(' for testing, input a card: ')
                if len(tcard)>0:
                    card=tcard
            self.card.configure(image=self.cardimage[card])
            if card == 'Vengeance':
                state=DREWVENGEANCE
                self.setoptions()
            elif card == "No Dice":
                self.nextplayer()
            else:
                state=ROLLFIRST
                self.setoptions()

    def takeVengeance(self):
        global state,speak
        if speak:
            line='Look out '
            for each in self.leadingPlayers:
                line+= '%s '%each
            line+= '%s is coming for you!'%self.player
            talktome(line)
        state=ROLLFIRST
        self.setoptions()

    def godraw(self):
        global state
        state=DRAWCARD
        self.options[1].configure(text='       ',command=self.donothing)

    def rollDice(self):
        '''roll the dice and determine subsequent course of events'''
        global dice, state, card, pscore, preserve, tscore,gtesting, debug
        if state == ROLLFIRST:
            dice=Dice()
            if gtesting:
                sdice=raw_input(' test roll string of 6: ')
                if len(sdice)>0:
                    dice.str2dice(sdice)
            if debug: print('   first roll is ',dice.dice)
        else:
            if debug: print('reserve ', preserve)  #FIXPRNT
            dice.reserve(preserve)
            if debug: print('reserved:', dice.reserved)  #FIXPRNT
            tscore+=pscore
            self.tscore.set('% 4d'%tscore)
            dice.dice=dice.roll()
            if gtesting:
                sdice=raw_input(' test roll string of %d: '%(6-len(dice.reserved)))
                if len(sdice)>0:
                    dice.str2dice(sdice)
            #print('   next roll is ',dice.dice)  #FIXPRNT
            if debug: print('   next roll: ',dice.dice[:(6-len(dice.reserved))], '||',dice.dice[(6-len(dice.reserved)):])  #FIXPRNT
        # get potential score and show it
        pscore,preserve,dlist=dice.scored(list(range(6-len(dice.reserved))))
        if card == 'Double Trouble':
            pscore*=2
        if debug: print(pscore, preserve, dlist)  #FIXPRNT
        self.pscore.set('% 4d'%pscore)
        #set states for all scoreable
        self.updatedice(dice.dice,dice.reserved,dlist)
        # check if busted or filled
        if pscore == 0:
            state = BUSTED
        elif (len(preserve)+len(dice.reserved))==6:
            state = FILLED
        else:
            state=ROLLED
        self.setoptions()

    def enRoll(self):
        ''' Show dice as not rolled'''
        for die in self.diceb:
            die.button.configure(relief=Ttk.SUNKEN, bd=0 \
                , selectimage=self.flagsup[0], image=self.flagsup[0] \
                ,command=self.rollDice, state='normal')

    def deRoll(self):
        ''' Show dice as not rolled'''
        for die in self.diceb:
            die.button.configure(relief=Ttk.SUNKEN, bd=0 \
                #, selectimage=self.flagsup[0], image=self.flagsup[0] \
                ,command=self.rollDice, state='disabled')

    def donothing(self):
        pass

    def tscoreset(self,val):
        self.tscore.set('% 4d'%val)

    def pscoreset(self,val):
        self.pscore.set('% 4d'%val)

    def setoptions(self):	#{
        '''Set the commands to be bound to the option buttons
           based on the current state, the card, and the dice'''
        global state, card, pscore, preserve, filled, tscore, dice
        self.options[0].configure(state='normal')
        self.options[1].configure(state='normal')
        if state == DRAWCARD:
            self.options[0].configure(state='disabled',text='        ')
            self.options[1].configure(state='disabled',text='        ')
            self.deRoll()
        elif state == DREWVENGEANCE:
            self.options[0].configure(text='draw another card',command=self.godraw)
            self.instructionbox.insert(Ttk.END, "\n  You drew the Vengeance card.")
            # check leader
            if self.player in self.leadingPlayers:
                self.options[1].configure(text='           ',command=self.donothing)
                self.instructionbox.insert(Ttk.END, "\n  But you\'re the leader so just get a new card.")
                self.instructionbox.see(Ttk.END)
                self.godraw()
            else:
                self.options[1].configure(text='take Vengeance',command=self.takeVengeance)
                self.instructionbox.insert(Ttk.END, "\n  Do you want to take vengeance or get a new card.")
                self.instructionbox.see(Ttk.END)
        elif state == ROLLFIRST:
            self.options[0].configure(text='Roll dice',command=self.rollDice)
            self.options[1].configure(text='         ',command=self.donothing,state='disabled')
            self.enRoll()
            self.instructionbox.insert(Ttk.END, "\n  Roll the dice.")
            self.instructionbox.see(Ttk.END)
        elif state == ROLLED:
            self.options[0].configure(text='Roll dice',command=self.rollDice)
            if card == 'Must Bust':
                self.instructionbox.insert(Ttk.END, "\n  No risk, just roll the dice")
                self.options[1].configure(text='       ',command=self.donothing,state='disabled')
            elif card == 'Fill 1000' or card == 'Double Trouble' or card == 'Vengeance':
                self.instructionbox.insert(Ttk.END, "\n  You have to fill it.")
                self.instructionbox.insert(Ttk.END, "\n  Select the dice to keep and roll again.")
                self.options[1].configure(text='       ',command=self.donothing,state='disabled')
            else:
                self.options[1].configure(text='Score',command=self.scoreNquit)
                self.instructionbox.insert(Ttk.END, "\n  Decide whether to take the %d accumulated points."%(tscore+pscore))
                self.instructionbox.insert(Ttk.END, "\n    or risk it, select which dice to keep and roll the remaining dice")
            self.instructionbox.see(Ttk.END)
        elif state == BUSTED:
            self.instructionbox.insert(Ttk.END, "\n  BUSTED ")
            if card == 'Must Bust':
                #if dice.score>0:
                #if True:
                if tscore>0:
                    self.options[0].configure(text='Score it',command=self.scoreNquit)
                    self.options[1].configure(text=' ',command=self.donothing)
                    self.instructionbox.insert(Ttk.END, " your Must Bust.  Score the %d accumulated points."%(tscore+pscore))
                    self.instructionbox.see(Ttk.END)
                else:
                    self.instructionbox.insert(Ttk.END, "\n")
                    self.instructionbox.see(Ttk.END)
                    self.nextplayer()
            else:
                self.instructionbox.insert(Ttk.END, "\n")
                self.instructionbox.see(Ttk.END)
                self.nextplayer()
        elif state == FILLED:	#{
            self.instructionbox.insert(Ttk.END, "\n  You filled it!")
            filled+=1
            if card == "Must Bust":
                # just keep rolling
                tscore+=pscore
                self.tscoreset(tscore)
                pscore=0
                self.pscoreset(pscore)
                self.options[0].configure(text='Keep Rolling', command=self.rollDice)
                self.options[1].configure(text='         ',command=self.donothing,state='disabled')
                state=ROLLFIRST
            elif card == "Vengeance":
                # reduce leaders' scores
                for leader in self.leadingPlayers:
                    print('subtract from ', leader)  #FIXPRNT
                    self.updatescore(leader,-2500)
                # add players score 
                tscore+=pscore
                self.tscoreset(tscore)
                pscore=0
                self.pscoreset(pscore)
                self.updatescore(self.player,tscore)
                self.getnewLeaders()
                # and get a new turn
                state=NEXTPLAYER
                tscore=0
                self.tscoreset(tscore)
                pscore=0
                self.pscoreset(pscore)
                filled=0
                self.setoptions()
            elif card == "Double Trouble":
                # must fill it two times
                if filled==2:
                    # count double the score and get a new turn
                    self.instructionbox.insert(Ttk.END, "\n  You filled it twice!")
                    player=self.player
                    self.updatescore(player,tscore+pscore)
                    #self.updatescore(player,dice.score*2)
                    state=NEXTPLAYER
                    tscore=0
                    self.tscoreset(tscore)
                    pscore=0
                    self.pscoreset(pscore)
                    filled=0
                    self.setoptions()
                else:
                    self.options[0].configure(text='Roll dice',command=self.rollDice)
                    self.options[1].configure(text='         ',command=self.donothing,state='disabled')
                    tscore+=pscore
                    self.instructionbox.insert(Ttk.END, " for %d points.\n  You have to fill it again!"%tscore)
                    self.instructionbox.see(Ttk.END)
                    self.tscoreset(tscore)
                    pscore=0
                    self.pscoreset(pscore)
                    state=ROLLFIRST
            elif card == 'Fill 1000':
                tscore+=pscore+1000
                self.tscoreset(tscore)
                pscore=0
                self.pscoreset(pscore)
                self.options[0].configure(text='Draw Card', command=self.godraw)
                self.options[1].configure(text='Score',command=self.scoreNquit)
                self.instructionbox.insert(Ttk.END, "\n  You can take this score (%d) and end your turn."%tscore)
                self.instructionbox.insert(Ttk.END, "\n  or risk this score and draw another card.")
                self.instructionbox.see(Ttk.END)
            elif 'Bonus' in card:
                tscore+=pscore+int(card[5:])
                self.tscoreset(tscore)
                pscore=0
                self.pscoreset(pscore)
                self.options[0].configure(text='Draw Card', command=self.godraw)
                self.options[1].configure(text='Score',command=self.scoreNquit)
                self.instructionbox.insert(Ttk.END, "\n  You can take this score (%d) and end your turn."%tscore)
                self.instructionbox.insert(Ttk.END, "\n  or risk this score and draw another card.")
            self.instructionbox.see(Ttk.END)	#}
        elif state == NEXTPLAYER:
            self.pui[self.player].setnext()
            self.master.update()
            time.sleep(1)
            if self.player[:2]=='ai':
                    self.aiplayer()
            else:
                # set new player and ask to draw a card
                tscore=0
                self.options[0].configure(text='         ', command=self.donothing,state='disabled')
                self.options[1].configure(text='         ',command=self.donothing,state='disabled')
                self.instructionbox.insert(Ttk.END, "\n\nHey %s, It is your turn."%self.player)
                self.instructionbox.insert(Ttk.END, "\n Draw a card.")
                self.instructionbox.see(Ttk.END)
                state= DRAWCARD
                self.setoptions()
        elif state == WINNER:
            self.instructionbox.insert(Ttk.END, "\n\n %s! You are the big whiner, I mean winner!"%self.player)
            self.instructionbox.see(Ttk.END)
            self.options[0].configure(text='         ', command=self.donothing,state='disabled')
            self.options[1].configure(text='         ',command=self.donothing,state='disabled')
            self.doWinner()
	#}

    def doWinner(self):
            if speak:
                talktome('%s! You are the big whiner, I mean winner!'%self.player)
            suf=Ttk.Toplevel()
            winner=Ttk.Button(suf,text='!!! %s wins !!!'%self.player,font=('Courier',44),command=sys.exit)
            winner.pack(padx=10,pady=10)
            winner.bind('<Button-3>', self.goLonger)
            more=Ttk.Frame(suf)
            again=Ttk.Button(more,text="New game")
            again.pack(side=Ttk.LEFT)
            longer=Ttk.Button(more,text="Extend game")
            longer.pack(side=Ttk.LEFT)
            more.pack(side=Ttk.TOP)
            suf.bind('<Key-A>', self.restart)
            again.bind('<Button-1>', self.restartb)
            longer.bind('<Button-1>', self.goLongerb)
            #print(suf.winfo_children())  #FIXPRNT
            #print(winner)  #FIXPRNT
        #}

    def goLongerb(self,event):
        #called by button in frame in popup
        event.widget.master.master.destroy()
        self.resetgoal()
        self.nextplayer()

    def goLonger(self,event):
        event.widget.master.destroy()
        self.resetgoal()
        self.nextplayer()

    def restartb(self,event):
        '''Start the game over with the same players'''
        global state, pscore, tscore
        pscore=0
        tscore=0
        self.deScore()
        self.tscoreset(0)
        self.pscoreset(0)
        self.card.configure(image=self.cardimage['title'],command=self.drawcard)
        self.enRoll()
        self.deRoll()
        self.instructionbox.insert(Ttk.END, "\n\nHey %s, It is your turn."%self.names[0])
        self.pui[self.player].shownotnext()
        self.player=self.names[0]
        self.pui[self.player].setnext()
        self.instructionbox.insert(Ttk.END, "\n Draw a card.")
        #called by button in frame in popup
        event.widget.master.master.destroy()
        state=DRAWCARD

    def restart(self,event):
        '''Start the game over with the same players'''
        #called by A-key in popup
        global state
        self.deScore()
        # kill "winner" window
        #print(event.widget)  #FIXPRNT
        event.widget.destroy()
        state=DRAWCARD

    def respond(self,player,options, rtype=None,debug=False):
        '''select ai response from options and show in history'''
        response= self.pui[player].player.ynResp(1,0,rtype=rtype,debug=debug)
        self.instructionbox.insert(Ttk.END, options[response])
        if debug: print(options[response])  #FIXPRNT
        return response
        
    def playserial(self, player):	#{
        '''Computer guided play according to the rules and the probability of events.
           Circumvent the GUI for decisions and actions.'''
        global deck, debug
        self.instructionbox.insert(Ttk.END, "\n\n%s takes it's turn.\n"%player)
        # take a turn according to the rules
        its_my_turn=True
        tscore=0
        # rule 1: turn a card to start and after each fill
        while its_my_turn:	# { turn loop
            #tscore=0
            filled=0
            mfills=1
            card=ctype(deck.draw())
            if testing:
                tcard = raw_input(' for testing, input a card: ')
                if len(tcard)>0: card=tcard
            self.instructionbox.insert(Ttk.END, "  %s drew %s\n"%(player, card))
            if debug:
                print("1  %s drew %s\n"%(player, card))  #FIXPRNT
            self.newcard(card)
            self.master.update()
            time.sleep(1)
            if card =='Vengeance':
               if player not in self.leadingPlayers:
                    rtype={}
                    rtype['name']='vengeance'
                    rtype['app']=app
                    response=self.respond(player, \
                       ['Seek vengeance\n','next card\n'][::-1], \
                       rtype=rtype,debug=debug)
                    if response <1: 	# conservative?
                       continue
               else:
                    self.instructionbox.insert(Ttk.END, '  but you can\'t take vengeance on yourself.\n')
                    continue
            if card =='No Dice':
                its_my_turn=False
                tscore=0
            else:
                # Roll all the dice
                if card == 'Double Trouble':
                    mfills=2
                while filled<mfills:  # { multi-fills loop
                    dice=Dice()
                    if testing:
                         tstr=raw_input('test first roll: ')
                         if len(tstr)>0:
                             dice.dice=[int(a) for a in tstr]
                    self.updatedice(dice.dice)
                    self.master.update()
                    time.sleep(1)
                    # get potential score
                    pscore,preserve,dummy=dice.scored(list(range(6)))
                    if pscore == 0:	#{ BUSTED on full roll
                       if 'Bonus' in card or 'Fill' in card or 'Veng' in card:
                            self.instructionbox.insert(Ttk.END,'  Gee %s, you busted right away\n'%player)
                            self.instructionbox.see(Ttk.END)
                            if debug: print('2  Gee %s, you busted right away'%player)  #FIXPRNT
                            #filled=mfills
                            its_my_turn=False
                            return 0
                            break	# out of fills loop
                       elif card == 'Double Trouble':
                            if filled==1:
                               tscore=0
                               self.instructionbox.insert(Ttk.END, " Just couldn't fill it the second time\n")
                               if debug: print("3 Just couldn't fill it the second time")  #FIXPRNT
                            else:
                               tscore=0
                               self.instructionbox.insert(Ttk.END, '  Gee %s, you busted right away\n'%player)
                               if debug: print('4  Gee %s, you busted right away'%player)  #FIXPRNT
                            return 0
                            its_my_turn=False
                            #filled=mfills
                            break	# out of fills loop
                       else:	# Must Bust did
                            if tscore>0:
                                #players[player].update(tscore)
                                return tscore #CHECK THIS
                                its_my_turn=False
                            #filled=mfills
                            else:
                                self.instructionbox.insert(Ttk.END, '  Gee %s, you busted right away\n'%player)
                                if debug: print('5  Gee %s, you busted right away\n'%player)  #FIXPRNT
                                its_my_turn=False
                                self.master.update()
                            break	# out of fills loop
                    #}
                    if len(preserve)==6: #{ filled on full roll
                       self.instructionbox.insert(Ttk.END, '!! filled on the first roll\n')
                       if debug: print('6 !! filled on the first roll\n')  #FIXPRNT
                       dice.score=pscore
                       filled+=1
                       if card == 'Vengeance':
                            tscore+=pscore
                            self.instructionbox.insert(Ttk.END, '  !! Vengeance !!')
                            leadlist=''
                            for leader in self.leadingPlayers:
                                self.updatescore(leader,-2500)
                                leadlist+= 'and '+leader+' '
                            self.instructionbox.insert(Ttk.END, '%s now has %d\n'%(leadlist,players[self.leadingPlayers[0]].score))
                            self.updatescore(player,tscore)
                            self.instructionbox.insert(Ttk.END, '    %s score is now %d\n   ,'%(player,self.pui[player].player.score))
                            if debug: print('%s now has %d\n'%(leadlist,players[self.leadingPlayers[0]].score))  #FIXPRNT
                            time.sleep(1)
                            self.instructionbox.insert(Ttk.END, '  %s, take another turn\n'%player)
                            if debug:  print('7   %s, take another turn\n'%player)  #FIXPRNT
                            self.master.update()
                            tscore=0
                            mfills=0
                            break	# out of fills loop
                       elif card == 'Double Trouble':
                            tscore+=pscore*2
                            if filled == 2:
                               self.updatescore(player,tscore)
                               self.instructionbox.insert(Ttk.END, '  %s, take another turn\n'%player)
                               if debug: print('8  %s, take another turn\n'%player)  #FIXPRNT
                               tscore=0
                               mfills=0
                               break	# out of fills loop
                            self.instructionbox.insert(Ttk.END, ' but you need to fill it twice to score\n')
                            self.master.update()
                            time.sleep(1)
                            continue	# to start of fills loop
                       elif 'Bonus' in card or 'Fill' in card:
                            bonus=int(card[5:])
                            tscore+=pscore+bonus
                            rtype={}
                            rtype['name']='draw'
                            rtype['score']=tscore
                            rtype['app']=app
                            response = self.respond(player \
                              ,['End the turn and keep the %d points\n'%tscore,'Risk it by taking another card\n'] \
                              ,rtype=rtype,debug=debug)
                            if response>0:
                               its_my_turn=True
                            else:
                               return tscore  #CHECK THIS
                               its_my_turn=False
                            mfills=filled
                            #pscore=0
                            break	# out of fills loop
                       elif card == 'Must Bust':
                            tscore+=pscore
                            self.instructionbox.insert(Ttk.END, '\n  Score for this turn is up to %d points\n'%tscore)
                            self.instructionbox.insert(Ttk.END, '  But don\'t stop now.\n')
                            if debug: print('9 must bust score is up to %d points'%tscore)  #FIXPRNT
                            mfills=filled+1
                            continue	# top of fills loop
                    #}
                    # continue rolling until filled, busted, or risk-averse
                    while pscore>0:	# {
                       self.instructionbox.insert(Ttk.END,'   potential score = %d by keeping %s\n'%(pscore,preserve))
                       if debug: print('10   potential score = %d by keeping %s\n'%(pscore,preserve))  #FIXPRNT
                       # add all the scoring dice and go on
                       #tscore+=pscore
                       dice.reserve(preserve)
                                    
                       numtoroll=6-len(dice.reserved)
                       if card == 'Double Trouble': # take all that scores
                            tscore+=pscore*2
                       elif card == 'Fill 1000' or card == 'Vengeance' or card == 'Must Bust':	# take all that scores
                            tscore+=pscore
                       elif 'Bonus' in card:	# choose which dice to roll again
                            tscore+=pscore
                            rtype={}
                            rtype['name']='roll'
                            rtype['ndice']=numtoroll
                            rtype['score']=tscore
                            rtype['app']=self
                            response=self.respond(player \
                              ,['risk %d points by rolling the remaining %d dice\n'%(tscore,numtoroll),'Take the score and end the turn\n'][::-1] \
                              ,rtype=rtype,debug=debug)
                            if debug: print('10a response',response)  #FIXPRNT
                            if response>0:
                               its_my_turn=True
                            else:
                               #players[player].update(tscore)
                               return tscore  #CHECK THIS
                               mfills=filled
                               its_my_turn=False
                               break	# out of rolling loop
                       dice.dice=dice.roll()
                       if testing:
                            testroll = raw_input(' testing next roll %d: '%numtoroll)[:numtoroll]
                            if len(testroll)>0:
                                dice.dice=[int(a) for a in testroll]+dice.dice[numtoroll:]
                       if debug: print('11   next roll: ',dice.dice[:numtoroll], '||',dice.dice[numtoroll:])  #FIXPRNT
                       pscore,preserve,dummy=dice.scored(list(range(numtoroll)))
                       self.updatedice(dice.dice,dice.reserved,dummy)
                       self.master.update()
                       time.sleep(1)
                       if len(preserve)+len(dice.reserved)== 6:  #{ it is filled
                            filled+=1
                            self.instructionbox.insert(Ttk.END, '  ! You filled it !\n')
                            if debug: print('12  ! You filled it !')  #FIXPRNT
                            if card == 'Vengeance':
                               tscore+=pscore
                               self.instructionbox.insert(Ttk.END, '  !! Vengeance !!\n')
                               leadlist=''
                               for leader in self.leadingPlayers:
                                  self.updatescore(leader,-2500)
                                  leadlist+= 'and '+leader+' '
                               self.instructionbox.insert(Ttk.END, '%s now have %d\n'%(leadlist,app.pui[self.leadingPlayers[0]].player.score))
                               self.updatescore(player,tscore)
                               self.instructionbox.insert(Ttk.END, '    %s score is now %d\n   ,'%(player,self.pui[player].player.score))
                               self.instructionbox.insert(Ttk.END, '  %s, take another turn'%player)
                               if debug: print('13 after Vengeance %s, take another turn'%player)  #FIXPRNT
                               self.master.update()
                               tscore=0
                               its_my_turn=True
                               break	# out of rolling loop
                            elif card == 'Double Trouble':
                               tscore+=pscore*2
                               if filled == 2:
                                    self.updatescore(player,tscore)
                                    self.instructionbox.insert(Ttk.END, '  %s, take another turn\n'%player)
                                    if debug: print('14 after DoubTroub %s, take %d points and another turn'%(tscore,player))  #FIXPRNT
                                    self.master.update()
                                    tscore=0
                                    its_my_turn=True
                                    break	# out of rolling loop
                               else:
                                    self.instructionbox.insert(Ttk.END, '   You have to fill it again. Good luck\n')
                                    if debug: print('15   You have to fill it again.')  #FIXPRNT
                               break	# out of rolling loop
                            elif 'Bonus' in card or 'Fill' in card:
                               bonus=int(card[5:])
                               tscore+=pscore+bonus
                               mfills=filled-1
                               rtype={}
                               rtype['name']='draw'
                               rtype['score']=tscore
                               rtype['app']=app
                               response = self.respond(player \
                              ,['End the turn and keep the %d points\n'%tscore,'Risk it by taking another card\n'] \
                              ,rtype=rtype,debug=debug)
                               if response>0:
                                    its_my_turn=True
                               else:
                                    #players[player].update(tscore)
                                    return tscore  #CHECK THIS
                                    its_my_turn=False
                               break	# out of rolling loop
                            elif card == 'Must Bust':
                               tscore+=pscore
                               self.instructionbox.insert(Ttk.END, '\n  Score for this turn is up to %d points'%tscore)
                               self.instructionbox.insert(Ttk.END, '  But don\'t stop now.')
                               if debug: print('16   score for MustBust is up to %d points'%tscore)  #FIXPRNT
                               self.master.update()
                               mfills=filled+1
                               break	# out of rolling loop
                       #}
                    else: #}  finished rolling cause you busted
                        self.instructionbox.insert(Ttk.END, '   !!! BUSTED !!!\n')
                        if debug: print('17   !!! BUSTED !!!')  #FIXPRNT
                        mfills=filled
                        if card != 'Must Bust':
                            return 0
                        #tscore=0
                        #pscore=0
                        its_my_turn=False
                        #break	# out of fills loop
                    if debug: print('18  DEBUG: %s, bottom of fills loop, tscore,pscore,filled,mfills= ',card,tscore,pscore,filled,mfills)  #FIXPRNT
                    if card == 'Must Bust':
                        if pscore==0:
                            mfills=filled
                            tscore+=pscore
                            #players[player].update(tscore)
                            return tscore
                            its_my_turn=False
                #}	fills loop
            #}	turn loop
        return tscore
    #}  

    def showAbout(self):
        '''Describe this program'''
        self.helpwinA=Ttk.Toplevel(self.master)
        self.helpwinA.wm_title("About Fill'RBust")
        howto=ScrolledText(self.helpwinA,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        howto.pack(side=Ttk.TOP,fill=Ttk.BOTH,expand=1)
        howto.insert(Ttk.END,about)
        done=Ttk.Button(self.helpwinA,text='Dismiss',command=self.dismissHelpA)
        done.pack(side=Ttk.TOP)

    def showSynopsis(self):
        '''Describe how to play with this GUI'''
        self.helpwinG=Ttk.Toplevel(self.master)
        self.helpwinG.wm_title("Fill'RBust Buttons")
        howto=ScrolledText(self.helpwinG,height=38,wrap=Ttk.WORD,font=('Times',self.iFont))
        howto.pack(side=Ttk.TOP,fill=Ttk.BOTH,expand=1)
        howto.insert(Ttk.END,theGUI)
        done=Ttk.Button(self.helpwinG,text='Dismiss',command=self.dismissHelpG)
        done.pack(side=Ttk.TOP)

    def showRules(self):
        '''Show rules in a window'''
        self.helpwinR=Ttk.Toplevel(self.master)
        self.helpwinR.wm_title("Fill'RBust Rules")
        howto=ScrolledText(self.helpwinR,height=38,wrap=Ttk.WORD,font=('Times',self.iFont))
        howto.pack(side=Ttk.TOP,fill=Ttk.BOTH,expand=1)
        howto.insert(Ttk.END,therules)
        done=Ttk.Button(self.helpwinR,text='Dismiss',command=self.dismissHelp)
        done.pack(side=Ttk.TOP)
        done.bind('<Button-3>', self.spekTherules)

    def spekTherules(self,event):
        if speak:
            talktome(therules)
    
    def dismissHelp(self):
        self.helpwinR.destroy()

    def dismissHelpA(self):
        self.helpwinA.destroy()

    def dismissHelpG(self):
        self.helpwinG.destroy()

    def helpGui(self):
        ''' make all button commands helpful'''
        self.master.configure(cursor='question_arrow')
        self.commands={}
        #buttons
        self.commands['card']=self.card['command']
        self.card.configure(command=self.helpcard)
        self.commands['goal']=self.goal['command']
        self.goal.configure(command=self.helpgoal)
        for each in self.pui.keys():
            self.commands['pui%s'%each]=self.pui[each].nbut['command']
            self.pui[each].nbut.configure(command=self.helpAP)
        for each in range(len(self.diceb)):
            self.commands['dice%d'%each]=self.diceb[each].button['command']
            self.diceb[each].button.configure(command=self.helpdice)
        self.commands['option0']=self.options[0]['command']
        self.options[0].configure(command=self.helpOption)
        self.commands['option1']=self.options[1]['command']
        self.options[1].configure(command=self.helpOption)
        #menu options
        self.commands['gmenu0']=self.gamemenu.entrycget(0,'command')
        self.gamemenu.entryconfig(0,command=self.helpAP)
        self.commands['gmenu1']=self.gamemenu.entrycget(1,'command')
        self.gamemenu.entryconfig(1,command=self.helpgoal)
        self.commands['gmenu2']=self.gamemenu.entrycget(2,'command')
        self.gamemenu.entryconfig(2,command=self.helpQuit)
        self.commands['hmenu0']=self.helpmenu.entrycget(0,'command')
        self.helpmenu.entryconfig(0,command=self.helphelp)
        self.commands['hmenu1']=self.helpmenu.entrycget(1,'command')
        self.helpmenu.entryconfig(1,command=self.helphelp)
        self.commands['hmenu2']=self.helpmenu.entrycget(2,'command')
        self.helpmenu.entryconfig(2,command=self.helphelp)


    def normalGui(self):
        ''' revert all button commands to action'''
        self.master.configure(cursor='arrow')
        self.card.configure(command=self.commands['card'])
        self.goal.configure(command=self.resetgoal)
        for each in self.pui.keys():
            self.pui[each].nbut.configure(command=self.commands['pui%s'%each])
        for each in range(len(self.diceb)):
            self.diceb[each].button.configure(command=self.commands['dice%d'%each])
        self.options[0].configure(command=self.commands['option0'])
        self.options[1].configure(command=self.commands['option1'])
        # menu options
        self.gamemenu.entryconfig(0,command=self.addplayerGui)
        self.gamemenu.entryconfig(1,command= self.resetgoal)
        self.gamemenu.entryconfig(2,command= sys.exit)
        self.helpmenu.entryconfig(0,command= self.showRules)
        self.helpmenu.entryconfig(1,command= self.showSynopsis)
        self.helpmenu.entryconfig(2,command= self.helpGui)

    def helpcard(self):
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,cardHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def helpgoal(self):
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,goalHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def helpAP(self):
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,playerHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def helpdice(self):
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,diceHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def helpOption(self):
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,optionHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def helpQuit(self):
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,quitHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def helphelp(self):
        '''display help info'''
        helpwin=Ttk.Toplevel(self.master)
        helpwin.wm_title('Help')
        helpt=ScrolledText(helpwin,height=8,wrap=Ttk.WORD,font=('Times',self.iFont))
        helpt.pack(side=Ttk.TOP)
        helpt.insert(Ttk.END,helpHelp)
        done=Ttk.Button(helpwin,text='Dismiss',command=helpwin.destroy)
        done.pack(side=Ttk.TOP)
        self.normalGui()

    def cheat(self, arg=None):
        global card, tscore,pscore,state
        #card='Must Bust'
        #card='Fill 1000'
        #self.card.configure(image=self.cardimage[card])
        #self.nextplayer()
        state=DREWVENGEANCE
        card='Vengeance'
        self.setoptions()

    def setIfont(self, event):
        self.instructionbox.configure(font=('Helvetica', 22))

    def setDebug(self, event):
        global debug
        debug= not debug
        if debug: print('Debug print on')  #FIXPRNT
    
    def inspectW(self, event):
        self.inspectwin=Ttk.Toplevel(self.master)
        self.inspectwin.wm_title('Eval 4 DB')
        self.inspectS=Ttk.StringVar()
        inspectE=Ttk.Entry(self.inspectwin, textvariable=self.inspectS)
        inspectE.pack(side=Ttk.TOP)
        dismissb=Ttk.Button(self.inspectwin,text='Dismiss',command=self.dismissInspect)
        dismissb.pack(side=Ttk.TOP)
        inspectE.bind('<Key-Return>',self.inspect)
    def dismissInspect(self):
        self.inspectwin.destroy()
    def inspect(self,event):
        word=self.inspectS.get()
        print(eval('%s'%word))  #FIXPRNT
    def savegame(self):
        ''' select a file or define a new one
            to which to save the current game for continuing later.'''
        global deck
        # open a file dialog to select the file name

        # save the state of the current game to the file.
        write_state([self.pui[ii].player for ii in self.names], deck.deck, self.player, int(self.goal.cget('text')))

class Die:
    """
    Display dice as a set of buttons painted by an image.
    A set of images is defined for two sets of 1-6.
    One set for selected, the other for unselected.
    """
    def __init__(self,master,num=0):
        self.dnum=num
        self.var=Ttk.IntVar()
        self.button= Ttk.Checkbutton(master.diceframe, relief=Ttk.SUNKEN, \
            image=master.flagdown[num], bg='black', fg='black', \
            selectimage=master.flagsup[num], \
            indicatoron=0, command=master.scoreDie, var=self.var)
        #self.button.toggle()
        self.button.pack(side=Ttk.LEFT)
    def num(self):
        return self.dnum
    def set(self):
        if not self.var.get():
            self.toggle()
    def toggle(self):
        self.button.toggle()
    def selection(self):
        return self.var.get()

class Pui():
    """
    User interface for players:
        For each player, it shows:
            name (highlighted in green during turn)
            list of scores
            total score to date.
    """
    def __init__(self,frame,parent,name,score=0):
        self.af=Ttk.Frame(frame)
        self.af.pack(side=Ttk.LEFT)
        self.parent=parent
        self.nbut=Ttk.Button(self.af,text=name)
        if name[:2]=='ai':
            fact=name[-1]
            if fact.isdigit():
                fact=int(fact)
            else:
                fact=5
            self.player=AIPlayer(name,risker=fact,score=score)
            print('added %s as AIPlayer with risk %d/10'%(name,fact))  #FIXPRNT
        else:
            self.player=Player(name,score)
        self.scores=Ttk.StringVar()
        self.scores.set("%d"%score)
        self.total=Ttk.StringVar()
        self.total.set("%d"%score)
        self.scoreb=Ttk.Listbox(self.af,height=15,width=6,listvariable=self.scores)
        self.scorel=Ttk.Label(self.af,textvariable=self.total)
        self.nbut.pack(side=Ttk.TOP)
        self.nbut.bind('<Button-3>', self.deleteMe)
        self.nbut.bind('<Key-R>', self.deleteMe)
        self.scoreb.pack(side=Ttk.TOP,fill=Ttk.BOTH)
        self.scorel.pack(side=Ttk.TOP)

    def updatescore(self,score):
        """
        Update the score that is displayed
        and tell the Player to update its score.
        """
        self.scoreb.insert(Ttk.END,'%d'%score)
        self.scoreb.see(Ttk.END)
        self.player.update(score)
        self.total.set('%d'%(self.player.score))

    def setnext(self):
        self.nbut.configure(bg='green')
    def shownotnext(self):
        self.nbut.configure(bg=orig_button_color)
    def deleteMe(self, event):
        '''pop up a new window to rename the player.
           empty name deletes the player'''
        global debug
        if debug: print('this should rename ', self.player.name)  #FIXPRNT
        wx=self.parent.master.winfo_x()
        wy=self.parent.master.winfo_y()
        self.renamef=Ttk.Toplevel(self.parent.master)
        self.srename=Ttk.StringVar()
        self.srename.set(self.player.name)
        self.erename=Ttk.Entry(self.renamef)
        self.erename["textvariable"]=self.srename
        self.erename.pack()
        self.renamef.update()
        dx=self.renamef.winfo_width()
        dy=self.renamef.winfo_height()
        self.renamef.geometry('%dx%d+%d+%d'%(dx,dy,wx,wy))
        self.erename.bind('<Return>', self.setrename)

    def setrename(self,event):
        ''' rename (or delete) player'''
        newname=self.srename.get()
        oldname=self.player.name
        if len(newname)>0:
            self.player.name=newname
            self.nbut.configure(text='%s'%newname)
            if oldname[0:2]=='ai': 
                if newname[0:2]!='ai':
                    #switch from ai to real
                    if debug: print('change from AI')  #FIXPRNT
                elif oldname[:] != newname[:] and newname[:].isdigit():
                    self.player.risker=int(newname[:])
            elif newname[0:2]=='ai' and oldname[0:2]!='ai':
                print('change to AI not implemented')  #FIXPRNT
            # copy Pui
            self.parent.pui[newname]=self.parent.pui[oldname]
            del self.parent.pui[oldname]
            for a in range(len(self.parent.names)):
               if self.parent.names[a] is oldname:
                  self.parent.names[a]=newname
            if self.parent.player is oldname:
                self.parent.player=newname
            self.renamef.destroy()
        else:
            self.af.destroy()
            del self.parent.pui[self.player.name]
            for a in range(len(self.parent.names)):
                if self.parent.names[a] is self.player.name:
                    del self.parent.names[a]
                    break
            if oldname == self.parent.player:
                self.parent.player=self.parent.names[a%len(self.parent.names)]
                self.parent.pui[self.parent.player].setnext()
                self.parent.state=NEXTPLAYER
                self.parent.instructionbox.insert(Ttk.END, " Hey %s, draw a card\n"%(self.parent.player))
                self.parent.master.update()
                self.parent.setoptions()
            self.renamef.destroy()

def talktome(phrase):
    command='spd-say -p 50 \"%s\"'%phrase
    print(command)  #FIXPRNT
    subprocess.call(command,shell=True)

def message(mess,istext=False,app=None):
    if istext:
        print(mess)  #FIXPRNT
    else:
        app.instructionbox.insert(Ttk.END, mess)

def playserial(player): #{
   print("\nHey %s, it's your turn."%player)  #FIXPRNT
   # take a turn according to the rules
   its_my_turn=True
   tscore=0
   # rule 1: turn a card to start and after each fill
   while its_my_turn:	# { turn loop
        #tscore=0
        filled=0
        mfills=1
        card=ctype(deck.draw())
        if testing:
            tcard = raw_input(' for testing, input a card: ')
            if len(tcard)>0:
                card = tcard
        print("  %s drew %s"%(player, card))  #FIXPRNT
        response=respond(player,' hit return ')
        if card =='Vengeance':
           if player not in leadingPlayers:
                print("Do you want to seek vengeance?")  #FIXPRNT
                response=respond(player,' y or n ').upper()
                if response != 'Y' and response != 'YES':
                   continue
           else:
                print('  but you can\'t take vengeance on yourself.')  #FIXPRNT
                continue
        if card =='No Dice':
            its_my_turn=False
        else:
            # Roll all the dice
            if card == 'Double Trouble':
                mfills=2
            while filled<mfills:  # { multi-fills loop
                dice=Dice()
                if testing:
                    tstr= raw_input('test first roll: ')
                    if len(tstr)>0:
                        dice.dice=[int(a) for a in tstr]
                print('   first roll is ',dice.dice)  #FIXPRNT
                # get potential score
                pscore,preserve,dummy=dice.scored(list(range(6)))
                if pscore == 0:	#{ BUSTED on full roll
                   if 'Bonus' in card or 'Fill' in card or 'Veng' in card:
                        print(' Gee %s, you busted right away'%player)  #FIXPRNT
                        #filled=mfills
                        its_my_turn=False
                        tscore=0
                        break	# out of fills loop
                   elif card == 'Double Trouble':
                        if filled==1:
                           print(" Just couldn't fill it the second time")  #FIXPRNT
                        else:
                           print('  Gee %s, you busted right away'%player)  #FIXPRNT
                        tscore=0
                        its_my_turn=False
                        #filled=mfills
                        break	# out of fills loop
                   else:        # Must Bust did
                        if tscore>0:
                           print('  %s , you scored %d so far'%(player,tscore))  #FIXPRNT
                           print('  Do you want to keep this score or turn another card?')  #FIXPRNT
                           response=respond(player,' d to draw another ')
                           if len(response)>0 and response.upper()[0]=='D':
                                its_my_turn=True
                           else:
                                players[player].update(tscore)
                                its_my_turn=False
                        #filled=mfills
                        else:
                           print('  Gee %s, you busted right away'%player)  #FIXPRNT
                           its_my_turn=False
                        break	# out of fills loop
                #}
                if len(preserve)==6: #{ filled on full roll
                   print('!! filled on the first roll')  #FIXPRNT
                   dice.score=pscore
                   filled+=1
                   if card == 'Vengeance':
                        tscore+=pscore
                        print('  !! Vengeance !!')  #FIXPRNT
                        for leader in leadingPlayers:
                           players[leader].update(-2500)
                           print('and '+leader+' ',)  #FIXPRNT
                        print( 'now has %d'%players[leadingPlayers[0]].score)  #FIXPRNT
                        players[player].update(tscore)
                        print('    %s score is now %d\n   ,'%(player,players[player].score))  #FIXPRNT
                        print('  %s, take another turn'%player)  #FIXPRNT
                        tscore=0
                        mfills=0
                        break	# out of fills loop
                   elif card == 'Double Trouble':
                        tscore+=pscore*2
                        if filled == 2:
                           players[player].update(tscore)
                           print('  %s, take another turn'%player)  #FIXPRNT
                           tscore=0
                           mfills=0
                           break        # out of fills loop
                        print(' but you need to fill it twice to score')  #FIXPRNT
                        continue	# to start of fills loop
                   elif 'Bonus' in card or 'Fill' in card:
                        bonus=int(card[5:])
                        print('\n  Do you want to end your turn and keep the %d point score'%(tscore+pscore+bonus))  #FIXPRNT
                        print('  or risk it by taking another card?')  #FIXPRNT
                        tscore+=pscore+bonus
                        response = (respond(player,'   r to risk it ')).lower()
                        if len(response)>0 and response[0]=='r':
                           its_my_turn=True
                        else:
                           return tscore  #CHECK THIS
                           its_my_turn=False
                        mfills=filled
                        #pscore=0
                        break	# out of fills loop
                   elif card == 'Must Bust':
                        tscore+=pscore
                        print('\n  Score for this turn is up to %d points'%tscore)  #FIXPRNT
                        print('  But don\'t stop now.')  #FIXPRNT
                        mfills=filled+1
                        continue	# top of fills loop
                #}
                # continue rolling until filled, busted, or risk-averse
                while pscore>0:	# {
                   print('   potential score = %d by keeping %s'%(pscore,preserve))  #FIXPRNT
                   if card == 'Must Bust':
                        # add all the scoring dice and go on
                        tscore+=pscore
                        dice.reserve(preserve)
                   else:
                        #select dice to score
                        selection_good=False
                        while not selection_good:
                           print('   Choose which dice to keep')  #FIXPRNT
                           response=respond(player,'list ,ie 014 : ')
                           if len(response)== 0:
                                dlist=list(range(6-len(dice.reserved)))
                           else:
                                if check_response(response):
                                   dlist=[int(a) for a in response]
                                   pscore,preserve,dummy=dice.scored(dlist)
                                else: pscore=0
                           if pscore>0:
                                selection_good=True
                           else:
                                print('  !! invalid selection !!')  #FIXPRNT
                        dice.reserve(preserve)
                        	
                   numtoroll=6-len(dice.reserved)
                   if card == 'Double Trouble':
                        tscore+=pscore*2
                   elif card == 'Fill 1000' or card == 'Vengeance':
                        tscore+=pscore
                   elif 'Bonus' in card:
                        tscore+=pscore
                        print('    Do you want to risk %d points by rolling the remaining %d dice?'%(tscore,numtoroll))  #FIXPRNT
                        print('    Or do you want to take this score and end your turn?')  #FIXPRNT
                        response=respond(player,'     r to roll and risk it: ')
                        if len(response)>0 and response.lower()[0] == 'r':
                           its_my_turn=True
                        else:
                           players[player].update(tscore)
                           mfills=filled
                           its_my_turn=False
                           break	# out of rolling loop
                   dice.dice=dice.roll()
                   if testing:
                        testroll = raw_input(' testing roll: ')[:numtoroll]
                        if len(testroll)>0:
                            dice.dice=[int(a) for a in testroll]+dice.dice[numtoroll:]
                   print('   next roll: ',dice.dice[:numtoroll], '||',dice.dice[numtoroll:])  #FIXPRNT
                   pscore,preserve,dummy=dice.scored(list(range(numtoroll)))
                   if len(preserve)+len(dice.reserved)== 6:  #{ it is filled
                        filled+=1
                        print('  ! You filled it !')  #FIXPRNT
                        if card == 'Vengeance':
                           tscore+=pscore
                           print('  !! Vengeance !!')  #FIXPRNT
                           for leader in leadingPlayers:
                                players[leader].update(-2500)
                                print('and '+leader+' ',)  #FIXPRNT
                           print('now have %d'%players[leadingPlayers[0]].score)  #FIXPRNT
                           players[player].update(tscore)
                           print('    %s score is now %d\n   ,'%(player,players[player].score))  #FIXPRNT
                           print('  %s, take another turn'%player)  #FIXPRNT
                           tscore=0
                           its_my_turn=True
                           break	# out of rolling loop
                        elif card == 'Double Trouble':
                           tscore+=pscore*2
                           if filled == 2:
                                players[player].update(tscore)
                                print('  %s, take another turn'%player)  #FIXPRNT
                                tscore=0
                                its_my_turn=True
                                break	# out of rolling loop
                           else:
                                print('   You have to fill it again. Good luck')  #FIXPRNT
                           break        # out of rolling loop
                        elif 'Bonus' in card or 'Fill' in card:
                           bonus=int(card[5:])
                           tscore+=pscore+bonus
                           mfills=filled-1
                           print('    Do you want to risk %d points by continuing?'%tscore)  #FIXPRNT
                           print('    Or do you want to take this score and end your turn?')  #FIXPRNT
                           response=respond(player,'     r to risk it: ')
                           if len(response)>0 and response.lower()[0] == 'r':
                                its_my_turn=True
                           else:
                                players[player].update(tscore)
                                its_my_turn=False
                           break	# out of rolling loop
                        elif card == 'Must Bust':
                           tscore+=pscore
                           print('\n  Score for this turn is up to %d points'%tscore)  #FIXPRNT
                           print('  But don\'t stop now.')  #FIXPRNT
                           mfills=filled+1
                           break	# out of rolling loop
                   #}
                else: #}  finished rolling cause you busted
                    print('   !!! BUSTED !!!')  #FIXPRNT
                    mfills=filled
                    its_my_turn=False
                    #break	# out of fills loop
                if debug: print('  DEBUG: %s, bottom of fills loop, tscore,pscore,filled,mfills= ',card,tscore,pscore,filled,mfills)  #FIXPRNT
                if card == 'Must Bust':
                    if pscore==0:
                        mfills=filled
                        tscore+=pscore
                        print('  Do you want to risk %d points by drawing another card?'%tscore)  #FIXPRNT
                        print('  or do you want to keep this score and end your turn')  #FIXPRNT
                        response=respond(player,'   d to draw a card ')
                        if len(response)>0 and response.lower()[0]=='d':
                            its_my_turn=True
                        else:
                            players[player].update(tscore)
                            its_my_turn=False
            #}	fills loop
        #}	turn loop
   return tscore
#}

def write_state(players, cards, currentplayer, goalscore, safile="resume.FrB"):
    ''' write restart file for current game
    '''
    filep=open(safile,'w')
    date=datetime.date.today()
    # players
    filep.write("FillRBust game saved %d/%d/%d\n %d players\n"%(
                          date.month,date.day,date.year, len(players)))
    for each in players:
        #  name, scores, ai, airisk
        filep.write("\"%s\", %d, %d\n"%(each.name, each.score, 
                                        each.risker if each.isai else -1))
    # cards left
    filep.write(" %d card left in deck:\n"%len(cards))
    for each in cards:
        filep.write("%d "%each)
    filep.write("\n")
    # whose turn on resumption
    filep.write("next player up \"%s\"\n"%currentplayer)
    # score goal
    filep.write("score to win is %d\n"%goalscore)
    filep.close()

def readSaved(filename, debug=False):
    ''' Extract state of previous game from a state file.
        Include player names and scores, remaining cards,
        goal score, and player to start.'''
    try:
        filep=open(filename,'r')
        line=filep.readline().strip().split()
        if debug:
            print(" Reading game saved %s"%line[3])
        nplayers=int(filep.readline().strip().split()[0])
        names=[]
        scores=[]
        for ii in range(nplayers):
            line=filep.readline().strip().split(',')
            names.append(line[0].strip('"'))
            scores.append(int(line[1]))
        decksize=int(filep.readline().strip().split()[0])
        deck=[int(ii) for ii in filep.readline().strip().split()]
        current=filep.readline().strip().split('"')[1]
        goal=int(filep.readline().strip().split()[4])
    except IOError:
        #return names,scores,cards,goal,current
        return []    ,[]    ,[]   ,0   ,""

    return names,scores,deck,goal,current

if __name__ == '__main__':
    import os,sys,getopt
    
    winningScore=0
    defaultnames=[]
    gui=True
    speak=False
    dicedir="."
    carddir="."
    #dicedir="Dice/FreeCad"

    def Usage():
        print('Fill\'RBust')
        print(' Usage: fillrbust.py [options]')
        print('where options are')
        print('    -m val	set winning score')
        print('    -p name	add player')
        print('    multiple players are typically specified.')
        print('    -t		don\'t use graphical user interface')

    def check_response(response):
        ''' response to set of dice to keep should be a set of integers
                no repeats
                non-negative
                in range 0-5'''
        if not response.isdigit(): return False
        if len(response)>6: return False
        if int(response[-1])>5: return False
        b=response[0]
        for a in response[1:]:
            if a>b:
                b=a
            else:
                return False
        return True

    try:
        options, args=getopt.getopt(sys.argv[1:],'dtm:p:TGsr:D:C:')
    except getopt.GetoptError:
        print('Caught getopt.GetoptError')
        Usage()
        sys.exit(1)
    gtesting=False	# GUI testing
    testing=False	# other testing
    debug=False
    names=[]
    scores=[]
    resumeGame=False
    resumename=""
    for opt, par in options:
        if opt == '-d':
             debug=True
        elif opt == '-T':
            testing=True
            print('!!!!!!!!!!!!!!!\n\n T option for testing\n\n!!!!!!!!!!!!!!!!\n')
        elif opt == '-G':
            gtesting=True
            print('!!!!!!!!!!!!!!!\n\n G option for testing GUI\n\n!!!!!!!!!!!!!!!!\n')
        elif opt == '-m':
            winningScore=int(par)
        elif opt == '-p':
            names.append(par)
            scores.append(0)
        elif opt == '-t':
            gui=False
        elif opt == '-s':
            speak=True
        elif opt == '-r':
            resumename=par
            resumeGame=True
        elif opt == '-D':
            dicedir="Dice/%s"%par
        elif opt == '-C':
            carddir="Cards/%s"%par
    tscore=0
    filled=0
    current=""
    if resumeGame:
        names,scores,cards,winningScore,current=readSaved(resumename)

    if gui:
        root = Ttk.Tk()
        root.title("Fill\'RBust")

        app = App(root,names=names,goal=winningScore, scores=scores, current=current)

        root.mainloop()
    else:
        # build deck
        deck=Cards()

        # assemble players
        players={}
        if len(names)==0:
            names=defaultnames
        for player in names:
            if player[:2]=='ai':
                fact=player[-1]
                if fact.isdigit():
                    fact=int(fact)
                else:
                    fact=5
                players[player]=AIPlayer(player,risker=fact)
                print('added %s as AIPlayer with risk %d/10'%(player,fact))
            else:
                players[player]=Player(player)
        maxScore=players[players.keys()[0]].score
        leadingPlayers=deepcopy(names)
    
        # play the game until someone wins
        while maxScore < winningScore:
            for player in names:
                tscore=playserial(player)
                print('%s score is %d'%(player,players[player].score))
                
                # check leading score
                if players[player].score>maxScore:
                    maxScore=players[player].score
                    if player not in leadingPlayers:
                        print('%s just took the lead, %d.\n'%(player,players[player].score))
                    leadingPlayers=[player]
                elif players[player].score == maxScore:
                    leadingPlayers.append(player)

        print('\n-------Final Score--------')
        for player in players.keys():
            print('   %s : %d'%(player, players[player].score))

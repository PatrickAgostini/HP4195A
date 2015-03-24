# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 17:15:22 2015

@author: Jochen
"""

#from plot2ax import plot2ax
from Tkinter import *
from ttk import Notebook, Labelframe

matplotlib.use('TkAgg')
#import matplotlib

import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

#from PIL import Image, ImageTk
import threading

class MainWindow(threading.Thread):
    
    def __init__(self):       
        #threading.Thread.__init__(self)
        #self.start()
        
    #def run(self):
        self.root = Tk()
        
        self.root.wm_title("HP4195A User Interface")
        #self.root.protocol("WM_DELETE_WINDOW", self.destructor)
        self.init()
        
    def destructor(self):
        #self.worker.stp() 
        self.root.quit()
        print("finished")
        
    def init(self):     
        
        self.plotInterval = 10        
        
        self.measFuncVar =IntVar()
        self.angleMode =IntVar()
        self.portNetwork = IntVar()
        self.formatNetwork = IntVar()
        self.dfreq = DoubleVar()
        # Stimulus Variables
        self.sweepParameter = IntVar()
        self.startFreqStr = StringVar()
        self.stopFreqStr = StringVar()
        self.centerFreqStr = StringVar()
        self.spanStr = StringVar()
        self.sweepType = IntVar()
        self.nopStr = StringVar()
        self.stepStr = StringVar()
        self.swpTimeStr = StringVar()
        self.stepStr = StringVar()
        self.spotFreqStr = StringVar()
        self.osc1LvlStr = StringVar()
        self.osc2LvlStr = StringVar()
        self.triggerMode = StringVar()
        self.iFModeRest = IntVar()
        self.inpAttR1 = StringVar()
        self.inpAttR2 = StringVar()
        self.inpAttT1 = StringVar()
        self.inpAttT2 = StringVar()
        self.portExtR1 = StringVar()
        self.portExtR2 = StringVar()
        self.portExtT1 = StringVar()
        self.portExtT2 = StringVar()
        self.portExtP1 = StringVar()
        self.portExtP2 = StringVar()
        self.calMode = IntVar()
        
        
        self.checkIsncalNetwork = BooleanVar()
        self.checkShortNetwork = BooleanVar()
        self.calibStepCounter = 0
        
        # Calibration Settings
        self.charImp = IntVar()
        self.openCond = StringVar()
        self.openCap = StringVar()
        self.ldRes = StringVar()
        self.ldInd = StringVar()
        self.shtRes = StringVar()
        self.shtInd = StringVar()
        self.correctn = BooleanVar()
        
        
      
        ###### plot #########
        self.xLbl = ''
        self.yLbl = '' #will contain up to 2 Strings depending on measFuncVar
        
        
        self.menubar=None
        self.note=None
        
        self.maintab=None
        self.stimulustab=None
        self.receivertabRest=None
        self.receivertabSpectrum=None
        self.calibrationtabNetwork=None
        
        self.setMenuBar()
        self.setTabBar()     
        
        #self.setSettingsTabNetwork()
        self.buildSettingsTabNetwork()
        self.buildStimulustab()
        self.buildMaintab()
        self.buildCalibrationtabNetwork()
        self.buildReceivertabRest()
        
        self.show()
            
            
    ###########################################################################
    # Menu Bar
    def setMenuBar(self):
        menubar = Menu(self.root)
        # File-Menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        
       
        # Measurement Function Menu
        measfuncmenu = Menu(menubar, tearoff=0)
        MODES = [   ('Network' , 1),
                    ('Spectrum', 2),
                    ('Impedance', 3),
                    ('S11', 4),
                    ('S21', 5),
                    ('S12', 6),
                    ('S22', 7)  
        ]
        for text, mode in MODES:
            measfuncmenu.add_radiobutton(label=text, variable=self.measFuncVar, value=mode, command=self.measFuncCall)    
        self.measFuncVar.set(1)
        menubar.add_cascade(label="Measurement Function", menu=measfuncmenu)
         
       
        
        # display the menu
        self.root.config(menu=menubar)
        
    ###########################################################################
    # Tab Bar  
    def setTabBar(self):    
        self.note = Notebook(self.root) 
        self.note.pack(fill=BOTH,expand=1)
        
        self.maintab = Frame(self.note)
        self.stimulustab = Frame(self.note)
        self.receivertabRest = Frame(self.note)
        self.receivertabSpectrum = Frame(self.note)
        self.calibrationtabNetwork = Frame(self.note)
        self.calibrationtabImpedance = Frame(self.note)
        self.calibrationtabS = Frame(self.note)
        self.settingstabNetwork = Frame(self.note)
        self.settingstabSpectrum = Frame(self.note)
        self.settingstabImpedance = Frame(self.note)
        self.settingstabS1122 = Frame(self.note)
        self.settingstabS2112 = Frame(self.note)
    

        
        
        self.note.add(self.maintab, text = "Main", compound=TOP)
        self.note.add(self.stimulustab, text = "Stimulus")
        self.note.add(self.receivertabRest, text = "Receiver")
        self.note.add(self.receivertabSpectrum, text = "Receiver")
        self.note.add(self.calibrationtabNetwork, text = "Calibration")
        self.note.add(self.calibrationtabImpedance, text = "Calibration")
        self.note.add(self.calibrationtabS, text = "Calibration")
        self.note.add(self.settingstabNetwork, text = "Settings")
        self.note.add(self.settingstabSpectrum, text = "Settings")
        self.note.add(self.settingstabImpedance, text = "Settings")
        self.note.add(self.settingstabS1122, text = "Settings")
        self.note.add(self.settingstabS2112, text = "Settings")


        
        
        self.setActiveTabs()
        
        
        
    
        
    def setActiveTabs(self):
        self.note.tab(self.maintab,state = "normal") 
        self.note.tab(self.stimulustab,state = "normal") 
        
        if self.measFuncVar.get()==1: #Network
            self.note.tab(self.receivertabRest,state = "normal")
            self.note.tab(self.receivertabSpectrum,state = "hidden")
            self.note.tab(self.calibrationtabNetwork,state = "normal")
            self.note.tab(self.calibrationtabImpedance, state = "hidden")
            self.note.tab(self.calibrationtabS, state = "hidden")
            self.note.tab(self.settingstabNetwork, state = "normal")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==2: #Spectrum
            self.note.tab(self.receivertabRest,state = "hidden")
            self.note.tab(self.receivertabSpectrum,state = "normal")
            self.note.tab(self.calibrationtabNetwork,state = "hidden")
            self.note.tab(self.calibrationtabImpedance, state = "hidden")
            self.note.tab(self.calibrationtabS, state = "hidden")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "normal")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==3: #Impedance
            self.note.tab(self.receivertabRest,state = "normal")
            self.note.tab(self.receivertabSpectrum,state = "hidden")
            self.note.tab(self.calibrationtabNetwork,state = "hidden")
            self.note.tab(self.calibrationtabImpedance, state = "normal")
            self.note.tab(self.calibrationtabS, state = "hidden")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "normal")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==4 or self.measFuncVar.get()==7: #S11 or S21
            self.note.tab(self.receivertabRest,state = "normal")
            self.note.tab(self.receivertabSpectrum,state = "hidden")
            self.note.tab(self.calibrationtabNetwork,state = "hidden")
            self.note.tab(self.calibrationtabImpedance, state = "hidden")
            self.note.tab(self.calibrationtabS, state = "normal")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "normal")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==5 or self.measFuncVar.get()==6: #S21 or S12
            self.note.tab(self.receivertabRest,state = "normal")
            self.note.tab(self.receivertabSpectrum,state = "hidden")
            self.note.tab(self.calibrationtabNetwork,state = "hidden")
            self.note.tab(self.calibrationtabImpedance, state = "hidden")
            self.note.tab(self.calibrationtabS, state = "normal")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "normal")
        
    
        
        
    def buildSettingsTabNetwork(self):
        pwFull = PanedWindow(self.settingstabNetwork,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        pw1 = PanedWindow(pwFull,orient=HORIZONTAL)
        pw1.pack(fill=BOTH,expand=1)
        lblPort = Labelframe(pw1, text='Port', width=100, height=100)
        PORTS = [
            ('T1/R1', 1),
            ('T2/R1', 2),
            ('R2/R1', 3),
            ('T1/R2', 4),
            ('T2/R2', 5)
        ]     
        for text, port in PORTS:
            rbPort = Radiobutton(lblPort,text=text, variable=self.portNetwork,value=port, command=self.printPortNetwork)
            rbPort.pack(anchor=W)
        self.portNetwork.set(1)
        pw1.add(lblPort)
        
        lblFmt = Labelframe(pw1,text="Format", width=100,height=100)
        FMTS = [
            ('Gain(dB)-Phase', 1),
            ('Gain-Phase', 2),
            ('Gain Re-Im', 3),
            ('Gain(dB)-GrpDel', 4)
        ]   
        for text, fmt in FMTS:
            rbFmt = Radiobutton(lblFmt,text=text, variable=self.formatNetwork,value=fmt)
            rbFmt.pack(anchor=W)
        self.formatNetwork.set(1)
        pw1.add(lblFmt)
        
        
        
        pw2 = PanedWindow(pwFull,orient=VERTICAL)
        pw2.pack()
        
        lblAngle = Labelframe(pw2,text="Angle Mode", width=100,height=100)
        MODES = [   ('Deg' , 1),
                    ('Rad', 2)
        ]
        for text, mode in MODES:
            rbAngle=Radiobutton(lblAngle,text=text, variable=self.angleMode, value=mode)
            rbAngle.pack(anchor=W)
        self.angleMode.set(1)
        pw2.add(lblAngle)
        
        lblDf = Labelframe(pw2,text="Delay Aperture", width=100,height=100)
        sDf = Scale(master=lblDf,from_=0.5, to=100, resolution=0.5,variable=self.dfreq, orient=HORIZONTAL,sliderlength=15)
        sDf.pack(fill=BOTH,padx=5)        
        self.dfreq.set(0.5)        
        pw2.add(lblDf)
        pw1.add(pw2)
        
        ySpacing = 2
        frPortExt = Labelframe(pwFull,text = "Port Extension [cm]")
        frPortExt.pack(fill=BOTH,expand=1)
        
        frPortExtR = Frame(frPortExt)  
        frPortExtT = Frame(frPortExt)  
        frPortExtP = Frame(frPortExt)
        frPortExtR.pack(side="left",fill=BOTH,expand=1)
        frPortExtT.pack(side="left",fill=BOTH,expand=1)
        frPortExtP.pack(side="left",fill=BOTH,expand=1)
        
        frR1=Frame(frPortExtR)
        lblR1=Label(frR1, text="R1:", height=ySpacing)
        lblR1.pack(side="left")   
        ePortExtR1=Entry(frR1,textvariable=self.portExtR1,width=8)
        ePortExtR1.bind('<Return>',self.ePortExtR1Callback)
        ePortExtR1.pack(side="left")
        frR1.pack()
        ePortExtR1.pack(fill=X,anchor=E,padx=5)
        
        
        frR2=Frame(frPortExtR)
        lblR2=Label(frR2, text="R2:", height=ySpacing)
        lblR2.pack(side="left")   
        ePortExtR2=Entry(frR2,textvariable=self.portExtR2,width=8)
        ePortExtR2.bind('<Return>',self.ePortExtR2Callback)
        ePortExtR2.pack(side="left")
        frR2.pack()
        ePortExtR2.pack(fill=X,anchor=E,padx=5)
        
        frT1=Frame(frPortExtT)
        lblT1=Label(frT1, text="T1:", height=ySpacing)
        lblT1.pack(side="left")   
        ePortExtT1=Entry(frT1,textvariable=self.portExtT1,width=8)
        ePortExtT1.bind('<Return>',self.ePortExtT1Callback)
        ePortExtT1.pack(side="left")
        frT1.pack()
        ePortExtT1.pack(fill=X,anchor=E,padx=5)
        
        
        frT2=Frame(frPortExtT)
        lblT2=Label(frT2, text="T2:", height=ySpacing)
        lblT2.pack(side="left")   
        ePortExtT2=Entry(frT2,textvariable=self.portExtT2,width=8)
        ePortExtT2.bind('<Return>',self.ePortExtT2Callback)
        ePortExtT2.pack(side="left")
        frT2.pack()
        ePortExtT2.pack(fill=X,anchor=E,padx=5)
        
        frP1=Frame(frPortExtP)
        lblP1=Label(frP1, text="P1:", height=ySpacing)
        lblP1.pack(side="left")   
        ePortExtP1=Entry(frP1,textvariable=self.portExtP1,width=8)
        ePortExtP1.bind('<Return>',self.ePortExtP1Callback)
        ePortExtP1.pack(side="left")
        frP1.pack()
        ePortExtP1.pack(fill=X,anchor=E,padx=5)
        
        
        frP2=Frame(frPortExtP)
        lblP2=Label(frP2, text="P2:", height=ySpacing)
        lblP2.pack(side="left")   
        ePortExtP2=Entry(frP2,textvariable=self.portExtP2,width=8)
        ePortExtP2.bind('<Return>',self.ePortExtP2Callback)
        ePortExtP2.pack(side="left")
        frP2.pack()
        ePortExtP2.pack(fill=X,anchor=E,padx=5)
        
        pwFull.add(pw1)
        pwFull.add(frPortExt)
        
    def buildStimulustab(self):
        f = Frame(self.stimulustab)
        f.pack(fill=BOTH,expand=1)
        ySpacing = 2
        
        pwFull = PanedWindow(f,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        
        
        pwTop = PanedWindow(pwFull,orient=HORIZONTAL)
        #pwTop.pack(fill=BOTH)
        
        pwLeft = PanedWindow(pwTop,orient=VERTICAL)
        pwLeft.pack(fill=BOTH)
        frSwpParam = Labelframe(pwLeft,text="Sweep Parameter", width=100,height=100)
        frSwpParam.pack(fill=BOTH)
        
        SWPS = [
            ('Frequency [Hz]', 1),
            ('DC Bias [V]', 2),
            ('Osc Lvl [V]', 3),
            ('Osc Lvl [dBm]', 4),
            ('Osc Lvl [dBµV]', 5)
        ]   
        for text, swp in SWPS:
            rbSwpParam = Radiobutton(frSwpParam,text=text, variable=self.sweepParameter,value=swp)
            rbSwpParam.pack(anchor=W)
        self.sweepParameter.set(1) 
        
        pwLeft.add(frSwpParam)
        
        frSwt = Labelframe(pwLeft, text="Sweep Type", width=100,height=100)
        frSwt.pack(fill=BOTH)
        MODES = [   ('Linear' , 1),
                    ('Logarithmic', 2),
        ]
        for text, mode in MODES:
            rbSwt=Radiobutton(frSwt,text=text, variable=self.sweepType, value=mode)
            rbSwt.pack(anchor=W)
        self.sweepType.set(1)
        pwLeft.add(frSwt)
        pwTop.add(pwLeft)
        
        
        frSwpRange = Labelframe(pwTop,text="Sweep Range", width=100,height=100)
        frSwpRange.pack(fill=BOTH)
        
        frStart=Frame(frSwpRange)
        lblStart=Label(frStart, text="Start:", height=ySpacing)
        lblStart.pack(side="left")   
        eStart=Entry(frStart,textvariable=self.startFreqStr,width=8)
        eStart.bind('<Return>',self.eStartCallback)
        eStart.pack(side="right")
        #unitStart=Label(frStart, text="Hz", height=4)
        #unitStart.pack(side="left")
        frStart.pack(fill=X,anchor=E,padx=5)
        
        frStop=Frame(frSwpRange)
        lblStop=Label(frStop, text="Stop:", height=ySpacing)
        lblStop.pack(side="left")   
        eStop=Entry(frStop,textvariable=self.stopFreqStr,width=8)
        eStop.bind('<Return>',self.eStopCallback)
        eStop.pack(side="right")
        #unitStop=Label(frStop, text="Hz", height=4)
        #unitStop.pack(side="left")
        frStop.pack(fill=X,anchor=E,padx=5)        
        
        frCenter=Frame(frSwpRange)
        lblCenter=Label(frCenter, text="Center:", height=ySpacing)
        lblCenter.pack(side="left")   
        eCenter=Entry(frCenter,textvariable=self.centerFreqStr,width=8)
        eCenter.bind('<Return>',self.eCenterCallback)
        eCenter.pack(side="right")
        #unitCenter=Label(frCenter, text="Hz", height=4)
        #unitCenter.pack(side="left")
        frCenter.pack(fill=X,anchor=E,padx=5)   
        
        frSpan=Frame(frSwpRange)
        lblSpan=Label(frSpan, text="Span:", height=ySpacing)
        lblSpan.pack(side="left")   
        eSpan=Entry(frSpan,textvariable=self.spanStr,width=8)
        eSpan.bind('<Return>',self.eSpanCallback)
        eSpan.pack(side="right")
        frSpan.pack(fill=X,anchor=E,padx=5) 
        
        pwTop.add(frSwpRange)
        
        pwRight = PanedWindow(pwTop,orient=VERTICAL)
        pwRight.pack(fill=BOTH)
        frTrigMode = Labelframe(pwRight, text="Trigger Mode", width=100,height=100)
        frTrigMode.pack(fill=BOTH)
        
        MODES = [   ('Continuous' , 1),
                    ('Single', 2),
                    ('Manual', 3)
        ]
        for text, mode in MODES:
            rbTrigMode=Radiobutton(frTrigMode,text=text, variable=self.triggerMode, value=mode)
            rbTrigMode.pack(anchor=W)
        self.triggerMode.set(1)
        pwRight.add(frTrigMode)
        
        frRes = Labelframe(pwRight, text="Resolution", width=100,height=100)
        frRes.pack(fill=BOTH)
        
        frNop=Frame(frRes)
        lblNop=Label(frNop, text="# Points:", height=ySpacing)
        lblNop.pack(side="left")   
        eNop=Entry(frNop,textvariable=self.nopStr,width=8)
        eNop.bind('<Return>',self.eNopCallback)
        eNop.pack(side="right")
        frNop.pack(fill=X,anchor=E,padx=5) 
        
        frStep=Frame(frRes)
        lblStep=Label(frStep, text="Step:", height=ySpacing)
        lblStep.pack(side="left")   
        eStep=Entry(frStep,textvariable=self.stepStr,width=8)
        eStep.bind('<Return>',self.eStepCallback)
        eStep.pack(side="right")
        frStep.pack(fill=X,anchor=E,padx=5) 
        
        frSwpTime=Frame(frRes)
        lblSwpTime=Label(frSwpTime, text="Swp Time:", height=ySpacing)
        lblSwpTime.pack(side="left")   
        eSwpTime=Entry(frSwpTime,textvariable=self.swpTimeStr,width=8)
        eSwpTime.bind('<Return>',self.eSwpTimeCallback)
        eSwpTime.pack(side="right")
        frSwpTime.pack(fill=X,anchor=E,padx=5) 
        
        pwRight.add(frRes)
        pwTop.add(pwRight)
        pwFull.add(pwTop)
        
        frNonSwp = Labelframe(pwFull,text="Non-Sweep Parameters", width=100,height=100)
        frNonSwp.pack(fill=BOTH)
        
        frSpot=Frame(frNonSwp)
        lblSpot=Label(frSpot, text="Spot Freq:", height=ySpacing)
        lblSpot.pack(side="left")   
        eSpot=Entry(frSpot,textvariable=self.spotFreqStr,width=8)
        eSpot.bind('<Return>',self.eSpotCallback)
        eSpot.pack(side="left")
        frSpot.pack(side="left",padx=5) 
        
        frOsc1=Frame(frNonSwp)
        lblOsc1=Label(frOsc1, text="Osc1 Lvl:", height=ySpacing)
        lblOsc1.pack(side="left")   
        eOsc1=Entry(frOsc1,textvariable=self.osc1LvlStr,width=8)
        eOsc1.bind('<Return>',self.eOsc1Callback)
        eOsc1.pack(side="left")
        frOsc1.pack(side="left",padx=5) 
        
        frOsc2=Frame(frNonSwp)
        lblOsc2=Label(frOsc2, text="Osc2 Lvl:", height=ySpacing)
        lblOsc2.pack(side="left")   
        eOsc2=Entry(frOsc2,textvariable=self.osc2LvlStr,width=8)
        eOsc2.bind('<Return>',self.eOsc2Callback)
        eOsc2.pack(side="left")
        frOsc2.pack(side="left",padx=5) 
        
        pwFull.add(frNonSwp)
        
    def startPlotting(self):
        if self.plotRun:
            self.plotThread.start()
        else:
            self.plotThread.stop()
        self.plotRun = not self.plotRun
        
        
    def buildMaintab(self):
        self.fig = plt.figure()
        
        self.ax1 = self.fig.add_subplot(111)    
        self.ax2 = self.ax1.twinx()
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.maintab)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.config(highlightthickness=2, bd=0, relief=SUNKEN,highlightcolor='grey')
        self.canvas._tkcanvas.pack(anchor=NW,fill=BOTH,expand=1)
        
        'Periodic Plotting'
        self.plotThread = self.canvas.new_timer()
        self.plotThread.add_callback(self.plot)
        self.plotThread._set_interval(self.plotInterval)
        self.plotRun = False
        
        refreshButton = Button(self.maintab,text="Refresh",command=self.startPlotting)
        refreshButton.pack()
        
        self.ax1.set_axis_bgcolor('black')
        self.ax2.set_axis_bgcolor('none')
        self.fig.set_facecolor('black')
        
        
        self.ax2.spines['top'].set_color([.5, .5, .5])
        self.ax2.spines['bottom'].set_color([.5, .5, .5])
        self.ax2.spines['left'].set_color([.5, .5, .5])
        self.ax2.spines['right'].set_color([.5, .5, .5])
        self.ax1.xaxis.label.set_color([.8, .8, .8])
        self.ax1.tick_params(axis='x', colors=[.8, .8, .8])       
        
        self.plot()
        
    def buildReceivertabRest(self):
        pw2 = PanedWindow(self.receivertabRest,orient=VERTICAL)
        pw2.pack(fill=BOTH,expand=1)
        pw1 = PanedWindow(pw2,orient = HORIZONTAL)
        pw1.pack(fill=BOTH,expand=1)
        frIFRest = Labelframe(pw1,text="IF Mode", width=100,height=100)
        IFMODES = [
                ('Normal' , 1),
                ('Low Distortion', 2),
                ('High Sensitivity', 3)
        ]
        for text, mode in IFMODES:
            self.rbIFRest = Radiobutton(frIFRest,variable = self.iFModeRest, text=text,value=mode)
            self.rbIFRest.pack(anchor=W)
        self.iFModeRest.set(1)
        pw1.add(frIFRest)
        frResBW = Labelframe(pw1,text="Resolution BW [Hz]",height=100, width=100)
        rbwList = ('Auto',3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000)
        self.sbResBW = Spinbox(frResBW,values=rbwList)
        self.sbResBW.pack()
        frResBW.pack(anchor=W)
        pw1.add(frResBW)
        pw2.add(pw1)
        
        ySpacing = 2
        
        frInputAtt = Labelframe(pw2,text = "Input Attenuation [dB]")
        frInputAtt.pack(fill=BOTH,expand=1)
        
        frInputAttR = Frame(frInputAtt)  
        frInputAttT = Frame(frInputAtt)  
        frInputAttR.pack(side="left",fill=BOTH,expand=1)
        frInputAttT.pack(side="left",fill=BOTH,expand=1)
        
        frR1=Frame(frInputAttR)
        lblR1=Label(frR1, text="R1:", height=ySpacing)
        lblR1.pack(side="left")   
        eR1=Entry(frR1,textvariable=self.inpAttR1,width=8)
        eR1.bind('<Return>',self.eInpAttR1Callback)
        eR1.pack(side="left")
        frR1.pack()
        eR1.pack(fill=X,anchor=E,padx=5)
        
        frR2=Frame(frInputAttR)
        lblR2=Label(frR2, text="R2:", height=ySpacing)
        lblR2.pack(side="left")   
        eR2=Entry(frR2,textvariable=self.inpAttR2,width=8)
        eR2.bind('<Return>',self.eInpAttR2Callback)
        eR2.pack(side="left")
        frR2.pack()
        eR2.pack(fill=X,anchor=E,padx=5)
        
        frT1=Frame(frInputAttT)
        lblT1=Label(frT1, text="T1:", height=ySpacing)
        lblT1.pack(side="left")   
        eT1=Entry(frT1,textvariable=self.inpAttT1,width=8)
        eT1.bind('<Return>',self.eInpAttT1Callback)
        eT1.pack(side="left")
        frT1.pack()
        eT1.pack(fill=X,anchor=E,padx=5)
        
        frT2=Frame(frInputAttT)
        lblT2=Label(frT2, text="T2:", height=ySpacing)
        lblT2.pack(side="left")   
        eT2=Entry(frT2,textvariable=self.inpAttT2,width=8)
        eT2.bind('<Return>',self.eInpAttT2Callback)
        eT2.pack(side="left")
        frT2.pack()
        eT2.pack(fill=X,anchor=E,padx=5)
        
        
        
        pw2.add(frInputAtt)
        
        
    def plot(self):
        
        self.setAxesLabels()        
        t = np.arange(0,400,1)
        s1 = 20*np.log(np.abs(np.random.randn(np.size(t))))
        self.ax1.cla()
        self.ax1.plot(t, s1, 'y')
        self.ax1.set_xlabel(self.xLbl,fontsize='medium')
        # Make the y-axis label and tick labels match the line color.
        self.ax1.set_ylabel(self.yLbl[0], color='y',fontsize='medium')
        
        for tl in self.ax1.get_yticklabels():
            tl.set_color('y')
        s2 = np.sin(2*np.pi*t/400)+0.1*np.random.randn(np.size(t))
        
        self.ax2.cla()
        self.ax2.plot(t, s2, 'c')
        self.ax2.set_ylabel(self.yLbl[1], color='c',fontsize='medium')
        for tl in self.ax2.get_yticklabels():
            tl.set_color('c')
        
        self.canvas.draw()
        
        
    def setAxesLabels(self):
        XLABELS = ('Frequency [Hz]',
            'DC Bias [V]',
            'Osc Lvl [V]',
            'Osc Lvl [dBm]',
            r'Osc Lvl [dB$\mu$V]')
        self.xLbl = XLABELS[self.sweepParameter.get()-1] #Radiobutton counts from 1, Python counts from 0
        angleStr = ('[deg]','[rad]')[self.angleMode.get()-1]
        if self.measFuncVar.get() == 1:
            YLABELS= [('Gain [dB]','Phase '+angleStr),
            ('Gain','Phase '+angleStr),
            ('Re {Gain}','Im {Gain}'),
            ('Gain [dB]','Group Delay')]
            self.yLbl = YLABELS[self.formatNetwork.get()-1]
            self.ax2.patch.set_visible(False)
            self.canvas.show()
            
## Old Version of CalibrationtabNetwork   
#    def buildCalibrationtabNetwork(self):
#        frCalMode = Frame(self.calibrationtabNetwork)
#        frCalMode.pack()
#        CALMODES = [("Transmission",1),
#                    ("Reflection",2)]    
#        for text, mode in CALMODES:
#            self.rbCalMode = Radiobutton (frCalMode,text=text,variable = self.calMode,value = mode,command = self.calModeCallback)
#            self.rbCalMode.pack(side="left")
#        self.calMode.set(1)
#        
#        
#        imgTransCalibPath = "./Images/TransmissionCalibrationDiagram.gif"
#        imgReflCalibPath = "./Images/ReflectionCalibrationDiagram.gif"
#        self.imgTransCalib = PhotoImage(file=imgTransCalibPath)
#        self.imgReflCalib = PhotoImage(file=imgReflCalibPath)
#        self.imgCalibLbl = Label(self.calibrationtabNetwork,image=self.imgTransCalib)
#        self.imgCalibLbl.pack()
#        
#        frCalCbtn = Frame(self.calibrationtabNetwork)
#        frCalCbtn.pack()
#        self.cbtnIsncalNetwork=Checkbutton(frCalCbtn,variable=self.checkIsncalNetwork,text="Perform Isolation Calibration")
#        self.checkIsncalNetwork.set(True)        
#        self.cbtnIsncalNetwork.pack(side="left")
#        
#        self.cbtnShortNetwork=Checkbutton(frCalCbtn,variable=self.checkShortNetwork,text="Perform Short Calibration")
#        self.checkShortNetwork.set(True)        
#        # don't pack yet
#        
#        
#        self.msgCalibrationtabNetwork = Message(self.calibrationtabNetwork,width=self.imgTransCalib.width())
#        self.msgCalibrationtabNetwork.config(text="Connect a power splitter, and a network as appropriate -- the MEASURE position shown above.")
#        self.msgCalibrationtabNetwork.pack()
#        
#        self.btnNextCalibration = Button(self.calibrationtabNetwork,text='Start Calibration',command=self.nextButtonCallback)
#        self.btnNextCalibration.pack()        
#        
#        self.calibStepCounter = 0
#        
    
    def buildCalibrationtabNetwork(self):
        frCalMode = Frame(self.calibrationtabNetwork)
        frCalMode.pack()
        CALMODES = [("Transmission",1),
                    ("Reflection",2)]    
        for text, mode in CALMODES:
            self.rbCalMode = Radiobutton (frCalMode,text=text,variable = self.calMode,value = mode,command = self.calModeCallback)
            self.rbCalMode.pack(side="left")
        self.calMode.set(1)
        
        
        imgTransCalibPath = "./Images/TransmissionCalibrationDiagram.gif"
        imgReflCalibPath = "./Images/ReflectionCalibrationDiagram.gif"
        self.imgTransCalib = PhotoImage(file=imgTransCalibPath)
        self.imgReflCalib = PhotoImage(file=imgReflCalibPath)
        self.imgCalibLbl = Label(self.calibrationtabNetwork,image=self.imgTransCalib)
        self.imgCalibLbl.pack()
        
        msg = Message(self.calibrationtabNetwork,text="Select stimulus and receiver settings before starting the calibration.",width=self.imgTransCalib.width())
        msg.pack()
        
        self.frTransBtns = Labelframe(self.calibrationtabNetwork, text="Calibration Setup")
        self.frTransBtns.pack()
        self.btnIso  = Button(self.frTransBtns,text="Isolation Calibration")
        self.btnIso.pack(side="left", padx=5, pady=5)
        self.btnThr  = Button(self.frTransBtns,text="Through Calibration")
        self.btnThr.pack(side="left",padx=5, pady=5)
        self.btnCor  = Checkbutton(self.frTransBtns,text="Correction", variable = self.correctn)
        self.correctn.set(True)
        self.btnCor.pack(side="left",padx=5, pady=5)
        
        self.btnCalibSettings = Button(self.frTransBtns,text="Settings",command=self.calibSettingsCallback)
        self.btnCalibSettings.pack(side="left",padx=5, pady=5)        
        
    def calibSettingsCallback(self):
        ySpacing = 2
        
        top = Toplevel(self.root)
        top.title("Calibration Settings")
        pw = PanedWindow(top, orient=VERTICAL)
        pw.pack(fill=BOTH,expand=1)
        
        lfCharImp = Labelframe(pw,text="Characteristic Impedance")
        lfCharImp.pack(fill=BOTH)
        Z0 = [('50 Ohm',1),('75 Ohm',2)]
        for text, mode in Z0:
            rbZ0 = Radiobutton(lfCharImp,text=text, value=mode,variable=self.charImp)
            rbZ0.pack(side="left")
        self.charImp.set(1)
        
        pw.add(lfCharImp)
        
        lfOpenStd = Labelframe(pw,text="Open Standard")
        lfOpenStd.pack(fill=BOTH)
        
        frOpenCond=Frame(lfOpenStd)
        frOpenCond.pack(side="left")
        lblOpenCond=Label(frOpenCond, text="Conductance [S]:", height=ySpacing)
        lblOpenCond.pack(side="left")   
        eOpenCond=Entry(frOpenCond,textvariable=self.openCond,width=8)
        eOpenCond.bind('<Return>',self.eOpenCondCallback)
        eOpenCond.pack(side="left") 
        eOpenCond.pack(fill=X,anchor=E,padx=5) 
        
        frOpenCap=Frame(lfOpenStd)
        frOpenCap.pack(side="left")
        lblOpenCap=Label(frOpenCap, text="Capacitance [F]:", height=ySpacing)
        lblOpenCap.pack(side="left")   
        eOpenCap=Entry(frOpenCap,textvariable=self.openCap,width=8)
        eOpenCap.bind('<Return>',self.eOpenCapCallback)
        eOpenCap.pack(side="left") 
        eOpenCap.pack(fill=X,anchor=E,padx=5) 
        
        pw.add(lfOpenStd)        
        
        lfLdStd = Labelframe(pw,text="Load Standard")
        lfLdStd.pack(fill=BOTH)
        
        frLdRes=Frame(lfLdStd)
        frLdRes.pack(side="left")
        lblLdRes=Label(frLdRes, text="Resistance [Ohm]:", height=ySpacing)
        lblLdRes.pack(side="left")   
        eLdRes=Entry(frLdRes,textvariable=self.ldRes,width=8)
        eLdRes.bind('<Return>',self.eLdResCallback)
        eLdRes.pack(side="left") 
        eLdRes.pack(fill=X,anchor=E,padx=5) 
        
        frLdInd=Frame(lfLdStd)
        frLdInd.pack(side="left")
        lblLdInd=Label(frLdInd, text="Inductance [H]:", height=ySpacing)
        lblLdInd.pack(side="left")   
        eLdInd=Entry(frLdInd,textvariable=self.ldInd,width=8)
        eLdInd.bind('<Return>',self.eLdIndCallback)
        eLdInd.pack(side="left") 
        eLdInd.pack(fill=X,anchor=E,padx=5) 
        
        pw.add(lfLdStd)      
        
        lfShtStd = Labelframe(pw,text="Short Standard")
        lfShtStd.pack(fill=BOTH)
        
        frShtRes=Frame(lfShtStd)
        frShtRes.pack(side="left")
        lblShtRes=Label(frShtRes, text="Resistance [Ohm]:", height=ySpacing)
        lblShtRes.pack(side="left")   
        eShtRes=Entry(frShtRes,textvariable=self.shtRes,width=8)
        eShtRes.bind('<Return>',self.eShtResCallback)
        eShtRes.pack(side="left") 
        eShtRes.pack(fill=X,anchor=E,padx=5) 
        
        frShtInd=Frame(lfShtStd)
        frShtInd.pack(side="left")
        lblShtInd=Label(frShtInd, text="Inductance [H]:", height=ySpacing)
        lblShtInd.pack(side="left")   
        eShtInd=Entry(frShtInd,textvariable=self.shtInd,width=8)
        eShtInd.bind('<Return>',self.eShtIndCallback)
        eShtInd.pack(side="left") 
        eShtInd.pack(fill=X,anchor=E,padx=5) 
        
        pw.add(lfShtStd) 
        
        btnOk = Button(top,text="Ok",command=top.destroy)
        btnOk.pack()
        
    def nextButtonCallback(self):
        self.calibStepCounter = self.calibStepCounter +1
        if self.calMode == 1:        
            if self.checkIsncalNetwork.get()==False and self.calibStepCounter == 1:
                self.calibStepCounter = self.calibStepCounter +1 #Skip ISNCAL
            if self.calibStepCounter == 1:
                 self.msgCalibrationtabNetwork.config(text="Terminate the source signal with an impedance matched load, and disconnect the network under test from the setup, leave the test channel open -- the ISOLATE position shown above.")
                 self.btnNextCalibration.config(text="Next")
            elif self.calibStepCounter == 2:
                self.msgCalibrationtabNetwork.config(text="Short circuit the test cables to make a through connection -- the THROUGH position shown above.")
                self.btnNextCalibration.config(text="Next")
            elif self.calibStepCounter == 3:
                self.msgCalibrationtabNetwork.config(text="Connect the network under test as appropriate for the selected measurement -- the MEASURE position shown above.")
                self.btnNextCalibration.config(text="Next")
            elif self.calibStepCounter == 4:
                self.msgCalibrationtabNetwork.config(text="Connect a power splitter, and a network as appropriate -- the MEASURE position shown above.")
                self.btnNextCalibration.config(text="Start Calibration")            
                self.calibStepCounter = 0
        else:
            if self.calibStepCounter == 1:
                self.msgCalibrationtabNetwork.config(text="Select the 4195A's stimulus and receiver settings as appropriate for the measurement.")
                self.btnNextCalibration.config(text="Next")   
            elif self.calibStepCounter ==2:
                top = Toplevel(self.root)
                top.title("Select Z0")
                
                msg = Message(top,text="Select the Characteristic Impedance", width=150) 
                msg.pack()
                
                Z0 = [('50 Ohm',1),('75 Ohm',2)]
                for text, mode in Z0:
                    rbZ0 = Radiobutton(top,text=text, value=mode,variable=self.charImp)
                    rbZ0.pack(anchor=W)
                self.charImp.set(1)
                
                btnOk = Button(top,text="Ok",command=top.destroy)
                btnOk.pack()
                
    

    def calModeCallback(self):
        if self.calMode.get() == 1:
            self.imgCalibLbl.config(image=self.imgTransCalib)
            self.cbtnShortNetwork.pack_forget()
            self.calibStepCounter = 0
            self.btnNextCalibration.config(text="Start Calibration") 
            self.msgCalibrationtabNetwork.config(text="Connect a power splitter, and a network as appropriate -- the MEASURE position shown above.")
        else:
            self.imgCalibLbl.config(image=self.imgReflCalib)
            self.cbtnShortNetwork.pack(side="left")
            self.calibStepCounter = 0
            self.btnNextCalibration.config(text="Start Calibration")  
            self.msgCalibrationtabNetwork.config(text="Connect a directional bridge, a power splitter, and the network under test as appropriate for the selected measurement -- the DUT position shown above.")
        


    def eStartCallback(self,event):
        print 'Start = '+self.startFreqStr.get()
    def eStopCallback(self,event):
        print 'Stop = '+self.stopFreqStr.get()
    def eCenterCallback(self,event):
        print 'Center = '+self.centerFreqStr.get()
    def eSpanCallback(self,event):
        print 'Span = '+self.spanStr.get()
    def eNopCallback(self,event):
        print 'NOP = '+self.nopStr.get()
    def eStepCallback(self,event):
        print 'Step = '+self.stepStr.get()
    def eSwpTimeCallback(self,event):
        print 'Sweep Time = '+self.swpTimeStr.get()
    def eSpotCallback(self,event):
        print 'Spot Frequency = '+self.spotFreqStr.get()
    def eOsc1Callback(self,event):
        print 'Osc1 Level = '+self.osc1LvlStr.get()
    def eOsc2Callback(self,event):
        print 'Osc2 Level = '+self.osc2LvlStr.get()
        
    def eInpAttR1Callback(self,event):
        print 'R1 Input Attenuation = '+self.inpAttR1.get()
    def eInpAttR2Callback(self,event):
        print 'R2 Input Attenuation = '+self.inpAttR2.get()
    def eInpAttT1Callback(self,event):
        print 'T1 Input Attenuation = '+self.inpAttT1.get()
    def eInpAttT2Callback(self,event):
        print 'T2 Input Attenuation = '+self.inpAttT2.get()
        
    def ePortExtR1Callback(self,event):
        print 'R1 Port Extension = '+self.portExtR1.get()
    def ePortExtR2Callback(self,event):
        print 'R2 Port Extension = '+self.portExtR2.get()
    def ePortExtT1Callback(self,event):
        print 'T1 Port Extension = '+self.portExtT1.get()
    def ePortExtT2Callback(self,event):
        print 'T2 Port Extension = '+self.portExtT2.get()
    def ePortExtP1Callback(self,event):
        print 'P1 Port Extension = '+self.portExtP1.get()
    def ePortExtP2Callback(self,event):
        print 'P2 Port Extension = '+self.portExtP2.get()
        
        
    def eOpenCondCallback(self,event):
        print 'OpenCond = '+self.openCond.get()
    def eOpenCapCallback(self,event):
        print 'OpenCap = '+self.openCap.get()
    def eLdResCallback(self,event):
        print 'LdRes = '+self.ldRes.get()
    def eLdIndCallback(self,event):
        print 'LdInd = '+self.ldInd.get()
    def eShtResCallback(self,event):
        print 'ShtRes = '+self.shtRes.get()
    def eShtIndCallback(self,event):
        print 'ShtInd = '+self.shtInd.get()
        
            
    def printPortNetwork(self):
        print self.portNetwork.get()
        
            
        
    def measFuncCall(self):
            print'FNC'+str(self.measFuncVar.get())
            self.setActiveTabs()
            
    def hello(self):
        print "hello"
    
    def show(self):
        self.root.mainloop()
      

###############################################################################

mw = MainWindow()

        

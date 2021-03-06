# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 17:15:22 2015

@author: Jochen
"""

from Tkinter import *
from ttk import Notebook, Labelframe, Combobox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
import tkFileDialog
import HP4195A_COM


class MainWindow():
    analyzer = ()
    
    # Analyzer Data Registers
    regA = None
    regB = None
    regX = None
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def __init__(self):       
        self.root     = Tk()
        self.analyzer = HP4195A_COM.HP4195A()   
        self.root.wm_title("HP4195A User Interface")
        self.root.iconbitmap(r'c:\Users\Jochen\HP4195A\Images\icon.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.destructor)
        self.init()
    def destructor(self):
        self.root.destroy()
        self.analyzer.Disconnect()
    def init(self):     
        self.plotInterval = 10        
        self.measFuncVar =IntVar()
        self.angleMode =IntVar()
        self.portNetwork = IntVar()
        self.portSpectrum = IntVar()
        self.formatNetwork = IntVar()
        self.unitSpectrum = StringVar()
        self.formatImpedance = StringVar()   
        self.formatS1122 = IntVar()
        self.formatS2112 = IntVar()
        self.dfreq = DoubleVar()
        self.trackGenOut = IntVar()
        # Stimulus Variables
        self.sweepParameter= IntVar()
        self.startFreqStr  = StringVar()
        self.stopFreqStr   = StringVar()
        self.centerFreqStr = StringVar()
        self.spanStr       = StringVar()
        self.sweepType     = IntVar()
        self.nopStr        = StringVar()
        self.stepStr       = StringVar()
        self.swpTimeStr    = StringVar()
        self.stepStr       = StringVar()
        self.spotFreqStr   = StringVar()
        self.osc1LvlStr    = StringVar()
        self.osc2LvlStr    = StringVar()
        self.triggerMode   = IntVar()
        self.iFMode        = IntVar()
        self.inpAttR1      = StringVar()
        self.inpAttR2      = StringVar()
        self.inpAttT1      = StringVar()
        self.inpAttT2      = StringVar()
        self.portExtR1     = StringVar()
        self.portExtR2     = StringVar()
        self.portExtT1     = StringVar()
        self.portExtT2     = StringVar()
        self.portExtP1     = StringVar()
        self.portExtP2     = StringVar()
        self.calMode       = IntVar()
        self.resBW         = StringVar()
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
        ###### plot #########
        self.xLbl = ''
        self.yLbl = '' #will contain up to 2 Strings depending on measFuncVar
        self.menubar=None
        self.note=None
        self.maintab=None
        self.stimulustab=None
        self.receivertab=None
        self.calibrationtab=None
        self.buildMenuBar()
        self.buildTabBar()  
        self.buildSettingsTabNetwork()
        self.buildSettingsTabSpectrum()
        self.buildSettingsTabImpedance()
        self.buildSettingsTabS1122()
        self.buildSettingsTabS2112()
        self.buildStimulustab()
        self.buildMaintab()
        self.buildCalibrationtab()
        self.buildReceivertab()
        self.show()
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       
    """
    Create Menu Bar
    
    Callbacks:
        - measurementFunctionSwitch
        - saveData
    """
    def buildMenuBar(self):
        menubar = Menu(self.root)
        # File-Menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label = "Save" , command = self.saveData)
        filemenu.add_command(label = "Connect" , command = self.connect)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit" , command = self.destructor)
        menubar.add_cascade(label  = "File" , menu = filemenu)
        ##### Measurement Function Menu #####
        measfuncmenu = Menu(menubar, tearoff = 0)
        for text, mode in self.getSortedList(self.analyzer.MeasurementModes, 'items'):
            measfuncmenu.add_radiobutton(label = text, variable = self.measFuncVar, value = mode, command = partial(self.measurementFunctionSwitch, text))    
        self.measFuncVar.set(1)
        menubar.add_cascade(label = "Measurement Function", menu = measfuncmenu)
        self.root.config(menu=menubar)
    """
    Callback functions
    """
    def measurementFunctionSwitch(self, measFunc):
        print self.analyzer.setMeasurementMode(measFunc)
        self.setActiveTabs()
        self.setCalibrationTab()
        self.setReceiverTab()
    def saveData(self):
        if self.measFuncVar.get()==2:
            data = np.vstack((self.regX, self.regA)).T
            info = (self.xLbl, self.yLbl[0])
        else:
            data = np.vstack((self.regX, self.regA, self.regB)).T
            info = (self.xLbl, self.yLbl[0], self.yLbl[1])
        
        outfile = tkFileDialog.asksaveasfile(mode='w', defaultextension=".nif")
        r,c = data.shape
        outfile.write(str(r)+", "+str(c)+"\n")
        outfile.write("{:18.17e}".format(np.max(data))+", "+"{:18.17e}".format(np.min(data))+"\n")
        outfile.write("\nASCII \n")
        outfile.write("\n0\n")
        for x in xrange(c):
            outfile.write(info[x]+"\n")
            for y in xrange(r):
                outfile.write("{:18.17e}".format(data[y,x])+"\n")
        outfile.close
        
        
    def connect(self):
        self.analyzer.Connect()
        print self.analyzer.status_Connected
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Create Tab Bars
    """
    def buildTabBar(self):    
        self.note = Notebook(self.root) 
        self.note.pack(fill=BOTH,expand=1)
        self.maintab              = Frame(self.note)
        self.stimulustab          = Frame(self.note)
        self.receivertab          = Frame(self.note)
        self.calibrationtab       = Frame(self.note)
        self.settingstabNetwork   = Frame(self.note)
        self.settingstabSpectrum  = Frame(self.note)
        self.settingstabImpedance = Frame(self.note)
        self.settingstabS1122     = Frame(self.note)
        self.settingstabS2112     = Frame(self.note)
        self.note.add(self.maintab, text              = "Main", compound=TOP)
        self.note.add(self.stimulustab, text          = "Stimulus")
        self.note.add(self.receivertab, text          = "Receiver")
        self.note.add(self.calibrationtab, text       = "Calibration")
        self.note.add(self.settingstabNetwork, text   = "Settings")
        self.note.add(self.settingstabSpectrum, text  = "Settings")
        self.note.add(self.settingstabImpedance, text = "Settings")
        self.note.add(self.settingstabS1122, text     = "Settings")
        self.note.add(self.settingstabS2112, text     = "Settings")
        self.setActiveTabs()
    """
    Set Active Tabs
    
    """
    def setActiveTabs(self):
        self.note.tab(self.maintab,state = "normal") 
        self.note.tab(self.stimulustab,state = "normal") 
        self.note.tab(self.receivertab,state = "normal")
        # set "normal" tabs before "hidden" tabs to avoid glitches
        if self.measFuncVar.get()==1: #Network
            self.note.tab(self.calibrationtab,state = "normal")
            self.note.tab(self.settingstabNetwork, state = "normal")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==2: #Spectrum
            self.note.tab(self.settingstabSpectrum, state = "normal")
            self.note.tab(self.calibrationtab,state = "hidden")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==3: #Impedance
            self.note.tab(self.calibrationtab,state = "normal")
            self.note.tab(self.settingstabImpedance, state = "normal")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==4 or self.measFuncVar.get()==7: #S11 or S21
            self.note.tab(self.calibrationtab,state = "normal")
            self.note.tab(self.settingstabS1122, state = "normal")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS2112,state = "hidden")
        elif self.measFuncVar.get()==5 or self.measFuncVar.get()==6: #S21 or S12
            self.note.tab(self.calibrationtab,state = "normal")
            self.note.tab(self.settingstabS2112,state = "normal")
            self.note.tab(self.settingstabNetwork, state = "hidden")
            self.note.tab(self.settingstabSpectrum, state = "hidden")
            self.note.tab(self.settingstabImpedance, state = "hidden")
            self.note.tab(self.settingstabS1122, state = "hidden")
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            
    """
    Settings-Tabs Constructors for each mode:
        *Network
        *Spectrum
        *Impedance
        *S1122
        *S2112
    """
    
    """
    Network Mode
    """
    def buildSettingsTabNetwork(self):
        pwFull = PanedWindow(self.settingstabNetwork,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        pw1 = PanedWindow(pwFull,orient=HORIZONTAL)
        pw1.pack(fill=BOTH,expand=1)
        ##### Port Radiobuttons #####
        pw1.add(self.radioFrame(pw1, self.getSortedList(self.analyzer.NetworkModePorts, 'items'), "Port", self.portNetwork, 'top', self.setPort)) 
        self.portNetwork.get()
        ##### Format Radiobuttons ##### 
        pw1.add(self.radioFrame(pw1, self.getSortedList(self.analyzer.NetworkModeFormats, 'items'), "Format", self.formatNetwork, 'top', self.setFormat))
        pw2 = PanedWindow(pwFull,orient=VERTICAL)
        pw2.pack()       
        ##### Angle Mode Radiobuttons #####
        pw2.add(self.radioFrame(pw2, self.getSortedList(self.analyzer.AngleMode, 'items'), "Angle Mode", self.angleMode, 'top', self.setAngle))
        # Add Delay Aperture Slider
        pw2.add(self.buildDelApSlider(pw2))
        pw1.add(pw2)
        pwFull.add(pw1)
        # Add Port Extension Frame
        pwFull.add(self.buildPortExt(pwFull))
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    Spectrum Mode
    """
    def buildSettingsTabSpectrum(self):
        pwFull = PanedWindow(self.settingstabSpectrum,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        pw1 = PanedWindow(pwFull,orient=HORIZONTAL)
        pw1.pack(fill=BOTH,expand=1)
        ##### Port Radiobuttons #####
        pw1.add(self.radioFrame(pw1, self.getSortedList(self.analyzer.SpectrumModePorts, 'items'), "Port", self.portSpectrum, 'top', self.setPort))
        pw11 = PanedWindow(pw1,orient=VERTICAL)
        pw11.pack(fill=BOTH,expand=1)
        ##### Format Combobox #####
        lfUnits = Labelframe(pw11, text = "Unit")
        lfUnits.pack(fill = BOTH,expand=1)
        self.cbUnitSpec = Combobox(lfUnits,values = self.getSortedList(self.analyzer.SpectrumModeFormatsTeX, 'keys'), textvariable = self.unitSpectrum)
        self.cbUnitSpec.pack(anchor=CENTER, padx=10, pady=10)
        self.cbUnitSpec.set(self.getSortedList(self.analyzer.SpectrumModeFormatsTeX, 'keys')[0])
        self.cbUnitSpec.bind("<<ComboboxSelected>>", self.setSpectrumFormat)       
        pw11.add(lfUnits)
        pw1.add(pw11)
        ##### Tracking Generator Output Radiobuttons #####
        pw11.add(self.radioFrame(pw11, self.getSortedList(self.analyzer.SpectrumModeTrackingGenOut, 'items'), "Tracking Generator Output", self.trackGenOut, 'top', self.setTrackingGeneratorOutput)) # Default = 0
        pw1.add(pw11)
        pw2 = PanedWindow(pwFull,orient=VERTICAL)
        pw2.pack()
        ##### Angle Mode Radiobuttons #####
        pw2.add(self.radioFrame(pw2, self.getSortedList(self.analyzer.AngleMode, 'items'), "Angle Mode", self.angleMode, 'top', self.setAngle))
        # Add Delay Aperture Slider
        pw2.add(self.buildDelApSlider(pw2))
        pw1.add(pw2)
        pwFull.add(pw1)
        # Add Port Extension Frame
        pwFull.add(self.buildPortExt(pwFull))
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    Impedance Mode
    """
    def buildSettingsTabImpedance(self):
        pwFull = PanedWindow(self.settingstabImpedance, orient=VERTICAL)
        pw1    = PanedWindow(pwFull, orient=HORIZONTAL)
        pwFull.pack(fill=BOTH,expand=1)
        pw1.pack(fill=BOTH,expand=1)
        ##### Port Radiobuttons #####
        pw1.add(self.radioFrame(pw1,self.getSortedList(self.analyzer.ImpedanceModePorts, 'items'), "Port", self.portNetwork, 'top', self.setPort))
        ##### Format Combobox #####             
        lfFmt = Labelframe(pw1,text = "Format")
        lfFmt.pack(fill = BOTH, expand = 1)
        self.cbFormatImp = Combobox(lfFmt, values = self.getSortedList(self.analyzer.ImpedanceModeFormats, 'keys'), textvariable = self.formatImpedance)
        self.cbFormatImp.pack(anchor=CENTER,padx=10,pady=10)
        self.cbFormatImp.set(self.getSortedList(self.analyzer.ImpedanceModeFormats, 'keys')[0])
        self.cbFormatImp.bind("<<ComboboxSelected>>", self.setImpedanceFormat)       
        pw1.add(lfFmt)
        pw2 = PanedWindow(pwFull,orient=VERTICAL)
        pw2.pack()
        ##### Angle Mode Radiobuttons #####
        pw2.add(self.radioFrame(pw2, self.getSortedList(self.analyzer.AngleMode, 'items'), "Angle Mode", self.angleMode, 'top', self.setAngle))
        # Add Delay Aperture Slider
        pw2.add(self.buildDelApSlider(pw2))
        pw1.add(pw2)
        pwFull.add(pw1)
        # Add Port Extension Frame
        pwFull.add(self.buildPortExt(pwFull))        
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    S11_22 Mode
    """
    def buildSettingsTabS1122(self):
        pwFull = PanedWindow(self.settingstabS1122,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        pw1 = PanedWindow(pwFull,orient=HORIZONTAL)
        pw1.pack(fill=BOTH,expand=1)
        ##### Format Radiobuttons #####
        pw1.add(self.radioFrame(pw1, self.getSortedList(self.analyzer.SModeFormats, 'items'), "Format", self.formatS1122, 'top', self.setFormat))
        pw2 = PanedWindow(pwFull,orient=VERTICAL)
        pw2.pack()
        ##### Angle Mode Radiobuttons #####
        pw2.add(self.radioFrame(pw2, self.getSortedList(self.analyzer.AngleMode, 'items'), "Angle Mode", self.angleMode, 'top', self.setAngle))
        # Add Delay Aperture Slider
        pw2.add(self.buildDelApSlider(pw2))
        pw1.add(pw2)
        pwFull.add(pw1)
        # Add Port Extension Frame
        pwFull.add(self.buildPortExt(pwFull))
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    S21_12 Mode Builder
    """
    def buildSettingsTabS2112(self):
        pwFull = PanedWindow(self.settingstabS2112,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        pw1 = PanedWindow(pwFull,orient=HORIZONTAL)
        pw1.pack(fill=BOTH,expand=1)
        ##### Format Radiobuttons #####
        FMTS = self.getSortedList(self.analyzer.SModeFormats, 'items')
        pw1.add(self.radioFrame(pw1, FMTS,"Format",self.formatS2112,'top', self.setFormat))
        pw2 = PanedWindow(pwFull,orient=VERTICAL)
        pw2.pack()
        ##### Angle Mode Radiobuttons #####
        pw2.add(self.radioFrame(pw2, self.getSortedList(self.analyzer.AngleMode, 'items'), "Angle Mode", self.angleMode, 'top', self.setAngle))
        # Add Delay Aperture Slider
        pw2.add(self.buildDelApSlider(pw2))
        pw1.add(pw2)
        pwFull.add(pw1)
        # Add Port Extension Frame
        pwFull.add(self.buildPortExt(pwFull))
        
    """
    Settings Tab - Callback functions Definition
    """
    def setPort(self, portName):
        print self.analyzer.setPort(portName)
    def setFormat(self, formatName):
        print self.analyzer.setFormat(formatName)
    def setAngle(self, angle):
        print self.analyzer.setAngleMode(angle)
    def setTrackingGeneratorOutput(self, out):
        print self.analyzer.setTrackingGeneratorOutput(out)
    def setSpectrumFormat(self, event):
        print self.analyzer.setFormat(self.unitSpectrum.get())
    def setImpedanceFormat(self, event):
        print self.analyzer.setPort(self.formatImpedance.get())
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""        
    
    """
    Aperture Slider
        Callbacks:
            - dfreqCallback
    """
    def buildDelApSlider(self,parent):
        ##### Delay Aperture Slider #####
        lfDf     = Labelframe(parent, text = "Delay Aperture")
        self.sDf = Scale(master=lfDf,from_=0.5, to=100, resolution=0.5,variable=self.dfreq, orient=HORIZONTAL,sliderlength=15)
        self.sDf.bind("<ButtonRelease-1>", self.dfreqCallback)        
        self.sDf.pack(fill=BOTH,padx=5)        
        self.dfreq.set(0.5)   
        return lfDf
    def dfreqCallback(self,event):
        print self.analyzer.setDelayApperture(self.dfreq.get())
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Port Extension Builder
        Callbacks:
            - ePortExtR1Callback
            - ePortExtR2Callback
            - ePortExtT1Callback
            - ePortExtT2Callback
            - ePortExtP1Callback
            - ePortExtP2Callback
    """
    def buildPortExt(self,parent):
        ##### Port Extension Entry Fields #####
        frPortExt = Labelframe(parent,text = "Port Extension [cm]")
        frPortExt.pack(fill=BOTH,expand=1)
        frPortExtR = Frame(frPortExt)  
        frPortExtT = Frame(frPortExt)  
        frPortExtP = Frame(frPortExt)
        frPortExtR.pack(side="left",fill=BOTH,expand=1)
        frPortExtT.pack(side="left",fill=BOTH,expand=1)
        frPortExtP.pack(side="left",fill=BOTH,expand=1)
        ##### R Ports #####
        portExtRPacklist = {'R1:' : (self.portExtR1, self.ePortExtR1Callback),
                            'R2:' : (self.portExtR2, self.ePortExtR2Callback)}
        self.labelEntryV(frPortExtR, portExtRPacklist)  
        ##### T Ports #####
        portExtTPacklist = {'T1:' : (self.portExtT1, self.ePortExtT1Callback),
                            'T2:' : (self.portExtT2, self.ePortExtT2Callback)}
        self.labelEntryV(frPortExtT, portExtTPacklist)  
        ##### P Ports #####
        portExtPPacklist = {'P1:' : (self.portExtP1, self.ePortExtP1Callback),
                            'P2:' : (self.portExtP2, self.ePortExtP2Callback)}
        self.labelEntryV(frPortExtP, portExtPPacklist)
        return frPortExt
    def ePortExtR1Callback(self,event):
        print self.analyzer.setExtensionLength('R1', self.portExtR1.get())
    def ePortExtR2Callback(self,event):
        print self.analyzer.setExtensionLength('R2', self.portExtR2.get())
    def ePortExtT1Callback(self,event):
        print self.analyzer.setExtensionLength('T1', self.portExtT1.get())
    def ePortExtT2Callback(self,event):
        print self.analyzer.setExtensionLength('T2', self.portExtT2.get())
    def ePortExtP1Callback(self,event):
        print self.analyzer.setExtensionLength('P1', self.portExtP1.get())
    def ePortExtP2Callback(self,event):
        print self.analyzer.setExtensionLength('P2', self.portExtP2.get())
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""  
    
    """
    Stimulus Tab Constructor
    
    - buildStimulustab
    - Callbacks:
        setSweepParameter
        setSweepType
        setTriggerMode
        eStartCallback
        eStopCallback
        eCenterCallback
        eSpanCallback
        eNopCallback
        eStepCallback
        eSwpTimeCallback
        eSpotCallback
        eOsc1Callback
        eOsc2Callback
    """

    """
    Build Stimulus Tab
    """
    def buildStimulustab(self):
        pwFull = PanedWindow(self.stimulustab,orient=VERTICAL)
        pwFull.pack(fill=BOTH,expand=1)
        pwTop = PanedWindow(pwFull,orient=HORIZONTAL)
        pwLeft = PanedWindow(pwTop,orient=VERTICAL)
        pwLeft.pack(fill=BOTH)
        ##### Sweep Parameter Radiobutton #####    
        pwLeft.add(self.radioFrame(pwLeft, self.getSortedList(self.analyzer.SweepParameters, 'items'), "Sweep Parameter", self.sweepParameter, 'top', self.setSweepParameter))
        ##### Sweep Type Radiobuttion #####
        pwLeft.add(self.radioFrame(pwLeft, self.getSortedList(self.analyzer.SweepModes, 'items'), "Sweep Type", self.sweepType, 'top', self.setSweepType))
        pwTop.add(pwLeft)
        ##### Sweep Range Entry Fields #####
        frSwpRange = Labelframe(pwTop,text="Sweep Range", width=100,height=100)
        frSwpRange.pack(fill=BOTH)
        swpRangePacklist = {'Start:'  : (self.startFreqStr  , self.eStartCallback),
                            'Stop:'   : (self.stopFreqStr   , self.eStopCallback),
                            'Center:' : (self.centerFreqStr , self.eCenterCallback),
                            'Span:'   : (self.spanStr       , self.eSpanCallback)}
        self.labelEntryV(frSwpRange, swpRangePacklist)    
        pwTop.add(frSwpRange)
        pwRight = PanedWindow(pwTop,orient=VERTICAL)
        pwRight.pack(fill=BOTH)
        ##### Trigger Mode Radio Button #####
        pwRight.add(self.radioFrame(pwRight, self.getSortedList(self.analyzer.TriggerModes, 'items'), "Trigger Mode", self.triggerMode, 'top', self.setTriggerMode))
        ##### Resolution Entry Fields #####
        frRes = Labelframe(pwRight, text="Resolution")
        frRes.pack(fill=BOTH)
        resolutionPacklist = {    '# Points:' : (self.nopStr     , self.eNopCallback),
                                  'Step:'     : (self.stepStr    , self.eStepCallback),
                                  'Swp Time:' : (self.swpTimeStr , self.eSwpTimeCallback)}        
        self.labelEntryV(frRes, resolutionPacklist)            
        pwRight.add(frRes)
        pwTop.add(pwRight)
        pwFull.add(pwTop)
        ##### Non-Sweep Parameter Entry Fields #####
        frNonSwp = Labelframe(pwFull,text="Non-Sweep Parameters")
        frNonSwp.pack(fill=BOTH,expand=1)
        nonSweepPacklist = {      'Spot Freq:' : (self.spotFreqStr,self.eSpotCallback),
                                  'Osc1 Lvl:'  : (self.osc1LvlStr,self.eOsc1Callback),
                                  'Osc2 Lvl:'  : (self.osc2LvlStr,self.eOsc2Callback)}        
        self.labelEntryH(frNonSwp, nonSweepPacklist)    
        pwFull.add(frNonSwp)
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
    """
    Build Stimulus Tab - Callback Functions Definition
    
    """
    def setSweepParameter(self, sweepParam):
        print self.analyzer.setSweepParameter(sweepParam)
    def setSweepType(self, sweepType):
        print self.analyzer.setSweepMode(sweepType)
    def setTriggerMode(self, triggerMode):
        print self.analyzer.setTriggerMode(triggerMode)
    def eStartCallback(self,event):
        print self.analyzer.setStartFreq(self.startFreqStr.get())
    def eStopCallback(self,event):
        print self.analyzer.setStopFreq(self.stopFreqStr.get())
    def eCenterCallback(self,event):
        print self.analyzer.setCenterFreq(self.centerFreqStr.get())
    def eSpanCallback(self,event):
        print self.analyzer.setSpan(self.spanStr.get())
    def eNopCallback(self,event):
        print self.analyzer.setNumberOfPoints(self.nopStr.get())
    def eStepCallback(self,event):
        print self.analyzer.setStep(self.stepStr.get())
    def eSwpTimeCallback(self,event):
        print self.analyzer.setSweepTime(self.swpTimeStr.get())
    def eSpotCallback(self,event):
        print self.analyzer.setStopFreq(self.spotFreqStr.get())
    def eOsc1Callback(self,event):
        print self.analyzer.setOsc1Amplitude(self.osc1LvlStr.get())
    def eOsc2Callback(self,event):
        print self.analyzer.setOsc2Amplitude(self.osc2LvlStr.get())
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
############################# Labeled Entry Fields ############################  
    # Vertical Alignment    
    def labelEntryV(self, parent, paramList):   
        rowIdx=0
        for name in paramList:
            att = paramList[name]       
            label      = Label(parent, text = name, height = 2)
            label.grid(sticky=W,padx=5)
            entry      = Entry(parent, textvariable = att[0] , width = 8)
            entry.bind('<Return>', att[1])
            entry.grid(row=rowIdx, column=1,padx=5)
            rowIdx=rowIdx+1
    # Horizontal Alignment
    def labelEntryH(self, parent, paramList):   
        for name in paramList:
            att = paramList[name]
            entryFrame = Frame(parent)
            entryFrame.pack(side = "left", padx = 5,fill=BOTH,expand=1)
            label      = Label(entryFrame, text = name, height = 2)
            label.pack(side = "left")   
            entry      = Entry(entryFrame, textvariable = att[0] , width = 8)
            entry.bind('<Return>', att[1])
            entry.pack(side = "left", fill = X, anchor = E, padx = 5)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    Main Tab Builder
        Callbacks:
            - startPlotting
    """
    def buildMaintab(self):
        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111)    
        self.ax2 = self.ax1.twinx()
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.maintab)
        self.canvas.get_tk_widget().pack()
        self.canvas._tkcanvas.config(highlightthickness=2, bd=0, relief=SUNKEN,highlightcolor='grey')
        self.canvas._tkcanvas.pack(anchor=NW,fill=BOTH,expand=1)
        'Periodic Plotting'
        self.plotThread = self.canvas.new_timer()
        self.plotThread.add_callback(self.plot)
        self.plotThread._set_interval(self.plotInterval)
        self.plotRun = False
        self.btnStartStop = Button(self.maintab,text="Run", command = self.startPlotting)
        self.btnStartStop.pack()
        self.ax1.set_axis_bgcolor('black')
        self.ax2.set_axis_bgcolor('none')
        self.fig.set_facecolor('black')
        self.ax2.spines['top'].set_color([.5, .5, .5])
        self.ax2.spines['bottom'].set_color([.5, .5, .5])
        self.ax2.spines['left'].set_color([.5, .5, .5])
        self.ax2.spines['right'].set_color([.5, .5, .5])
        self.ax1.xaxis.label.set_color([.8, .8, .8])
        self.ax1.tick_params(axis='x', colors=[.8, .8, .8])
        self.ax2.patch.set_visible(False)
        self.plot()
    
    """
    Main Tab - Callbacks
    
    """
    def startPlotting(self):
        if not self.plotRun:
            self.plotThread.start()
            self.btnStartStop.config(text="Stop")
        else:
            self.plotThread.stop()
            self.btnStartStop.config(text="Run")
        self.plotRun = not self.plotRun
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        
    """
    Receiver Tab Builder
        Update Method:
            - setReceiverTab
        Callbacks:
            - resBWCallback
            - eInpAttR1Callback
            - eInpAttR2Callback
            - eInpAttT1Callback
            - eInpAttT2Callback
            -
    """    
    def buildReceivertab(self):
        pw2 = PanedWindow(self.receivertab,orient=VERTICAL)
        pw2.pack(fill=BOTH,expand=1)
        self.pwRec1 = PanedWindow(pw2,orient = HORIZONTAL)
        self.pwRec1.pack(fill=BOTH, expand=1)
        frIF = Labelframe(self.pwRec1,text="IF Mode", width=100,height=100)
        frIF.pack(fill=BOTH,expand=1)
        ###### IF Mode Rest ######
        self.frIFRest = Frame(frIF)
        self.frIFRest.pack(pady=(0,35)) # Leave space for 3rd Radiobutton
        for text, mode in self.getSortedList(self.analyzer.GeneralIFModes, 'items'):
            self.rbIFRest = Radiobutton(self.frIFRest, variable = self.iFMode, text=text, value=mode, command = partial(self.setIFMode,text))         
            self.rbIFRest.pack(anchor=W)
        ###### IF Mode Spectrum ######
        self.frIFSpec = Frame(frIF)
        for text, mode in self.getSortedList(self.analyzer.SpectrumIFModes, 'items'):
            self.rbIFSpec = Radiobutton(self.frIFSpec, variable = self.iFMode, text=text, value=mode, command = partial(self.setIFMode,text))
            self.rbIFSpec.pack(anchor=W)
        self.pwRec1.add(frIF)
        self.iFMode.set(1)
        ##### Resolution Bandwidth Combobox #####
        lfResBW = Labelframe(self.pwRec1, text = "Resolution BW [Hz]", height=100, width=100)
        self.sbResBW = Combobox(lfResBW, values = self.analyzer.BW_Resolutions, textvariable = self.resBW)
        self.resBW.set('Auto')
        self.sbResBW.bind("<<ComboboxSelected>>", self.resBWCallback)
        self.sbResBW.pack(anchor=CENTER,padx=10,pady=10)
        lfResBW.pack(fill=BOTH,expand=1)
        self.pwRec1.add(lfResBW)
        pw2.add(self.pwRec1)
        ##### Input Attenuation Entry Fields #####
        frInputAtt = Labelframe(pw2, text = "Input Attenuation [dB]")
        frInputAtt.pack(fill=BOTH,expand=1)
        frInpAttR = Frame(frInputAtt)  
        frInpAttT = Frame(frInputAtt)  
        frInpAttR.pack(side="left",fill=BOTH,expand=1)
        frInpAttT.pack(side="left",fill=BOTH,expand=1)
        ##### R Ports #####
        inpAttRPacklist = {'R1:' : (self.inpAttR1,self.eInpAttR1Callback),
                           'R2:' : (self.inpAttR2,self.eInpAttR2Callback)}
        self.labelEntryV(frInpAttR, inpAttRPacklist)
        ##### T Ports #####
        inpAttTPacklist = {'T1:' : (self.inpAttT1,self.eInpAttT1Callback),
                           'T2:' : (self.inpAttT2,self.eInpAttT2Callback)}
        self.labelEntryV(frInpAttT, inpAttTPacklist)
        pw2.add(frInputAtt)
    """
    Update Receiver Tab
    """
    def setReceiverTab(self):
        if self.measFuncVar.get() == 2:
            if not self.frIFSpec.winfo_ismapped():
                self.frIFSpec.pack()
            self.frIFRest.pack_forget()
        else:
            if not self.frIFRest.winfo_ismapped():
                self.frIFRest.pack()
            self.frIFSpec.pack_forget()
    """
    Callbacks
    
    """
    def resBWCallback(self, event):
        print self.analyzer.setResolutionBandwidth(self.resBW.get())   
    def eInpAttR1Callback(self,event):
        print self.analyzer.setInputAttenuation("R1", self.inpAttR1.get())
    def eInpAttR2Callback(self,event):
        print self.analyzer.setInputAttenuation("R2", self.inpAttR2.get())
    def eInpAttT1Callback(self,event):
        print self.analyzer.setInputAttenuation("T1", self.inpAttT1.get())
    def eInpAttT2Callback(self,event):
        print self.analyzer.setInputAttenuation("T2", self.inpAttT2.get())
    def setIFMode(self, mode):
        print self.analyzer.setIFRange(mode)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    Calibration Tab Builder:
        Callbacks:
            - calibSettingsCallback
            - setCalibrationMode
            - setCharacteristicImpedance
            - eShtIndCallback
            - eShtResCallback
            - eLdIndCallback
            - eLdResCallback
            - eOpenCondCallback
            - eOpenCapCallback
            - getShort
            - getLoad
            - getOpen
            - getThrough
            - getIsolation
    """
    def buildCalibrationtab(self):
        # Load Images
        imgTransCalibPath = "./Images/TransmissionCalibrationDiagram.gif"
        imgReflCalibPath = "./Images/ReflectionCalibrationDiagram.gif"
        self.imgTransCalib = PhotoImage(file=imgTransCalibPath)
        self.imgReflCalib = PhotoImage(file=imgReflCalibPath)        
        superFrCalMode = Frame(self.calibrationtab)
        superFrCalMode.pack(fill=BOTH,expand=1)
        ######### Calibration Mode Radiobutton #############  
        self.frCalMode = self.radioFrame(superFrCalMode, self.getSortedList(self.analyzer.CalibrationModes, 'items'), "Calibration Mode", self.calMode, 'left', self.setCalibrationMode)
        self.frCalMode.pack(fill=BOTH,expand=1)
        frPwCalib = Frame(self.calibrationtab)
        frPwCalib.pack(fill=BOTH,expand=1)
        ######### Transmission Calibration #############
        self.pwTransCalib = PanedWindow(frPwCalib,orient=HORIZONTAL)
        self.pwTransCalib.pack()
        frLeft = Frame(self.pwTransCalib)
        frLeft.pack(fill=BOTH,expand=1)
        self.imgCalibLbl = Label(frLeft,image=self.imgTransCalib,relief = SUNKEN)
        self.imgCalibLbl.pack()
        self.pwTransCalib.add(frLeft)
        frRight = Labelframe(self.pwTransCalib, text = "Calibration Setup")
        frRight.pack(fill=BOTH,expand=1)
        self.btnIso  = Button(frRight, text = "Isolation",  command = self.getIsolation)
        self.btnIso.pack(side="top", padx=5, pady=5)
        self.btnThr  = Button(frRight, text = "Through",  command = self.getThrough)
        self.btnThr.pack(side="top",padx=5, pady=5)
        self.pwTransCalib.add(frRight)
        ######### Reflection Calibration ############
        self.pwReflCalib = PanedWindow(frPwCalib,orient=HORIZONTAL)
        ## Don't pack yet
        frLeft = Frame(self.pwReflCalib)
        frLeft.pack(fill=BOTH,expand=1)
        self.imgCalibLbl = Label(frLeft,image=self.imgReflCalib,relief = SUNKEN)
        self.imgCalibLbl.pack()
        self.pwReflCalib.add(frLeft)
        frRight = Labelframe(self.pwReflCalib, text="Calibration Setup")
        frRight.pack(fill=BOTH,expand=1)
        self.btnOpn  = Button(frRight, text = "Open",  command = self.getOpen)
        self.btnOpn.pack(side="top", padx=5, pady=5)
        self.btnLd  = Button(frRight, text = "Load",   command = self.getLoad)
        self.btnLd.pack(side="top",padx=5, pady=5)
        self.btnSht  = Button(frRight, text = "Short", command = self.getShort)
        self.btnSht.pack(side="top", padx=5, pady=5)
        self.pwReflCalib.add(frRight)
        #### Bottom of Calibrationtab ####
        msg = Message(self.calibrationtab,text="Select stimulus and receiver settings before starting the calibration.",width=self.imgTransCalib.width())
        msg.pack(side="left")
        self.btnCalibSettings = Button(self.calibrationtab, text="Settings", command=self.calibSettingsCallback)
        self.btnCalibSettings.pack(side="right",padx=15, pady=15)      
        self.setCalibrationMode(None)
    """
    Set Calibration Tab
    """
    def setCalibrationTab(self):
        if self.measFuncVar.get() == 1:
            if not self.frCalMode.winfo_ismapped():
                self.frCalMode.pack(fill=BOTH,expand=1)
                self.calMode.set(1)
            self.setCalibrationMode(None)
        elif self.measFuncVar.get() in (5,6):
            self.frCalMode.pack_forget()
            self.calMode.set(1)
            self.setCalibrationMode(None)
        elif self.measFuncVar.get() in (3,4,7):
            self.frCalMode.pack_forget()
            self.calMode.set(2)
            self.setCalibrationMode(None)
    """
    Calibration Settings Callback
    """    
    def calibSettingsCallback(self):
        top = Toplevel(self.root)
        top.title("Calibration Settings")
        pw = PanedWindow(top, orient=VERTICAL)
        pw.pack(fill=BOTH,expand=1)
        ### Characteristic Impedance ###
        pw.add(self.radioFrame(pw, self.getSortedList(self.analyzer.CharacteristicImpedances, 'items'), "Characteristic Impedance", self.charImp, 'left', self.setCharacteristicImpedance))
        ### Open ###
        lfOpenStd = Labelframe(pw,text="Open Standard")
        lfOpenStd.pack(fill=BOTH)
        openStdPacklist = {'Conductance [S]:' : (self.openCond , self.eOpenCondCallback),
                           'Capacitance [F]:' : (self.openCap  , self.eOpenCapCallback)}
        self.labelEntryH(lfOpenStd, openStdPacklist)        
        pw.add(lfOpenStd)   
        ### Load ###
        lfLdStd = Labelframe(pw,text="Load Standard")
        lfLdStd.pack(fill=BOTH)
        ldStdPacklist = {'Resistance [Ohm]:' : (self.ldRes , self.eLdResCallback),
                         'Inductance [H]:'   : (self.ldInd , self.eLdIndCallback)}
        self.labelEntryH(lfLdStd, ldStdPacklist)   
        pw.add(lfLdStd)      
        ### Short ###
        lfShtStd = Labelframe(pw,text="Short Standard")
        lfShtStd.pack(fill=BOTH)
        shtStdPacklist = {'Resistance [Ohm]:' : (self.shtRes , self.eShtResCallback),
                         'Inductance [H]:'    : (self.shtInd , self.eShtIndCallback)}
        self.labelEntryH(lfShtStd, shtStdPacklist)
        pw.add(lfShtStd) 
        ### Ok ###
        btnOk = Button(top,text="Ok",command=top.destroy)
        btnOk.pack()
    def setCalibrationMode(self, mode):
        if self.calMode.get() == 1:
            if not self.pwTransCalib.winfo_ismapped():
                self.pwTransCalib.pack()
            self.pwReflCalib.pack_forget()
        else:
            if not self.pwReflCalib.winfo_ismapped():
                self.pwReflCalib.pack()
            self.pwTransCalib.pack_forget()
    def setCharacteristicImpedance(self, impedance):
        print self.analyzer.setCharacteristicImpedance(impedance)     
    def eOpenCondCallback(self, event):
        print self.analyzer.setOpenCalStd(self.openCond.get(),self.openCap.get())
    def eOpenCapCallback(self,event):
        print self.analyzer.setOpenCalStd(self.openCond.get(),self.openCap.get())
    def eLdResCallback(self,event):
        print self.analyzer.setLoadCalStd(self.ldRes.get(), self.ldInd.get())
    def eLdIndCallback(self,event):
        print self.analyzer.setLoadCalStd(self.ldRes.get(), self.ldInd.get())
    def eShtResCallback(self,event):
        print self.analyzer.setShortCalStd(self.shtRes.get(),self.shtInd.get())
    def eShtIndCallback(self,event):
        print self.analyzer.setShortCalStd(self.shtRes.get(),self.shtInd.get())
    def getShort(self):
        print self.analyzer.shortCal()
    def getLoad(self):
        print self.analyzer.loadCal()
    def getOpen(self):
        print self.analyzer.openCal()
    def getThrough(self):
        print self.analyzer.thruCal()
    def getIsolation(self):
        print self.analyzer.isoCal()
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    """
    Helper Methods:
        - radioFrame
        - plot
        - setAxesLabels
        - saveData
        - show
        - getSortedList
    """
    
    """
    Radio Frame
    
    """     
    def radioFrame(self, parent, paramList, label, var, orient, cmd):
        lf = Labelframe(parent, text = label)
        lf.pack(fill = BOTH, expand = 1)
        i = 0
        for txt, val in paramList:
            rb = Radiobutton(lf, text = txt, value = i, variable = var, command = partial(cmd,txt))
            rb.pack(side=orient,padx=5,anchor=W)
            i = i+1
        var.set(0)
        return lf
    """
    plot
    
    """
    def plot(self):
        if (self.analyzer.status_Connected):
            self.setAxesLabels() 
            # https://github.com/hgrecco/pyvisa/blob/master/docs/rvalues.rst
            self.regX = np.array((self.analyzer.getRegister('X'))
            #self.regX = np.random.rand(401)
            
            
        #print type(self.analyzer.getRegister('X'))
            self.regA = np.array((self.analyzer.getRegister('A'))
            #self.regA = np.random.rand(401)
            self.ax1.cla()
            self.ax1.plot(self.regX, self.regA, 'y')
            self.ax1.set_xlabel(self.xLbl,fontsize='medium')
            # Make the y-axis label and tick labels match the line color.
            self.ax1.set_ylabel(self.yLbl[0], color='y',fontsize='medium')
            
            for tl in self.ax1.get_yticklabels():
                tl.set_color('y')
            
            
            self.regB = np.array((self.analyzer.getRegister('B'))
            #self.regB = np.random.rand(401)
            self.ax2.cla()
            if self.measFuncVar.get() != 2: # Don't plot 2nd axis in Spectrum Mode
                self.ax2.plot(self.regX, self.regB, 'c')
                self.ax2.set_ylabel(self.yLbl[1], color='c',fontsize='medium')
                for tl in self.ax2.get_yticklabels():
                    tl.set_color('c')
            
            self.canvas.draw()
    """
    Setting Axes Labels
    """
    def setAxesLabels(self):
        XLABELS = ('Frequency [Hz]',
            'DC Bias [V]',
            'Osc Lvl [V]',
            'Osc Lvl [dBm]',
            r'Osc Lvl [dB$\mu$V]')
        self.xLbl = XLABELS[self.sweepParameter.get()] 
        angleStr = ('[deg]','[rad]')[self.angleMode.get()]
        if self.measFuncVar.get() == 1:
            YLABELS= [('Gain [dB]','Phase '+angleStr),
            ('Gain','Phase '+angleStr),
            ('Re {Gain}','Im {Gain}'),
            ('Gain [dB]','Group Delay')]
            self.yLbl = YLABELS[self.formatNetwork.get()]
        elif self.measFuncVar.get() == 2:
            YLABELS= ('dBm',r'dB$\mu$V', 'Vrms', 'dBm/Hz', r'dB$\mu$V/Hz', 'V/Hz')
            self.yLbl = (YLABELS[self.cbUnitSpec.current()],'')
        elif self.measFuncVar.get() == 3:
            YLABELS= [('|Z|', 'Theta'),
                ('R','X'), 
                ('Ls','Rs'), 
                ('Ls','Q'),
                ('Cs','Rs'),
                ('Cs','D'),
                ('|Y|','Theta'),
                ('G','B'),
                ('Lp','Rp'),
                ('Lp','Q'),
                ('Cp','Rp'),
                ('Cp','D')]
            self.yLbl = YLABELS[self.cbFormatImp.current()]
        elif self.measFuncVar.get() in (4,7):
            YLABELS= [('Gain [dB]','Phase '+angleStr),
            ('Gain','Phase '+angleStr),
            ('Re {Gain}','Im {Gain}'),
            ('Gain [dB]','Group Delay')]
            self.yLbl = YLABELS[self.formatS1122.get()]
        elif self.measFuncVar.get() in (5,6):
            YLABELS= [('Gain [dB]','Phase '+angleStr),
            ('Gain','Phase '+angleStr),
            ('Re {Gain}','Im {Gain}'),
            ('Gain [dB]','Group Delay')]
            self.yLbl = YLABELS[self.formatS2112.get()] 
    """
    Show
    
    """
    def show(self):
        self.root.mainloop()
    """
    Get Sorted List
    """
    def getSortedList(self, ilist, what):
        if what == 'items':
            return sorted(ilist.items(), key=lambda x:x[1])
        if what == 'keys':
            return sorted(ilist.keys(), key=lambda x:x[1])
        if what == 'values':
            return sorted(ilist.values(), key=lambda x:x[1])
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""   
mw = MainWindow()
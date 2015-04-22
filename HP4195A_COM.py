# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 19:31:21 2015

Communication Class for interfacing the HP4195A-Network-Analyzer.


@author: Jochen Fink & Patrick Agostini 
"""

## Packages
import visa

class HP4195A_Constants:
    
        """
        General Constatnts
        """
        MeasurementModes = {
            'NETWORK'   : 1,
            'SPECTRUM'  : 2,
            'IMPEDANCE' : 3,
            'S11'       : 4,
            'S21'       : 5,
            'S12'       : 6,
            'S22'       : 7  
        }
        GeneralIFModes = {
            'Normal'           : 1,
            'High Sensitivity' : 2
        }        
        TriggerModes = {
            'Continuous': 1,
            'Single'    : 2,
            'Manual'    : 3
        }
        BW_Resolutions = ('Auto', 
                          '3'     , 
                          '10'    , 
                          '30'    , 
                          '100'   , 
                          '300'   , 
                          '1000'  , 
                          '3000'  , 
                          '10000' , 
                          '30000' , 
                          '100000', 
                          '300000'
        )
        """
        Network/S-Mode Specific Constants
        """
        NetworkModePorts = {
            'T1/R1': 1,
            'T2/R1': 2,
            'R2/R1': 3,
            'T1/R2': 4,
            'T2/R2': 5
        }
        NetworkModeFormats = {
            'T/R(dB)-Phase'   : 1,
            'R2/R1(db)-Phase' : 1,
            'T/R-Phase'       : 2,
            'R2/R1-Phase'     : 2,
            'T/R(Re-Im)'      : 3,
            'R2/R1(Re-Im)'    : 3,
            'T/R-GD'          : 4,
            'R2/R1-GD'        : 4,
        }
        SModeFormats = {
            'T/R(dB)-Phase'   : 1,
            'R2/R1(db)-Phase' : 1,
            'T/R-Phase'       : 2,
            'R2/R1-Phase'     : 2,
            'T/R(Re-Im)'      : 3,
            'R2/R1(Re-Im)'    : 3,
            'T/R-GD'          : 4,
            'R2/R1-GD'        : 4,
        }        
        """
        Spectrum-Mode Specific Constants
        """
        SpectrumModeFormats = {
            'dBm'    : 1,
            'dBuV'   : 2,
            'Vrms'   : 3,
            'dBm/HZ' : 4,
            'dBuV/HZ': 5,
            'uV/HZ'  : 6
        }
        SpectrumModeFormatsTeX = {
            'dBm'    : 1,
            r'dBµV'  : 2,
            'Vrms'   : 3,
            'dBm/HZ' : 4,
            'dBµV/HZ': 5,
            'µV/HZ'  : 6
        }
        SpectrumModePorts = {
            'R1': 1,
            'T1': 2,
            'R2': 3,
            'T2': 4
        }
        SpectrumModeTrackingGenOut = {
            'NONE': 0,
            'S1': 1,
            'S2': 2
        }        
        SpectrumIFModes = {
            'Normal'           : 1,
            'Low Distortion'   : 2,
            'High Sensitivity' : 3
        }
        """
        Impedance-Mode Specific Constants
        """
        ImpedanceModePorts = {
            'T1/R1': 1,
            'T2/R1': 2,
            'R2/R1': 3,
            'T1/R2': 4,
            'T2/R2': 5
        }
        ImpedanceModeFormats = {
            'Z-Phase': 1,
            'R-X'    : 2,
            'Ls-Rs'  : 3,
            'Ls-Q'   : 4,
            'Cs-Rs'  : 5,
            'Cs-D'   : 6,
            'Y-Phase': 7,
            'G-B'    : 8,
            'Lp-Rp'  : 9,
            'Lp-Q'   : 10,
            'Cp-Rp'  : 11,
            'Cp-D'   : 12
            }
        """
        Calibration Specific Constants
        """       
        CharacteristicImpedances = {
            '50': 1,
            '75': 2
        }
        OffsetCompensationFunctions = {
            'None'        : 0,
            '0S Offset'   : 1,
            '0O Offset'   : 2,
            '0S&0O Offset': 3
        }
        CalibrationModes = {
            'Transmission' : 1,
            'Reflection'   : 2        
        }
        
        AngleMode = {
            'Deg' : 1,
            'Rad' : 2
        }
        """
        Stimulus Parameters
        """
        SweepParameters = {
            'Frequency [Hz]' : 1,
            'DC Bias [V]'    : 2,
            'Osc Lvl [V]'    : 3,
            'Osc Lvl [dBm]'  : 4,
            'Osc Lvl [dBµV]' : 5
        }   
        SweepModes = {
            'Linear'      : 1,
            'Logarithmic' : 2,
        }
        TriggerModes = {   
            'Continuous' : 1,
            'Single'     : 2,
            'Manual'     : 3
        }     
        
        
class HP4195A(HP4195A_Constants):
    DeviceObj            = ()    
    visa_ResourceManager = ()
    GPIBO_Address        = ()
    """
    Class Status Flags    
    """    
    status_Connected     = False    
    status_MeasMode      = 'NETWORK'
    status_CurrentAngle  = ()
    status_CurrentFormat = ()
    status_CurrentPort   = ()
    status_CurrentDA     = () 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Class Init Stuff
    """
    def __init__(self):
        self.visa_ResourceManager = visa.ResourceManager()
        self.getDevAddr()
    def __del__(self):    
        self.Disconnect() 
    def getDevAddr(self):
        devList      = self.visa_ResourceManager.list_resources()
        if devList: 
            self.GPIBO_Address = [s for s in devList if "GPIB0" in s]
            self.GPIBO_Address = str(self.GPIBO_Address[0])
            return 1   
    def Connect(self):       
        if self.getDevAddr():
            self.DeviceObj = self.visa_ResourceManager.open_resource(self.GPIBO_Address)
            self.status_Connected = True
    def Disconnect(self):
        self.visa_ResourceManager.close
        self.status_Connected = False
        self.GPIBO_Address    = ()
        self.DeviceObj        = ()
    def queryDev(self, command):
        answer = None
        if self.status_Connected:
            answer = self.DeviceObj.query(command)
        return answer
    def sendDev(self, command):  
        if self.status_Connected:
            self.DeviceObj.write(command)
        else:
            print "Dev not Connected"
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Command Handling
    """
    def sendCommand(self, cmd, value, list):
        if self.checkCommand(list, value):
            if self.sendDev(cmd + str(self.getCommand(list, value))):
                return 1
        return 0
    def checkCommand(self, list, value):
        if isinstance(value, (str)):
            if self.isStrCommand(list, value):
                return value
        else:
            if self.isNumCommand(list, value):
                return self.isNumCommand(list, value)
        print("Error: Command does not Exist!\nFollowing Commands are Accepted:\n")
        self.printCommandList(list)
        return False     
    def getCommand(self, list, value):
        if isinstance(value, (str)):
            return self.getIntCommandValue(list, value)
        return value
    def isNumCommand(self, list, value):
        for k, v in list.iteritems():
            if v==value:
                return k
        return False
    def isStrCommand(self, list, value):
        for k, v in list.iteritems():
            if k==value:
                return True
        return False
    def getIntCommandValue(self, list, value):
        for k, v in list.iteritems():
            if k==value:
                return v
    def getStrCommandValue(self, list, value):
        if self.isStrCommand(list, value):
            return value
        else:
            for k, v in list.iteritems():
                if v==value:
                    return v
    def printCommandList(self, list):
         for k, v in list.iteritems():
             print str(k) + '   <<< or >>>   ' + str(v)
    def isNum(self, value):
        return isinstance(value, (int, long, float, complex))
    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False      
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Get & Set System Stuff
    """
    def getStatusByte(self):
        return self.queryDev("STB?")
    def getRevisionNumber(self):
        return self.queryDev("REV?")
    def getID(self):
        return self.queryDev("ID?")
    def getError(self):
        return self.queryDev("ERR?")        
    def getDisplayMessage(self):
        return self.queryDev("DISP?")
    def getComment(self):
        return self.queryDev("CMT?")
    def getRegister(self,name):
        command=name.upper()+"?"
        return self.queryDev(command)
    def setRegister(self,name,value):
        if self.isNum(value):
            if self.sendDev(name.upper() + "=" + str(value)):
                return 1
        return 0
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    General Functions
    
    """
    def setMeasurementMode(self, value):
        return self.sendCommand('FNC', value, self.MeasurementModes) 
    def setPort(self, value):
        if self.status_MeasMode   == 'NETWORK':
            return self.setNetworkPort(value)
        elif self.status_MeasMode == 'SPECTRUM':
            return self.setSpectrumPort(value)
        else:
            return self.setImpedancePort(value)
    def setFormat(self, value):
        if self.status_MeasMode == 'NETWORK':
            return self.setNetworkFormat(value)
        elif self.status_MeasMode == 'SPECTRUM':
            return self.setSpectrumFormat(value)
        elif self.status_MeasMode == 'IMPEDANCE':
            return self.setImpedanceFormat(value)
        else:
            return self.setSModeFormat(value)    
    def setDelayApperture(self, value):
        if self.isfloat(value):
            return self.setRegister('DFREQ' , value)
        return 0
    def setAngleMode(self, mode):
        self.sendDev(mode.upper)
        self.status_CurrentAngle = mode
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Network Mode Functions
    """
    def setNetworkPort(self, value):
        return self.sendCommand('PORT', value, self.NetworkModePorts) 
    def setNetworkFormat(self, value):
        return self.sendCommand('GPP', value, self.NetworkModeFormats)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Spectrum Mode Functions
    """
    def setSpectrumFormat(self, value):    
        return self.sendCommand('SAP', value, self.SpectrumModeFormats)
    def setSpectrumPort(self, value):              
        return self.sendCommand('PORT', value, self.SpectrumModePorts)
    def setTrackingGeneratorOutput(self, value):   
        return self.sendCommand('PWR', value, self.SpectrumModeTrackingGenOut)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Impedance Mode Functions
    """
    def setImpedanceFormat(self, value):
        return self.sendCommand('IMP', value, self.ImpedanceModeFormats)
    def setImpedancePort(self, value):
        return self.sendCommand('PORT', value, self.ImpedanceModePorts)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    S Mode Functions
    """
    def setSModeFormat(self, value):       
        if self.currentMode == 'S11' or self.currentMode == 'S22':
            return self.sendCommand('SPI', value, self.SModeFormats)
        else:
            return self.sendCommand('GPP', value, self.SModeFormats)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    """
    Calibration Functions
    """
    def setCharacteristicImpedance(self, value):
        if self.isfloat(value):
            return self.sendDev('CHRZ' + str(self.CharacteristicImpedances[value]))
        return 0
    def shortCal(self):
        return self.sendDev('SHTCAL')
    def loadCal(self):
        return self.sendDev('LDCAL')
    def openCal(self):
        return self.sendDev('OPNCAL')
    def normIsnCal(self):
        return self.sendDev('CALT5')
    def isoCal(self):
        return self.sendDev('ISNCAL')
    def normalizeThru(self):
        return self.sendDev('CALT4')    
    def thruCal(self):
        return self.sendDev('THRCAL')
    def correctnOnOff(self, on):
        return self.sendDev('CORR' + str(int(bool(on))))
    def calStdModify(self):
        return self.sendDev('STDDSP')
    def setOpenCalStd(self, conductance, capacitance):
        if self.isfloat(conductance) and self.isfloat(capacitance):
            return self.sendDev('OPNSTD=' + str(conductance) + ',' + str(capacitance))
        return 0
    def setLoadCalStd(self, resistance, inductance):
        if self.isfloat(resistance) and self.isfloat(inductance):
            return self.sendDev('LDSTD=' + str(resistance) + ',' + str(inductance))
        return 0
    def setShortCalStd(self, conductance, capacitance):
        if self.isfloat(conductance) and self.isfloat(capacitance):            
            return self.sendDev('SHTSTD=' + str(conductance) + ',' + str(capacitance))
        return 0
    def onePortFullCal(self):
        return self.sendDev('CALT3')
    def onePortPartCal(self):
        return self.sendDev('CALT2')
    def NormalizeOpen(self):
        return self.sendDev('CALT1')
    def zeroResistanceCalibration(self):
        return self.sendDev('ZOCMP')
    def zeroConductanceCalibration(self):
        return self.sendDev('ZSCMP')
    def setCompensationFunction(self,value):
        return self.sendDev('CMPT' + str(self.OffsetCompensationFunctions[value]))
    def getBias(self):
        self.getRegister('BIAS')
    def getCenterFreq(self):
        self.getRegister('CENTER')    
    def getConstFreq(self,value):
        self.getRegister('FREQ')        
    def getNumberOfPoints(self):
        self.getRegister('NOP')
    def getOsc1Amplitude(self):
        self.getRegister('OSC1')        
    def getOsc2Amplitude(self):
        self.getRegister('OSC2')        
    def getSpan(self):
        self.getRegister('SPAN')
    def getStartFreq(self):
        self.getRegister('START')        
    def getStep(self,value):
        self.getRegister('STEP')    
    def getStopFreq(self,value):
        self.getRegister('STOP')       
    def getSweepTime(self):
        self.setRegister('ST')
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""       
    """
    Port Extensions
    """    
    def setExtensionLength(self, port, value):
        if self.isfloat(value):
            return self.setRegister('PE' + port, value)
        return 0
    def portExtensionOnOff(self, onOff):
        self.sendDev('PEXT' + str(int(bool(onOff))))  
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    """
    Set Stimulus Settings  
    """
    def setSweepParameter(self, value):
        return self.sendCommand('SWP', value, self.SweepParameters)        
    def setSweepMode(self,value):
        return self.sendCommand('SWT', value, self.SweepModes)
    def setBias(self, value):
        return self.setRegister('BIAS'  , value)
    def setCenterFreq(self, value):
        return self.setRegister('CENTER', value)  
    def setConstFreq(self, value):
        return self.setRegister('FREQ'  , value)       
    def setNumberOfPoints(self, value):
        return self.setRegister('NOP'   , value)
    def setOsc1Amplitude(self, value):
        return self.setRegister('OSC1'  , value)       
    def setOsc2Amplitude(self, value):
        return self.setRegister('OSC2'  , value)       
    def setSpan(self, value):
        return self.setRegister('SPAN'  , value)
    def setStartFreq(self, value):
        return self.setRegister('START' , value)        
    def setStep(self, value):
        return self.setRegister('STEP'  , value)  
    def setStopFreq(self, value):
        return self.setRegister('STOP'  , value)
    def setSweepTime(self, value):
        return self.setRegister('ST'    , value)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Set Receiver Settings
    
    """
    def setIFRange(self, value):
        if self.currentMode=="SPECTRUM":
            return self.sendCommand('IRNG', value, self.SpectrumIFModes)
        else:
            return self.sendCommand('IRNG', value, self.GeneralIFModes)        
    def setInputAttenuation(self, input, value):
        return self.setRegister('AT' + input, value)
    def setResolutionBandwidth(self, value):
        if value.upper() == 'AUTO':
            return self.sendDev('CPL1')
        elif str(value) in self.BW_Resolutions:
            if self.sendDev('CPL0'):
                return self.setRegister('RBW', int(value))
            return 0
        else:
            print("Available Bandwidths:\n" + self.BW_Resolutions)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Set Trigger Mode
    
    
    """
    def setTriggerMode(self, value):
        self.sendDev('SWM' + str(self.TriggerModes[value]))
        self.status_TriggerMode = self.TriggerModes[value]
    def triggerReset(self):
        self.sendDev('SWTRG')
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""           
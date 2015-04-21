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
            'NETWORK' : 1,
            'SPECTRUM': 2,
            'IMPEDANCE': 3,
            'S11': 4,
            'S21': 5,
            'S12': 6,
            'S22': 7  
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

###############################################################################
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
            
 ##############################################################################
    def checkCommand(self, list, value):
        if str(type(value))=="str":
            if self.isStrCommand(list, value):
                return value
        else:
            if self.isNumCommand(list, value):
                return self.isNumCommand(list, value)
        print("Error:\nCommand does not Exist!\nFollowing Commands are Accepted:\n")
        self.printCommandList(list)
        return False     
    def getCommand(self, list, value):
        if str(type(value))=="str":
            if self.isStrCommand(list, value):
                return value
        return value
    def isNumCommand(self, list, value):
        for k, v in list.iteritems():
            if v==value:
                return k
        return False
    def isStrCommand(self, list, value):
        for k in list.iteritems():
            if k==value:
                return True
        return False
    def getStrCommandValue(self, list, value):
        if self.isStrCommand(list, value):
            return value
        else:
            for k, v in list.iteritems():
                if v==value:
                    return k
    def printCommandList(self, list):
         for k, v in list.iteritems():
             print str(k) + '   <<< or >>>   ' + str(v)
###############################################################################       
      
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
        command=name.upper()+"="+str(value)
        return self.sendDev(command)

###############################################################################
## Measurement Configuration  
    def setMeasurementMode(self, value):
        if self.checkCommand(self.MeasurementModes, value):
            self.sendDev('FNC' + self.getCommand(self.MeasurementModes, value))
            self.status_MeasMode = self.getStrCommandValue(self.MeasurementModes, value)
    
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
    
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    Special Functions
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    def setDelayApperture(self, value):
        self.setRegister('DFREQ' , value)
        self.status_CurrentDA = value
    
    def setAngleMode(self, mode): #value = 'rad', 'deg'
        self.sendDev(mode.upper)
        self.status_CurrentAngle = mode
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Network Mode Functions
    """
    def setNetworkPort(self, value):
        if self.checkCommand(self.NetworkPortModes, value):
            self.sendDev('PORT' + str(self.NetworkPortModes[value]))
            self.status_CurrentPort = self.getStrCommandValue(self.NetworkPortModes, value)
            return True
        return False
        
    def setNetworkFormat(self, value):
        if self.checkCommand(self.NetworkModeFormats, value):
            self.sendDev('GPP' + str(self.NetworkModeFormats[value]))
            self.status_CurrentFormat = self.getStrCommandValue(self.NetworkModeFormats, value)
            return True
        return False
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Spectrum Mode Functions
    """
    def setSpectrumFormat(self, value):
        if self.checkCommand(self.SpectrumModeFormats, value):
            self.sendDev('SAP' + str(self.SpectrumModeFormats[value]))
            self.status_CurrentFormat = self.getStrCommandValue(self.SpectrumModeFormats, value)
            return True
        return False        
    def setSpectrumPort(self, value):
        if self.checkCommand(self.SpectrumModePorts, value):
            self.sendDev('PORT' + str(self.SpectrumModePorts[value]))
            self.status_CurrentPort = self.getStrCommandValue(self.SpectrumModePorts, value)
            return True
        return False                
    def setTrackingGeneratorOutput(self, value):
        if self.checkCommand(self.SpectrumModeTrackingGenOut, value):
            self.sendDev('PWR' + str(self.SpectrumModeTrackingGenOut[value]))
            self.status_CurrentTrackingMode = self.getStrCommandValue(self.SpectrumModeTrackingGenOut, value)
            return True
        return False       
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Impedance Mode Functions
    """
    def setImpedanceFormat(self, value):
        if self.checkCommand(self.ImpedanceModeFormats, value):
            self.sendDev('IMP' + str(self.ImpedanceModeFormats[value]))
            self.status_CurrentFormat = self.getStrCommandValue(self.ImpedanceModeFormats, value)
            return True
        return False  
        
    def setImpedancePort(self, value):
        if self.checkCommand(self.ImpedanceModePorts, value):
            self.sendDev('PORT' + str(self.ImpedanceModePorts[value]))
            self.status_CurrentPort = self.getStrCommandValue(self.ImpedanceModePorts, value)
            return True
        return False  
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    S Mode Functions
    """
    def setSModeFormat(self, value):
        if self.checkCommand(self.SModeFormats, value):        
            if self.currentMode == 4 or self.currentMode == 7:
                self.sendDev('SPI' + str(self.SModeFormats[value]))
                self.status_CurrentFormat = self.getStrCommandValue(self.SModeFormats, value)
                return True
            else:
                self.sendDev('GPP' + str(self.SModeFormats[value]))
                self.status_CurrentFormat = self.getStrCommandValue(self.SModeFormats, value)
                return True
        return False
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    """
    Calibration Functions
    """
        
    def normIsnCal(self):
        self.sendDev('CALT5')
        
    def isolatn(self):
        self.sendDev('ISNCAL')
        
    def normalizeThru(self):
        self.sendDev('CALT4')    
        
    def thruCal(self):
        self.sendDev('THRCAL')
        
    def correctnOnOff(self, on):
        self.sendDev('CORR' + str(int(bool(on))))
        
    def calStdModify(self):
        self.sendDev('STDDSP')
        
    def setOpenCalStd(self, conductance, capacitance):
        self.sendDev('OPNSTD=' + str(conductance) + ',' + str(capacitance))
        
    def setLoadCalStd(self, resistance, inductance):
        self.sendDev('LDSTD=' + str(resistance) + ',' + str(inductance))
        
    def setShortCalStd(self, conductance, capacitance):
        self.sendDev('SHTSTD=' + str(conductance) + ',' + str(capacitance))
            
    def onePortFullCal(self):
        self.sendDev('CALT3')

    def onePortPartCal(self):
        self.sendDev('CALT2')
        
    def NormalizeOpen(self):
        self.sendDev('CALT1')
        
    def shortCal(self):
        self.sendDev('SHTCAL')
        
    def loadCal(self):
        self.sendDev('LDCAL')
        
    def openCal(self):
        self.sendDev('OPNCAL')
        
    # 0S/0Ohm Offset Compensation

    def setCharacteristicImpedance(self, value):
        self.sendDev('CHRZ' + str(self.CharacteristicImpedances[value]))
        
    def zeroResistanceCalibration(self):
        self.sendDev('ZOCMP')
        
    def zeroConductanceCalibration(self):
        self.sendDev('ZSCMP')
        
    def setCompensationFunction(self,value):
        self.sendDev('CMPT' + str(self.OffsetCompensationFunctions[value]))

###############################################################################        
## Port Extension
    
    def setExtensionLength(self, port, value): #port = 'R1','R2','T1','T2','P1','P2'
        self.setRegister('PE' + port, value)
        
    def portExtensionOnOff(self, onOff):
        self.sendDev('PEXT' + str(int(bool(onOff))))     
###############################################################################
## Stimulus Settings

    def setBias(self,value):
        self.setRegister('BIAS',value)
        
    def setCenterFreq(self,value):
        self.setRegister('CENTER',value)
    
    def setConstFreq(self,value):
        self.setRegister('FREQ',value)
        
    def setNumberOfPoints(self,value):
        self.setRegister('NOP',value)

    def setOsc1Amplitude(self,value):
        self.setRegister('OSC1',value)
        
    def setOsc2Amplitude(self,value):
        self.setRegister('OSC2',value)
        
    def setSpan(self,value):
        self.setRegister('SPAN',value)

    def setStartFreq(self,value):
        self.setRegister('START',value)
        
    def setStep(self,value):
        self.setRegister('STEP',value)
    
    def setStopFreq(self,value):
        self.setRegister('STOP',value)

    def setSweepParameter(self,value):
       self.sendDev('SWP'+str(value))
       self.currentSweepParameter=value
       
    def setSweepTime(self,value):
        self.setRegister('ST',value)
       
    def setSweepType(self,value):
        self.sendDev('SWT'+str(value))
        self.currentSweepType=value
        
###############################################################################
## Get Stimulus Settings

    def getBias(self):
        self.getRegister('BIAS')
        
    def getCenterFreq(self):
        self.getRegister('CENTER')
    
    def getConstFreq(self,value):
        self.setRegister('FREQ')
        
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

#    def getSweepParameter(self):
#       return self.currentSweepParameter
       
    def getSweepTime(self):
        self.setRegister('ST')
       
#    def getSweepType(self):
#        return self.currentSweepType
   
###############################################################################
## Receiver Settings
    def setIFRange(self, value):
        if self.currentMode==2:
            self.sendDev('IRNG' + self.SpectrumIFModes[value])
        else:
            self.sendDev('IRNG' + self.GeneralIFModes[value])
        
    def setInputAttenuation(self,input,value): #input = 'R1', 'T1', 'R2', T2'
        self.setRegister('AT' + input, value)
    
    def setResolutionBandwidth(self, value):
        if value.upper() == 'AUTO':
            self.sendDev('CPL1')
        elif str(value) in self.BW_Resolutions:
            self.sendDev('CPL0')
            self.setRegister('RBW', int(value))
        else:
            print("Available Bandwidths:\n" + self.BW_Resolutions)
            
 ###############################################################################
## Measurement Triggering
            
    def setTriggerMode(self, value):
        self.sendDev('SWM' + str(self.TriggerModes[value]))
        self.status_TriggerMode = self.TriggerModes[value]
        
    def triggerReset(self):
        self.sendDev('SWTRG')
        
###############################################################################

            
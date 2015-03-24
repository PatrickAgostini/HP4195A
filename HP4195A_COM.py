# -*- coding: utf-8 -*-
"""
Created on Thu Mar 05 19:31:21 2015

@author: 
"""
import visa

class HP4195A_COM:
    
    deviceOpen = False
    
    def __init__(self):
        self.rmObj = visa.ResourceManager()
        self.getDevAddr()
        #self.openDev()
    
    def __del__(self):    
        self.closeDev()
        
    def getDevAddr(self):
        devList      = self.rmObj.list_resources()
        self.devAddr = None
        if devList: 
            self.devAddr = [s for s in devList if "GPIB0" in s]
            self.devAddr = str(self.devAddr[0])
        
    def openDev(self):
        self.device=None        
        self.deviceOpen = False
        if self.devAddr:
            self.device = self.rmObj.open_resource(self.devAddr)
            self.deviceOpen = True
    
    def closeDev(self):
        self.rmObj.close
        self.deviceOpen = False
        
    def queryDev(self, command):
        answer = None
        if self.deviceOpen:
            answer = self.device.query(command)
        return answer
        
    def sendDev(self, command):  
        if self.deviceOpen:
            self.device.write(command)
 
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
   
    def setMeasurementFunction(self,value):
        mode = {
            'NETWORK' : 1,
            'SPECTRUM': 2,
            'IMPEDANCE': 3,
            'S11': 4,
            'S21': 5,
            'S12': 6,
            'S22': 7  
        }
        self.sendDev('FNC'+mode[value])
        self.currentMode=mode[value]

###############################################################################
## Network Configuration

    def setNetworkPort(self,value):
        port = {
            'T1/R1': 1,
            'T2/R1': 2,
            'R2/R1': 3,
            'T1/R2': 4,
            'T2/R2': 5
        }
        self.sendDev('PORT'+str(port[value]))
        
    def setNetworkFormat(self,value): #value = 1,2,3,4
        self.sendDev('GPP'+str(value))
        
    def setAngleMode(self,mode): #value = 'rad', 'deg'
        self.sendDev(mode.upper)
    
    def setDelayApperture(self,value):
        self.setRegister('DFREQ',value)
        
## Network Measurement Calibration
        
    def normIsnCal(self):
        self.sendDev('CALT5')
        
    def isolatn(self):
        self.sendDev('ISNCAL')
        
    def normalizeThru(self):
        self.sendDev('CALT4')    
        
    def thruCal(self):
        self.sendDev('THRCAL')
        
    def correctnOnOff(self,on):
        if on:
            self.sendDev('CORR1')
        else:
            self.sendDev('CORR0')
            
    def setCharacteristicImpedance(self,Z0): #Z0 = 50, 75
        if Z0 == 50:
            self.sendDev('CHRZ1')
        elif Z0 == 75:
            self.sendDev('CHRZ1')
        else:
            print('Error: Argument must be 50 or 75.')
        
    def calStdModify(self):
        self.sendDev('STDDSP')
        
    def setOpenCalStd(self,conductance,capacitance):
        self.sendDev('OPNSTD='+str(conductance)+','+str(capacitance))
        
    def setLoadCalStd(self,resistance,inductance):
        self.sendDev('LDSTD='+str(resistance)+','+str(inductance))
        
    def setShortCalStd(self,conductance,capacitance):
        self.sendDev('SHTSTD='+str(conductance)+','+str(capacitance))
            
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
        
###############################################################################
## Spectrum Configuration
    
    def setMeasurementUnits(self,value):
        unit = {
            'DBM': 1,
            'DBUV': 2,
            'VRMS': 3,
            'DBM/HZ': 4,
            'DBUV/HZ': 5,
            'UV/HZ': 6
        }
        self.sendDev('SAP'+str(unit[value]))
        
    def setSpectrumPort(self,value):
        port = {
            'R1': 1,
            'T1': 2,
            'R2': 3,
            'T2': 4
        }
        self.sendDev('PORT'+str(port[value]))
        
    def setTrackingGeneratorOutput(self,value):
        output = {
            'NONE': 0,
            'S1': 1,
            'S2': 2
        }
        self.sendDev('PWR'+str(output[value]))

###############################################################################
## Impedance Configuration

    def setImpedanceMeasurementParameters(self,value): #value = 1,2,3,...,12
        self.sendDev('IMP'+str(value))
        
    def setImpedancePort(self,value): # Same as setNetworkPort() !!!
        port = {
            'T1/R1': 1,
            'T2/R1': 2,
            'R2/R1': 3,
            'T1/R2': 4,
            'T2/R2': 5
        }
        self.sendDev('PORT'+str(port[value]))
        
## Impedance Measurement Calibration
 
 # ONE PORT FULL CAL   
    def setCharacteristicImpedance(self,Z0): #Z0 = 50, 75
        if Z0 == 50:
            self.sendDev('CHRZ1')
        elif Z0 == 75:
            self.sendDev('CHRZ1')
        else:
            print('Error: Argument must be 50 or 75.')
        
    def calStdModify(self):
        self.sendDev('STDDSP')
        
    def setOpenCalStd(self,conductance,capacitance):
        self.sendDev('OPNSTD='+str(conductance)+','+str(capacitance))
        
    def setLoadCalStd(self,resistance,inductance):
        self.sendDev('LDSTD='+str(resistance)+','+str(inductance))
        
    def setShortCalStd(self,conductance,capacitance):
        self.sendDev('SHTSTD='+str(conductance)+','+str(capacitance))
            
    def onePortFullCal(self):
        self.sendDev('CALT3')
        
    def shortCal(self):
        self.sendDev('SHTCAL')
        
    def loadCal(self):
        self.sendDev('LDCAL')
        
    def openCal(self):
        self.sendDev('OPNCAL')
        
 # 0S/0Ohm Offset Compensation

    def zeroResistanceCalibration(self):
        self.sendDev('ZOCMP')
        
    def zeroConductanceCalibration(self):
        self.sendDev('ZSCMP')
        
    def setCompensationFunction(self,value):
        cmpFunc={
            'COMPEN NONE': 0,
            '0S OFFSET': 1,
            '0, OFFSET': 2,
            '0S&0, OFFSET': 3
        }
        self.sendDev('CMPT'+str(cmpFunc[value]))

###############################################################################        
## Port Extension
    
    def setExtensionLength(self,port,value): #port = 'R1','R2','T1','T2','P1','P2'
        self.setRegister('PE'+port,value)
        
    def portExtensionOnOff(self,on):
        if on:
            self.sendDev('PEXT1')
        else:
            self.sendDev('PEXT0')
    
###############################################################################
## S-Parameter Measurement
    

    
    def setSParameterFormat(self,value): #value = 1,2,3,4 / Same as setNetworkFormat
        if self.currentMode == 4 or self.currentMode == 7:
            self.sendDev('SPI'+str(value))
        else:
            self.sendDev('GPP'+str(value))
        
    def setAngleMode(self,mode): #value = 'rad', 'deg'
        self.sendDev(mode.upper)
    
    def setDelayApperture(self,value):
        self.setRegister('DFREQ',value)
        
## S-Parameter Measurement Calibration
        
    def normIsnCal(self):
        self.sendDev('CALT5')
        
    def isolatn(self):
        self.sendDev('ISNCAL')
        
    def normalizeThru(self):
        self.sendDev('CALT4')    
        
    def thruCal(self):
        self.sendDev('THRCAL')
        
    def correctnOnOff(self,on):
        if on:
            self.sendDev('CORR1')
        else:
            self.sendDev('CORR0')
            
    def setCharacteristicImpedance(self,Z0): #Z0 = 50, 75
        if Z0 == 50:
            self.sendDev('CHRZ1')
        elif Z0 == 75:
            self.sendDev('CHRZ1')
        else:
            print('Error: Argument must be 50 or 75.')
        
    def calStdModify(self):
        self.sendDev('STDDSP')
        
    def setOpenCalStd(self,conductance,capacitance):
        self.sendDev('OPNSTD='+str(conductance)+','+str(capacitance))
        
    def setLoadCalStd(self,resistance,inductance):
        self.sendDev('LDSTD='+str(resistance)+','+str(inductance))
        
    def setShortCalStd(self,conductance,capacitance):
        self.sendDev('SHTSTD='+str(conductance)+','+str(capacitance))
            
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
   
    def setIFRange(self,value):
        if self.currentMode==2:
           IFmodes = {
                'Normal' : 1,
                'Low Distortion': 2,
                'High Sensitivity': 3
                }
        else:
            IFmodes = {
                'Normal' : 1,
                'High Sensitivity': 2
                }
        self.sendDev('IRNG'+IFmodes[value])
        
    def setInputAttenuation(self,input,value): #input = 'R1', 'T1', 'R2', T2'
        self.setRegister('AT'+input,value)
    
    def setResolutionBandwidth(self,value): #input = 'AUTO', 3, 10, 30, 100, ..., 300000
        rbwList = [3, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000]        
        if type(value)==str and value.upper() == 'AUTO':
            self.sendDev('CPL1')
        elif value in rbwList:
            self.sendDev('CPL0')
            self.setRegister('RBW',value)
        else:
            closest = min(rbwList, key=lambda x:abs(x-value))
            self.sendDev('CPL0')
            self.setRegister('RBW',closest)
            print('Argument must be in\n'+str(rbwList)+'\n\nResolution Bandwidth is set to '+str(closest)+'.')
            
 ###############################################################################
## Measurement Triggering
            
    def setTriggerMode(self,value):
        triggerModes = {
            'CONTINUOUS': 1,
            'SINGLE': 2,
            'MANUAL': 3
            }
        self.sendDev('SWM'+str(triggerModes[value]))
        self.triggerMode = triggerModes[value]
        
    def triggerReset(self):
        self.sendDev('SWTRG')
            
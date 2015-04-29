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
        General Constants
        """
        ErrorMessages ={ 
            0:'Input buffer full',
            1:'Back up RAM data lost',
            2:'EEPROM check sum error',
            10:'Undefined symbol',
            11:'Improper numeric expression',
            12:'Out of range 1E-37 -> 9.99999E+37)',
            13:'Improper delimiter',
            14:'Command syntax error',
            15:'Invalid select code number',
            16:'Invalid parameter range',
            17:'Not allowed in LOG sweep',
            18:'LOG sweep not allowed in OSC_dB',
            19:'NOP must be 2 to 401',
            20:'Not allowed in ASP',
            21:'Recursive call not allowed',
            22:'Freq. must be 0.001 to 500M Hz',
            23:'Zero to negative power',
            24:'Osc must be -50 thru +15 dBm /Osc must be 57 to 122 dBmuV / Osc must be 707mu to 1.26 V',
            25:'SPAN must be within 26dB in OSC sweep',
            26:'Bias must be -40 to +40 V',
            27:'Improper entry unit',
            28:'Sign must be same in LOG sweep',
            29:'Down sweep not allowed in SPECTRUM',
            30:'Improper definition in sweep end fctn',
            31:'Min. Resolution<=STEP<=SPAN',
            32:'STEP > SPAN error',
            33:'Write to read only register',
            34:'Improper math definition',
            35:'Not allowed in Zero Span',
            36:'Not allowed in present state',
            37:"Can't select manual sweep",
            39:'Must be 0<= SPAN <=full range',
            40:'Not allowed in SMITH display',
            41:'Multi statement not allowed',
            42:'Subscript out of range',
            43:'Delay aperture 0.5 to 100 %',
            44:'Only FREQ & LIN swp allowed in tau meas',
            45:"Can't measure tau in prog. point meas.",
            46:"Can't change in smith/polar display",
            47:'Not allowed in LOG scale',
            48:'Improper scale value',
            49:'Not allowed in manual sweep',
            50:'Not allowed in prog. measure',
            51:'Statement too complex',
            60:'Smith/polar display not allowed',
            61:'N must be >=2 in sweep range',
            62:'N must be >=2 in ana. range',
            63:'Not in o & * MKRS mode',
            64:'Markers not displayed',
            65:'Line cursor not displayed',
            66:'NOISE allowed only in SPECTRUM',
            70:"Can't change scale >20 times/sweep",
            71:'Select o marker mode',
            80:'Compen allowed only in impedance mode',
            81:'Calibration type mismatched',
            82:'Compen type mismatched',
            83:'No calibration type selected',
            100:"Can't change while data exist",
            101:'Memory fullall boxes used)',
            102:'Number of points full',
            103:'Sweep parameter mismatching',
            104:'Syntax error in SWEEP POINTS',
            105:'Syntax error in RBW value',
            106:'Sweep point required in freq table',
            107:'Programmed points table empty',
            108:'Invalid prog. points table',
            109:'Out of range in SWEEP POINTS',
            110:'Out of range in real part',
            111:'Out of range in imag part',
            120:'String buffer full',
            121:'Line number syntax error',
            140:'No ASP program in memory',
            141:'Not continuable',
            142:'WAIT syntax error',
            143:'GOTO syntax error',
            144:'IF THEN syntax error',
            145:'FOR NEXT syntax error',
            146:'GOSUB RETURN syntax error',
            147:'DISP syntax error',
            148:'OUTPUT syntax error',
            149:'INPUT syntax error',
            150:'Line number not found',
            151:'END statement not found',
            160:'HP-IB char string too long',
            161:'Plot allowed X-A&B/A-B/SMITH/POLAR',
            162:"Can't print data on this display",
            180:'Overload on R1 input',
            181:'Overload on T1 input',
            182:'Overload on R2 input',
            183:'Overload on T2 input',
            184:'Fractional N loop + unlocked',
            185:'Fractional N loop - unlocked',
            190:'Mass storage hardware failure',
            191:'Record not found',
            192:'Read data error',
            193:'Write protected',
            194:'Disc not in drive',
            195:'FORMAT failed',
            196:'Directory overflow',
            197:'Mass storage medium overflow',
            198:'Duplicate file name',
            199:'Improper file type',
            200:'File name is undefined',
            201:'Protect code violation',
            202:'Invalid mass storage volume label',
            203:'RECOVER failed',
            204:'Record address error',
            205:'Improper file name.A->Z & _ only)',
            206:'Improper data exist',
            207:'Get failed',
            220:'Allowed only in IMPEDANCE/S11/S22',
            221:'Change parameter to Z-theta/Y-theta',
            222:'Change sweep to frequency',
            223:'N must be >=3 in ana. range',
            224:'Allowed only in IMPEDANCE',
            225:'Negative data exists in A_REG',
            226:"Can't calculate EQV parameter",
            227:'Allowed only in Z-theta/Y-theta/R-X/G-B',
            228:'Integer overflow',
            229:'Divide by zero error',
            230:'Real math overflow',
            231:'Real math underflow',
            232:'Value range error',
            233:'Invalid SIN/COS argument',
            234:'Invalid LOG/LN argument',
            235:'Invalid SQR argument',
            237:'HP 4195A service function error',
            238:'HP 4195A service function error',
            239:'HP 4195A service function error',
            240:'HP 4195A service function error',
            241:'HP 4195A service function error'
        }
        
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
    status_Error = False        ## Contains 0 or string with error message
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
            self.resetDev()
    def Disconnect(self):
        self.visa_ResourceManager.close
        self.status_Connected = False
        self.GPIBO_Address    = ()
        self.DeviceObj        = ()
    def queryDev(self, command):
        answer = None
        if self.status_Connected:
            answer = self.DeviceObj.query(command) # .query_ascii_values() for A,B & X
        return answer
    def sendDev(self, command):  
        if self.status_Connected:
            self.DeviceObj.write(command) 
            return self.checkStatus()
        else:
            print "Dev not Connected"
            return 0
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
    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False     
    def checkStatus(self):
        statusByte = format(int(self.getStatusByte()), '08b')
        print statusByte
        if statusByte[2] == '0':
            self.status_Error = False
            return True
        try:
            self.status_Error = self.ErrorMessages[int(self.getError())]
        except:
            self.status_Error = 'Unknown Error'
        self.clearStatusByte()
        print self.status_Error
        return False

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    Get & Set System Stuff
    """
    def resetDev(self):
        return self.sendDev('RST')
    def getStatusByte(self):
        return self.queryDev("STB?")
    def maskStatusByte(self, value):
        return self.DeviceObj.write("RQS=" + str(value))
    def clearStatusByte(self):
        return self.DeviceObj.write("CLS")
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
        if self.isFloat(value):
            return self.sendDev(name.upper() + "=" + str(value))
        return 0
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """
    General Functions
    
    """
    def setMeasurementMode(self, value):
        self.status_MeasMode = self.getStrCommandValue(self.MeasurementModes, value)
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
        return self.setRegister('DFREQ' , value)
    def setAngleMode(self, mode):
        self.status_CurrentAngle = mode
        return self.sendDev(mode.upper())
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
        print 'AA'
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
        if self.status_MeasMode == 'S11' or self.status_MeasMode == 'S22':
            return self.sendCommand('SPI', value, self.SModeFormats)
        else:
            return self.sendCommand('GPP', value, self.SModeFormats)
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""    
    """
    Calibration Functions
    """
    def setCharacteristicImpedance(self, value):
        if self.isFloat(value):
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
        if self.isFloat(conductance) and self.isFloat(capacitance):
            return self.sendDev('OPNSTD=' + str(conductance) + ',' + str(capacitance))
        return 0
    def setLoadCalStd(self, resistance, inductance):
        if self.isFloat(resistance) and self.isFloat(inductance):
            return self.sendDev('LDSTD=' + str(resistance) + ',' + str(inductance))
        return 0
    def setShortCalStd(self, conductance, capacitance):
        if self.isFloat(conductance) and self.isFloat(capacitance):            
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
        return self.setRegister('PE' + port, value)
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
        if self.status_MeasMode=="SPECTRUM":
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
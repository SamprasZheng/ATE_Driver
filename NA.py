import pyvisa as visa
import time
import pandas as pd
import os
import numpy as np

class Dryrun():
    def write(self, cmd):
        time.sleep(0.001)
    def read(self):
        time.sleep(0.001)
        return "0.0"

class p5026a:
    visa_addr = ""
    def __init__(self, visa_addr = None, dryrun = False) -> None:
        if dryrun:
            self.VNA = Dryrun()
        elif visa_addr == None:
            rm = visa.ResourceManager()
            rm.list_resources()
            self.VNA = rm.open_resource(self.visa_addr)
            self.VNA.timeout = 5000
        else:
            rm = visa.ResourceManager()
            rm.list_resources()
            self.VNA = rm.open_resource(visa_addr)
            self.VNA.timeout = 5000

    def MeasurementForm(self, point = 201):
        # Reset channel 1&2
        self.VNA.write(":CALC1:PAR:DEL:ALL")
        # Set power sweep
        self.VNA.write(":SENS1:SWE:TYPE LIN")
        self.VNA.write(":SENS1:FREQ:STAR 27E9")
        self.VNA.write(":SENS1:FREQ:STOP 31E9")
        self.VNA.write(":SOUR1:POW1 0")
        self.VNA.write(":SENS1:SWE:POINts "+ str(point))
        # Define measurements
        self.VNA.write(":CALC1:MEAS1:DEF 'S11'")
        self.VNA.write(":CALC1:MEAS2:DEF 'S21'")
        self.VNA.write(":CALC1:MEAS3:DEF 'S21'")
        self.VNA.write(":CALC1:MEAS4:DEF 'S12'")
        self.VNA.write(":CALC1:MEAS5:DEF 'S12'")
        self.VNA.write(":CALC1:MEAS6:DEF 'S22'")
        self.VNA.write(":CALC1:MEAS3:FORM PHAS")
        self.VNA.write(":CALC1:MEAS5:FORM PHAS")
        # Turn on display
        self.VNA.write(":DISP:WIND2 1")
        self.VNA.write(":DISP:WIND3 1")
        self.VNA.write(":DISP:WIND4 1")
        # Feed signal
        self.VNA.write(":DISP:WIND1:TRAC1:FEED:MNUM 1")
        self.VNA.write(":DISP:WIND2:TRAC2:FEED:MNUM 2")
        self.VNA.write(":DISP:WIND3:TRAC3:FEED:MNUM 3")
        self.VNA.write(":DISP:WIND4:TRAC4:FEED:MNUM 4")
        self.VNA.write(":SENS1:SWE:MODE CONT")

    def MarkerSet(self):
        self.VNA.write(":CALC:MEAS1:MARK1 ON")
        self.VNA.write(":CALC:MEAS2:MARK1 ON")
        self.VNA.write(":CALC:MEAS3:MARK1 ON")
        self.VNA.write(":CALC:MEAS4:MARK1 ON")
        self.VNA.write(":CALC:MEAS5:MARK1 ON")
        self.VNA.write(":CALC:MEAS6:MARK1 ON")
        self.VNA.write(":CALC:MEAS1:MARK1:X 28Ghz")
        self.VNA.write(":CALC:MEAS2:MARK1:X 28Ghz")
        self.VNA.write(":CALC:MEAS3:MARK1:X 28Ghz")
        self.VNA.write(":CALC:MEAS4:MARK1:X 28Ghz")
        self.VNA.write(":CALC:MEAS5:MARK1:X 28Ghz")
        self.VNA.write(":CALC:MEAS6:MARK1:X 28Ghz")

        self.VNA.write(":CALC:MEAS1:MARK2 ON")
        self.VNA.write(":CALC:MEAS2:MARK2 ON")
        self.VNA.write(":CALC:MEAS3:MARK2 ON")
        self.VNA.write(":CALC:MEAS4:MARK2 ON")
        self.VNA.write(":CALC:MEAS5:MARK2 ON")
        self.VNA.write(":CALC:MEAS6:MARK2 ON")
        self.VNA.write(":CALC:MEAS1:MARK2:X 29Ghz")
        self.VNA.write(":CALC:MEAS2:MARK2:X 29Ghz")
        self.VNA.write(":CALC:MEAS3:MARK2:X 29Ghz")
        self.VNA.write(":CALC:MEAS4:MARK2:X 29Ghz")
        self.VNA.write(":CALC:MEAS5:MARK2:X 29Ghz")
        self.VNA.write(":CALC:MEAS6:MARK2:X 29Ghz")

        self.VNA.write(":CALC:MEAS1:MARK3 ON")
        self.VNA.write(":CALC:MEAS2:MARK3 ON")
        self.VNA.write(":CALC:MEAS3:MARK3 ON")
        self.VNA.write(":CALC:MEAS4:MARK3 ON")
        self.VNA.write(":CALC:MEAS5:MARK3 ON")
        self.VNA.write(":CALC:MEAS6:MARK3 ON")
        self.VNA.write(":CALC:MEAS1:MARK3:X 30Ghz")
        self.VNA.write(":CALC:MEAS2:MARK3:X 30Ghz")
        self.VNA.write(":CALC:MEAS3:MARK3:X 30Ghz")
        self.VNA.write(":CALC:MEAS4:MARK3:X 30Ghz")
        self.VNA.write(":CALC:MEAS5:MARK3:X 30Ghz")
        self.VNA.write(":CALC:MEAS6:MARK3:X 30Ghz")
        
    def MarkerRead(self):
        self.VNA.write(":CALC:MEAS1:MARK1:Y?")
        mark1_1 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS1:MARK2:Y?")
        mark1_2 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS1:MARK3:Y?")
        mark1_3 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS2:MARK1:Y?")
        mark2_1 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS2:MARK2:Y?")
        mark2_2 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS2:MARK3:Y?")
        mark2_3 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS3:MARK1:Y?")
        mark3_1 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS3:MARK2:Y?")
        mark3_2 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS3:MARK3:Y?")
        mark3_3 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS4:MARK1:Y?")
        mark4_1 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS4:MARK2:Y?")
        mark4_2 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS4:MARK3:Y?")
        mark4_3 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS5:MARK1:Y?")
        mark5_1 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS5:MARK2:Y?")
        mark5_2 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS5:MARK3:Y?")
        mark5_3 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS6:MARK1:Y?")
        mark6_1 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS6:MARK2:Y?")
        mark6_2 = float(self.VNA.read().split(',')[0])
        self.VNA.write(":CALC:MEAS6:MARK3:Y?")
        mark6_3 = float(self.VNA.read().split(',')[0])
        return \
            [mark1_1, mark1_2, mark1_3], \
            [mark2_1, mark2_2, mark2_3], \
            [mark3_1, mark3_2, mark3_3], \
            [mark4_1, mark4_2, mark4_3], \
            [mark5_1, mark5_2, mark5_3], \
            [mark6_1, mark6_2, mark6_3], \

    def Getdata(self):
        self.VNA.write("SENS1:SWE:MODE CONT")
        time.sleep(0.5)
        # Get x data
        self.VNA.write(":CALC1:MEAS2:X?")
        data = self.VNA.read()
        Xaxix=[float(d) for d in data.split(',')]
        datapoint = len(Xaxix)
        # Get measurement 1
        self.VNA.write(":CALC1:MEAS1:DATA:FDAT?")
        data = self.VNA.read()
        Trace1=[float(d) for d in data.split(',')]
        # Get measurement 2
        self.VNA.write(":CALC1:MEAS2:DATA:FDAT?")
        data = self.VNA.read()
        Trace2=[float(d) for d in data.split(',')]
        # Get measurement 3
        self.VNA.write(":CALC1:MEAS3:DATA:FDAT?")
        data = self.VNA.read()
        Trace3=[float(d) for d in data.split(',')]
        # Get measurement 4
        self.VNA.write(":CALC1:MEAS4:DATA:FDAT?")
        data = self.VNA.read()
        Trace4=[float(d) for d in data.split(',')]
        # Get measurement 5
        self.VNA.write(":CALC1:MEAS5:DATA:FDAT?")
        data = self.VNA.read()
        Trace5=[float(d) for d in data.split(',')]
        # Get measurement 6
        self.VNA.write(":CALC1:MEAS6:DATA:FDAT?")
        data = self.VNA.read()
        Trace6=[float(d) for d in data.split(',')]
        return(Xaxix,Trace1,Trace2,Trace3,Trace4,Trace5,Trace6)
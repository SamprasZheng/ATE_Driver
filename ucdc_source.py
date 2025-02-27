#CoraZ7
#GPIO Usage 13 pins
# 4pins 3.3V 9pins 1.8V
# 3 Output 10 Input
# from JTAGDriver2 import JTAGDriver
# from ToolDriver import ToolClass
# bit_stream_path = './Cora_Z7_measurement_tool_10.bit'
# device_name = 'xc7z010_1'

# Dev = JTAGDriver(bit_stream_path, device_name, debug=False)

# Dev.jtag_connect()
# Dev.jtag_program()

# Tool = ToolClass(Dev)
# Tool.parse_usr_access_timestamp()

##### GPIO
UCDC_PIN_LIST={
    #Pin Name           CoraZ7 pin     Type
    'RX_PLL_MUXOUT':    0, #JA.P[1]    O
    'I2C_UCDC_RSTB':    1, #JA.N[1]    I
    'EN_VDD_-5V_UCDC': 2, #JA.P[2]    I
    'PG_DVDD_3V3_UCDC': 3, #JA.N[2]    O
    'EN_VDD_4V_UCDC':  4, #JA.P[3]    I 
    'EN_RX_PLL':        5, #JA.N[3]    I
    'EN_FE':            6, #JA.P[4]    I 
    'EN_DVDD_3V3_UCDC': 7, #JA.N[4]    I
    'EN_DVDD_5V_UCDC':  8, #JB.P[1]    I
    'EN_VDD_3V3_UCDC':  9, #JB.N[1]    I
    'EN_TX_PLL':       10, #JB.P[2]    I
    'BBF_SEL':         11, #JB.N[2]    I
    'TX_PLL_MUXOUT':   12  #JB.P[3]    O
    }
##### Current Sensor (PAC1934T-I/JQ)
# key : MEASURE_ITEM => 'VBUS' 'VSENSE' 'VBUS_AVG' 'VSENSE_AVG'
# value : Reg Base Address (ch1)
#Example 'VBUS' : Ch1=0x70 => Ch2=0x07+0x01=0x08 =>Ch3=0x07+0x02=0x09
DIC_CS_BASE_ADDRESS={
    'VBUS':0x07,
    'VSENSE':0x0B,
    'VBUS_AVG':0x0F,
    'VSENSE_AVG':0x13,
    }

#key : Name of Curent Sensor
#value : [MUX_CHANNEL,SLAVE Address,DATA]
DIC_CS_CONFIG={
    'UCDC_PWR_CS':['FE',0x10,[0x00,0x00,0xF0]],
    'FE_PWR_CS':['FE',0x18,[0x00,0x10,0xF0]],
    'TX_DC_CS':[0x01,0x10,[0x00,0x60,0xF0]],
    'TX_UC_CS':[0x01,0x18,[0x00,0x20,0xF0]],
    'TX_PLL_CS':[0x02,0x10,[0x00,0x20,0xF0]],
    'RX_PLL_CS':[0x04,0x10,[0x00,0x20,0xF0]],
    'RX_UC_CS':[0x08,0x10,[0x00,0x00,0xF0]],
    'RX_DC_CS':[0x08,0x18,[0x00,0x00,0xF0]],
    }

def cora_init(Tool=None):
    # Define GPIO Output Pins
    Tool.gpio_init_w_pin(device = 'gpio_3v3', w_pin = [1,2,4,5,6,7,8,9,10,11]) 
    # Set all output pins to 0 
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {1:0,2:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0})

    # Tool.gpio_read(device = 'gpio_3v3')#default : 1111111111000000001001
    ##### SPI
    #SPI_0
    #MAX529*3 => CPOL=0 CPHA=0 => 8bit address + 8bit data => 16bit
    #HMC960LP4E => CPOL=0 CPHA=0 => 24 bit data + 5bit address + '110' =>32bit
    #SPI_1
    #ADF4372*2 => CPOL=0 CPHA=0 => 16 bit address + 8bit data =>24bit
    #Initial Cora_Z7 SPI : CSB_IDLE_STATE sets to low for avoiding conducting the diode. 
    Tool.SPI_init(device = 'SPI_0', SPI_CSB_IDLE_STATE = 0, SPI_CSB_MASK = 0, SPI_CPOL = 0, SPI_CPHA = 0, SPI_SDIO_mode = 0) 
    Tool.SPI_init(device = 'SPI_1', SPI_CSB_IDLE_STATE = 0, SPI_CSB_MASK = 0, SPI_CPOL = 0, SPI_CPHA = 0, SPI_SDIO_mode = 0)

# TX_PLL_SCLK       J4.IO13 *
# TX_PLL_CSB        J4.IO12 **
# TX_PLL_MOSI       J4.IO34

# RX_PLL_SCLK       J4.IO13 *
# RX_PLL_CSB        J4.IO12 **
# RX_PLL_MOSI       J4.IO35

# TX_UCDC_VG_SCLK   J4.IO11 ***
# TX_UCDC_VG_CSB    J4.IO10 ****
# TX_UCDC_VG_MOSI   J5.IO30

# RX_UCDC_VG_SCLK   J4.IO11 ***
# RX_UCDC_VG_CSB    J4.IO10 ****
# RX_UCDC_VG_MOSI   J5.IO31

# TRX_UCDC_IF_SCLK  J4.IO11 ***
# TRX_UCDC_IF_CSB   J4.IO10 ****
# TRX_UCDC_IF_MOSI  J5.IO32

# RX_DC_PGA_SCLK    J4.IO11 ***
# RX_DC_PGA_CSB     J4.IO10 ****
# RX_DC_PGA_MOSI    J5.IO33


# read pin

# Tool.gpio_read(device = 'gpio_3v3')
import struct
import pandas as pd
import time
# import pyvisa as visa
import time
import math


def PLL_CONFIG(PLL_Name,df, Tool=None):
    #PLL_Name : 'TX_PLL' or 'RX_PLL'
    #df : PLL_Reg_Map
    for i in range(71):
        #ADF4372 Programming Sequence
        index=70-i
        if index==7:
            print(f'ADF4372 programs successfully')
            return 
        else:
            w_data_PLL=[]
            test=[]
            temp=int(df.at[index,'Reg'],16)
            w_data_PLL.append(temp>>8)
            w_data_PLL.append(temp&((1<<8)-1))        
            w_data_PLL.append(int(df.at[index,'Data'],16))
            
            if PLL_Name=='TX_PLL':
                
                Tool.SPI_program(device = ['SPI_1'], w_data = [[w_data_PLL,[0x00,0x00,0x18],[0x00,0x00,0x00],[0x00,0x00,0x00]]], r_bytes = [0])
#                 print(f'TX_PLL Reg:{hex(temp)} write successfully')
            elif PLL_Name=='RX_PLL':
                
                Tool.SPI_program(device = ['SPI_1'], w_data = [[[0x00,0x00,0x18],w_data_PLL,[0x00,0x00,0x00],[0x00,0x00,0x00]]], r_bytes = [0])
#                 print(f'RX_PLL Reg:{hex(temp)} write successfully')
                
            else:
                print('PLL Name Error')
                return

def PAC1934_CS_CONFIG(CS_NAME, Tool=None):
    if DIC_CS_CONFIG[CS_NAME][0]=='FE':
        #REFRESH Command 
        Tool.i2c_write(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [], write_data = [0x00])
        #Config Command
        Tool.i2c_write(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x01], write_data = [DIC_CS_CONFIG[CS_NAME][2][0]])
        Tool.i2c_write(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x1C], write_data = [DIC_CS_CONFIG[CS_NAME][2][1]])
        Tool.i2c_write(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x1D], write_data = [DIC_CS_CONFIG[CS_NAME][2][2]])
        #REFRESH Command 
        Tool.i2c_write(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [], write_data = [0x00])
        print(f'{CS_NAME} is initialized')
    else:
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [DIC_CS_CONFIG[CS_NAME][0]])
        #REFRESH Command 
        Tool.i2c_write(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [], write_data = [0x00])
        #Config Command
        Tool.i2c_write(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x01], write_data = [DIC_CS_CONFIG[CS_NAME][2][0]])
        Tool.i2c_write(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x1C], write_data = [DIC_CS_CONFIG[CS_NAME][2][1]])
        Tool.i2c_write(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x1D], write_data = [DIC_CS_CONFIG[CS_NAME][2][2]])
       
#         print(f'{CS_NAME} is initialized')
#         READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x01], byte_len = 1)
#         print("0x01 data: "+str(hex(READ_DATA[0])))
#         READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x1C], byte_len = 1)
#         print("0x1C data: "+str(hex(READ_DATA[0])))
#         READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [0x1D], byte_len = 1)
#         print("0x1D data: "+str(hex(READ_DATA[0])))
         #REFRESH Command 
        Tool.i2c_write(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [], write_data = [0x00])
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])

def PAC1934_CS_MONITOR(CS_NAME,SUPPLY,MEASURE_ITEM, Tool=None):
      
    if DIC_CS_CONFIG[CS_NAME][0]=='FE':
        #REFRESH Command 
        Tool.i2c_write(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [], write_data = [0x00])
        #Read 2 bytes from specify reg
        
        READ_DATA=Tool.i2c_read(device = 'iic_1', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [DIC_CS_BASE_ADDRESS[MEASURE_ITEM]+DIC_CS_MONITOR[SUPPLY][0]], byte_len = 2)
    else:
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [DIC_CS_CONFIG[CS_NAME][0]])
        #REFRESH Command 
        
        Tool.i2c_write(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [], write_data = [0x00])
        #Read 2 bytes from specify reg
#         print("dic_cs config:"+ str(hex(DIC_CS_CONFIG[CS_NAME][1])))
#         print("DIC_CS_MONITOR[SUPPLY][0]]:"+ str(DIC_CS_MONITOR[SUPPLY][0]))
#         print("[DIC_CS_BASE_ADDRESS[MEASURE_ITEM]:"+ str([DIC_CS_BASE_ADDRESS[MEASURE_ITEM]]))

#         print("reg_ptr:"+ str([DIC_CS_BASE_ADDRESS[MEASURE_ITEM]+DIC_CS_MONITOR[SUPPLY][0]]))
        
        READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = DIC_CS_CONFIG[CS_NAME][1], reg_ptr = [DIC_CS_BASE_ADDRESS[MEASURE_ITEM]+DIC_CS_MONITOR[SUPPLY][0]], byte_len = 2)
        #Deselect the MUX Channel
#         print("read data: "+str(READ_DATA))
#         print("data0: "+str(READ_DATA[0]))
#         print("data1: "+str(READ_DATA[1]))
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])    
    
    if MEASURE_ITEM=='VBUS' or MEASURE_ITEM=='VBUS_AVG':
        #unsigned 16bit binary output
#         print(READ_DATA[1])
#         print(READ_DATA[0])
        (VBUS,)=struct.unpack("H",struct.pack("<BB",READ_DATA[1],READ_DATA[0]))
        #LSB = 0.488mV
#         print(VBUS)
        VBUS=round(VBUS*0.000488,3)
        if MEASURE_ITEM=='VBUS':
            print(f'{SUPPLY} Voltage:{VBUS}V')
        else:
            print(f'{SUPPLY} AVG Voltage:{VBUS}V')
        return VBUS
    else:
        #signed 16bit binary output
        (VSENSE,)=struct.unpack("h",struct.pack("<BB",READ_DATA[1],READ_DATA[0]))
        #LSB = 0.003mV
        VSENSE=VSENSE*0.003
#         print(f'VSENSE:{VSENSE}mV')
        RSNS=DIC_CS_MONITOR[SUPPLY][1]
#         print(f'{RSNS} Ohms')
        IDD=round(VSENSE/RSNS,3)
        if MEASURE_ITEM=='VSENSE':
            print(f'{SUPPLY} Current:{IDD}mA')
        else:
            print(f'{SUPPLY} AVG Current:{IDD}mA')
        return IDD

def PAC1934_CS_PWR_AVG(CS_NAME,SUPPLY,Tool=None):
    Temp_VBUS=PAC1934_CS_MONITOR(CS_NAME,SUPPLY,'VBUS_AVG',Tool=Tool)
    Temp_IDD=PAC1934_CS_MONITOR(CS_NAME,SUPPLY,'VSENSE_AVG',Tool=Tool)
    print(f'{SUPPLY} AVG PWR:{round(abs(Temp_VBUS*Temp_IDD),3)}mW')
    return abs(Temp_VBUS*Temp_IDD)   

def RX_DC_Bias(Status):
    if Status=='ON':
        SPI_0_CONFIG('RX_DC_LNA_VG',-0.41,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_LNA_VD','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_LNA_VD','VSENSE_AVG')
        SPI_0_CONFIG('RX_DC_VG1',-0.51,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD1','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD1','VSENSE_AVG')
        SPI_0_CONFIG('RX_DC_VG2',-0.63,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD2','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD2','VSENSE_AVG')
        SPI_0_CONFIG('RX_DC_VG3',-0.44,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD3','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD3','VSENSE_AVG')
        print('RX_DC turns on')
    else:
        SPI_0_CONFIG('RX_DC_LNA_VG',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_LNA_VD','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_LNA_VD','VSENSE_AVG')
        SPI_0_CONFIG('RX_DC_VG3',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD3','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD3','VSENSE_AVG')
        SPI_0_CONFIG('RX_DC_VG2',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD2','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD2','VSENSE_AVG')
        SPI_0_CONFIG('RX_DC_VG1',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD1','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD1','VSENSE_AVG')
        print('RX_DC turns off')

####RX_DC Current & Vbus
def RX_DC_SNS():
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD1','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD1','VSENSE_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD2','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD2','VSENSE_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD3','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_VD3','VSENSE_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_LNA_VD','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_DC_CS','RX_DC_LNA_VD','VSENSE_AVG')        
        
####RX_UC Bias Setting        
def RX_UC_Bias(Status):

    if Status=='ON':
        #RX_UC LNA Bias Setting
        SPI_0_CONFIG('RX_UC_LNA_VG',-0.41,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_LNA_VD','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_LNA_VD','VSENSE_AVG')
        SPI_0_CONFIG('RX_UC_VG1',-0.62,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD1','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD1','VSENSE_AVG')
        SPI_0_CONFIG('RX_UC_VG2',-0.47,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD2','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD2','VSENSE_AVG')
        SPI_0_CONFIG('RX_UC_VG3',-0.39,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD3','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD3','VSENSE_AVG')
        print('RX_UC turns on')
    else:
        SPI_0_CONFIG('RX_UC_LNA_VG',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_LNA_VD','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_LNA_VD','VSENSE_AVG')
        SPI_0_CONFIG('RX_UC_VG3',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD3','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD3','VSENSE_AVG')
        SPI_0_CONFIG('RX_UC_VG2',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD2','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD2','VSENSE_AVG')        
        SPI_0_CONFIG('RX_UC_VG1',-1,DIC_DAC)
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD1','VBUS_AVG')
        PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD1','VSENSE_AVG')        
        print('RX_UC turns off')
####RX_UC Current & Vbus
def RX_UC_SNS():
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD1','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD1','VSENSE_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD2','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD2','VSENSE_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD3','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_VD3','VSENSE_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_LNA_VD','VBUS_AVG')
    PAC1934_CS_MONITOR('RX_UC_CS','RX_UC_LNA_VD','VSENSE_AVG')        
   
#### SET all DAC channels to -1V 
def DAC_BIAS_OFF(Tool=None):
    for i in ['TX_DC_LNA_VG','TX_UC_VG3','TX_UC_VG2','TX_UC_VG1','RX_DC_LNA_VG','RX_DC_VG3','RX_DC_VG2','RX_DC_VG1','RX_UC_LNA_VG','RX_UC_VG3','RX_UC_VG2','RX_UC_VG1']:
        SPI_0_CONFIG(i,-1,DIC_DAC,Tool=Tool)

def DAC_IF_OFF(Tool=None):
    for i in ['TX_IF_IN','TX_IF_IP','TX_IF_QP','TX_IF_QN','RX_IF_IN','RX_IF_IP','RX_IF_QP','RX_IF_QN']:
        SPI_0_CONFIG(i,0,DIC_DAC,Tool=Tool)
#### Initial all the CS 
def UCDC_CS_INITIAL():
    PAC1934_CS_CONFIG('TX_DC_CS')
    PAC1934_CS_CONFIG('TX_UC_CS')
    PAC1934_CS_CONFIG('RX_UC_CS')
    PAC1934_CS_CONFIG('RX_DC_CS')
    PAC1934_CS_CONFIG('TX_PLL_CS')
    PAC1934_CS_CONFIG('RX_PLL_CS')
    PAC1934_CS_CONFIG('UCDC_PWR_CS')
    PAC1934_CS_CONFIG('FE_PWR_CS')
##### Mode operation
#Nomal mode => Enable TX_UC / RX_DC / ADC_SW:0,DAC_SW:0 /BBF_SEL:0 or 1
#TX mode
#RX mode
#TX build in test mode => Enable TX_UC / TX_DC / ADC_SW:1,DAC_SW:0 /BBF_SEL:0 or 1/TX_CAL_SW=0 or 1
#RX build in test mode => Enable RX_DC /RX_UC / ADC_SW:0,DAC_SW:1/RX_CAL_SW=0 or 1
#Factory test mode => Enable TX_DC/RX_UC/ADC_SW:1,DAC_SW:1/BBF_SEL:0 or 1

#Dictionary to save setting in different operation mode
# Key: Mode Name
# Value : [[DAC_SW,ADC_SW],[TX_CAL_SW,RX_CAL_SW],[TX_UC,TX_DC,RX_DC,RX_UC],[TX_PLL,RX_PLL]]
DIC_Mode={'NORMAL':[[0,0],[0,0],[1,0,1,0],[1,1]],
          'TX':[[0,0],[0,0],[1,0,0,0],[1,0]],
          'RX':[[0,0],[0,0],[0,0,1,0],[0,1]],
          'TX_BIT':[[0,1],[0,0],[1,1,0,0],[1,0]],
          'RX_BIT':[[1,0],[0,0],[0,0,1,1],[0,1]],
          'FACTORY_TEST':[[1,1],[0,1],[0,1,0,1],[1,1]]         
         }
#key : Name of supply
#value: [CS_CHANNEL,RSNS]
#CS_CHANNEL: Ch1:0 Ch2:1 Ch3:2 Ch4:3
#RSNS: Sense resistor in Ohms
DIC_CS_MONITOR={
    #UCDC_PWR CS
    'VDD_5V_UCDC':[0,0.1],
    'VDD_-5V_UCDC':[1,'None'],
    'VDD_3V3_UCDC':[2,0.05],
    'VDD_4V_UCDC':[3,0.05],
    #FE_PWR CS
    'VDD_3V3_FE_1':[0,0.01],
    'VDD_3V3_FE_0':[1,0.01],
    'VDD_5V_FE':[2,0.01],
    #TX_DC CS
    'TX_DC_VD':[0,0.2],
    'TX_DC_LNA_VD':[3,0.2],
    #TX_UC CS
    'TX_UC_VD1':[0,0.2],
    'TX_UC_VD3':[1,0.2],
    'TX_UC_VD2':[3,0.2],
    #TX_PLL CS
    'TX_PLL_AMP_5V':[0,0.1],
    'TX_PLL_3V3':[1,0.1],
    'TX_PLL_5V':[3,0.1],
    #RX_PLL CS
    'RX_PLL_5V':[0,0.1],
    'RX_PLL_3V3':[1,0.1],
    'RX_PLL_AMP_5V':[3,0.1],
    #RX_UC CS
    'RX_UC_VD1':[0,0.2],
    'RX_UC_VD3':[1,0.2],
    'RX_UC_LNA_VD':[2,0.2],
    'RX_UC_VD2':[3,0.2],
    #RX_DC CS
    'RX_DC_VD1':[0,2.7],
    'RX_DC_LNA_VD':[1,0.2],
    'RX_DC_VD3':[2,0.2],
    'RX_DC_VD2':[3,1],
    }  
##### SPI_0 Command (Only for Coraz7)
# Tool.SPI_program(device = ['SPI_0', 'SPI_1'], w_data = w_data, r_bytes = [1, 1])
def SPI_0_INITIAL(Tool=None):
    #SPI_0 can control TX_UCDC_VG / RX_UCDC_VG / TRX_UCDC_IF / RX_DC_PGA 
    w_data_TX_UCDC_VG=DAC_BUFF_MODE('TX_UCDC_VG',DIC_DAC)
    w_data_RX_UCDC_VG=DAC_BUFF_MODE('RX_UCDC_VG',DIC_DAC)
    w_data_TRX_UCDC_IF=DAC_BUFF_MODE('TRX_UCDC_IF',DIC_DAC)
    w_data_RX_DC_PGA=RX_DC_PGA_SET(0,1,0b10,0b01)
    w_data_SPI_0=[w_data_TX_UCDC_VG,w_data_RX_UCDC_VG,w_data_TRX_UCDC_IF,w_data_RX_DC_PGA]
    print(f'SPI salves are initialized with :{w_data_SPI_0}')
    Tool.SPI_program(device = ['SPI_0'], w_data = [w_data_SPI_0], r_bytes = [0])
    return w_data_SPI_0
    

def SPI_0_CONFIG(CH_Name,DATA,DIC_DAC, Tool=None):
    #CH_Name : Ex:'TX_UC_VG3'
    #DATA : DACoutput voltage or Gain of PGA
    if CH_Name=='RX_DC_PGA':
        w_data_TX_UCDC_VG=DAC_BUFF_MODE('TX_UCDC_VG',DIC_DAC)
        w_data_RX_UCDC_VG=DAC_BUFF_MODE('RX_UCDC_VG',DIC_DAC)
        w_data_TRX_UCDC_IF=DAC_BUFF_MODE('TRX_UCDC_IF',DIC_DAC)
        w_data_RX_DC_PGA=RX_DC_PGA_GAIN_CTRL(DATA)
        w_data_SPI_0=[w_data_TX_UCDC_VG,w_data_RX_UCDC_VG,w_data_TRX_UCDC_IF,w_data_RX_DC_PGA]
#         print(f'w_data_SPI_0:{w_data_SPI_0}')
        Tool.SPI_program(device = ['SPI_0'], w_data = [w_data_SPI_0], r_bytes = [0])
        return     
    if DIC_DAC[CH_Name][0]=='TX_UCDC_VG':        
        w_data_TX_UCDC_VG=DAC_SET(CH_Name,DATA,DIC_DAC)
        w_data_RX_UCDC_VG=DAC_BUFF_MODE('RX_UCDC_VG',DIC_DAC)
        w_data_TRX_UCDC_IF=DAC_BUFF_MODE('TRX_UCDC_IF',DIC_DAC)
        w_data_RX_DC_PGA=RX_DC_PGA_SET(0,1,0b10,0b01)
        w_data_SPI_0=[w_data_TX_UCDC_VG,w_data_RX_UCDC_VG,w_data_TRX_UCDC_IF,w_data_RX_DC_PGA]
#         print(f'w_data_SPI_0:{w_data_SPI_0}')
        Tool.SPI_program(device = ['SPI_0'], w_data = [w_data_SPI_0], r_bytes = [0])
        return
    elif DIC_DAC[CH_Name][0]=='RX_UCDC_VG':
        w_data_TX_UCDC_VG=DAC_BUFF_MODE('TX_UCDC_VG',DIC_DAC)
        w_data_RX_UCDC_VG=DAC_SET(CH_Name,DATA,DIC_DAC)
        w_data_TRX_UCDC_IF=DAC_BUFF_MODE('TRX_UCDC_IF',DIC_DAC)
        w_data_RX_DC_PGA=RX_DC_PGA_SET(0,1,0b10,0b01)
        w_data_SPI_0=[w_data_TX_UCDC_VG,w_data_RX_UCDC_VG,w_data_TRX_UCDC_IF,w_data_RX_DC_PGA]
#         print(f'w_data_SPI_0:{w_data_SPI_0}')
        Tool.SPI_program(device = ['SPI_0'], w_data = [w_data_SPI_0], r_bytes = [0])
        return
    elif DIC_DAC[CH_Name][0]=='TRX_UCDC_IF':
        w_data_TX_UCDC_VG=DAC_BUFF_MODE('TX_UCDC_VG',DIC_DAC)
        w_data_RX_UCDC_VG=DAC_BUFF_MODE('RX_UCDC_VG',DIC_DAC)
        w_data_TRX_UCDC_IF=DAC_SET(CH_Name,DATA,DIC_DAC)
        w_data_RX_DC_PGA=RX_DC_PGA_SET(0,1,0b10,0b01)
        w_data_SPI_0=[w_data_TX_UCDC_VG,w_data_RX_UCDC_VG,w_data_TRX_UCDC_IF,w_data_RX_DC_PGA]
#         print(f'w_data_SPI_0:{w_data_SPI_0}')
        Tool.SPI_program(device = ['SPI_0'], w_data = [w_data_SPI_0], r_bytes = [0])
        return

#### Initial all the CS 
def UCDC_CS_INITIAL(Tool=None):
    PAC1934_CS_CONFIG('TX_DC_CS',Tool=Tool)
    PAC1934_CS_CONFIG('TX_UC_CS',Tool=Tool)
    PAC1934_CS_CONFIG('RX_UC_CS',Tool=Tool)
    PAC1934_CS_CONFIG('RX_DC_CS',Tool=Tool)
    PAC1934_CS_CONFIG('TX_PLL_CS',Tool=Tool)
    PAC1934_CS_CONFIG('RX_PLL_CS',Tool=Tool)
    PAC1934_CS_CONFIG('UCDC_PWR_CS',Tool=Tool)
    PAC1934_CS_CONFIG('FE_PWR_CS',Tool=Tool)
#####DAC MAX529 funciton
##### DAC (MAX529)
DIC_DAC={
    #'Name':[DAC_Name,Reg,Target voltage,Target current]    
    'TX_DC_LNA_VG':['TX_UCDC_VG',0x01,-0.46,90],
    'TX_UC_VG2':['TX_UCDC_VG',0x02,-1,90],
    'TX_UC_VG3':['TX_UCDC_VG',0x04,-1,160],
    'TX_UC_VG1':['TX_UCDC_VG',0x08,-1,160],
    'TX_UC_VG_LNA':['TX_UCDC_VG_LNA',0x08,-1,90],
    
    'RX_DC_VG1':['RX_UCDC_VG',0x01,-1,7.5],
    'RX_DC_LNA_VG':['RX_UCDC_VG',0x02,-0.46,90],
    'RX_DC_VG2':['RX_UCDC_VG',0x04,-1,30],
    'RX_DC_VG3':['RX_UCDC_VG',0x08,-1,90],
    'RX_UC_LNA_VG':['RX_UCDC_VG',0x10,-0.41,90],
    'RX_UC_VG2':['RX_UCDC_VG',0x20,-1,150],
    'RX_UC_VG1':['RX_UCDC_VG',0x40,-1,90],
    'RX_UC_VG3':['RX_UCDC_VG',0x80,-1,140],
    
    #'Name':[DAC Name,Reg,Target voltage]
    'TX_IF_IN':['TRX_UCDC_IF',0x01,0],
    'TX_IF_IP':['TRX_UCDC_IF',0x02,0],
    'TX_IF_QP':['TRX_UCDC_IF',0x04,0],
    'TX_IF_QN':['TRX_UCDC_IF',0x08,0],
    'RX_IF_IN':['TRX_UCDC_IF',0x10,0],
    'RX_IF_IP':['TRX_UCDC_IF',0x20,0],
    'RX_IF_QP':['TRX_UCDC_IF',0x40,0],
    'RX_IF_QN':['TRX_UCDC_IF',0x80,0],
    
    #'Name':[DAC Name,BUFF_MODE_Reg,REFH,REFL]
    'TX_UCDC_VG':[0xB8,0,-1],
    'RX_UCDC_VG':[0xBF,0,-1],
    'TRX_UCDC_IF':[0xBF,0.5,-0.5],    
    }  
def DAC_BUFF_MODE(DAC_Name,DIC_DAC):
    #Extend to 32 bit for Coraz7 programming
    return [0x00,DIC_DAC[DAC_Name][0],0x00,DIC_DAC[DAC_Name][0]]
#     return [0x00,DIC_DAC[DAC_Name][0]]

def DAC_SET(CH_Name,VDAC,DIC_DAC):
    # CH_Name :'TX_DC_LNA_VG' for example
    # VDAC : Target DAC output voltage
    REFH=DIC_DAC[DIC_DAC[CH_Name][0]][1]
    REFL=DIC_DAC[DIC_DAC[CH_Name][0]][2]
    DATA=VDAC_CONV(VDAC,REFH,REFL)
    print(DATA)
    if DATA==None:
        print(f'Out of range! {CH_Name} sets to {REFL}V')
        return [DIC_DAC[CH_Name][1],0x00,DIC_DAC[CH_Name][1],0x00]
    #Extend to 32 bit for Coraz7 programming
    print(f'{CH_Name}:{VDAC}V')
    return [DIC_DAC[CH_Name][1],DATA,DIC_DAC[CH_Name][1],DATA]
#     return [DIC_DAC[CH_Name][1],DATA]

def VDAC_CONV(VDAC,REFH,REFL):
    #VDAC converts to bit stream
    if VDAC<REFL or VDAC>=(REFH-0.1):
#         print('VDAC is out of range')
        return 
    else:        
        N=(VDAC-REFL)*256/(REFH-REFL)
        N=round(N)
#         print(N & ((1<<8)-1))
        return N & ((1<<8)-1)
#####RX_DC_PGA HMC960 funciton
def RX_DC_PGA_REG(data,reg):
    #RX_DC_PGA Register Format Generation
    if reg<1 or reg>3:
        print('reg invalid')
    else:
        return [0x00,0x00,data,((reg)<<3)+0b110]
    
def RX_DC_PGA_SET(Gain_Deglitch,Rin_Sel,drvr_bias,Opamp_bias):
    #Gain_Deglitch : 0:active (Default) 1:disable
    #Rin_Sel : 0:Rin=200Ohms 1:Rin=50Ohms (Default)
    #drvr_bias : 00:min bias 11:max bias 10:(Default)
    #Opamp_bais : 00:min bias 11:max bias 01:(Default)
    temp=((Gain_Deglitch & 0b1)<<7)+(1<<5)+((Rin_Sel & 0b1)<<4)+((drvr_bias&0b11)<<2)+(Opamp_bias & 0b11)
    return RX_DC_PGA_REG(temp,0x02)

def RX_DC_PGA_GAIN_CTRL(Gain):
    #Gain(dB):Min=0dB Max=40dB LSB=0.5dB 
    if Gain<0 or Gain>40:
        print('Out of range! Gain sets to 0dB')
        return RX_DC_PGA_REG(temp,0x03)
    print(f'The Gain of RX_DC_PGA sets to {Gain}dB')
    Gain=round(Gain/0.5)
    temp=Gain & 0b01111111    
    return RX_DC_PGA_REG(temp,0x03)

#####TX_DC_PS_GPIO Configuration
def TX_DC_PS_GPIO_CONFIG(DAC_SW,TX_CAL_SW,PHASE):
    #Input inspeciton
    if (DAC_SW>>1)!=0:
        print('DAC_SW Input Error')
        return
    elif (TX_CAL_SW>>1)!=0:
        print('TX_CAL_SW Input Error')
        return
    elif PHASE>360 or PHASE<0:
        print('PHASE Input Error')
        return
    
    #####Phase to bit sequence 
    TEMP=round(PHASE/5.625)
    print(f'Setting Phase:{TEMP*5.625} degree')
    # print(bin(TEMP))
    SET_PHASE=[~(TEMP>>2)&((1<<4)-1),TEMP&((1<<2)-1)]
    # print(SET_PHASE)
    # print(bin(SET_PHASE[0]),bin(SET_PHASE[1]))
    PHASE=(SET_PHASE[0]<<2)+SET_PHASE[1]
    # print(bin(PHASE),PHASE)
    #####Concatenate write data
    WRITE_DATA=(DAC_SW<<7)+(TX_CAL_SW<<6)+PHASE
    print(f'Write Data:{bin(WRITE_DATA)}') 
    
    #Select the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x01])
    #Write Data into GPIO
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], write_data = [WRITE_DATA])
    #GPIO Configuration => All output port
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x03], write_data = [0x00])
    #Deselect the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
    

#####TX_DC_PS_GPIO READ Status    
def TX_DC_PS_GPIO_READ(Tool=None):

    #Select the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x01])
    #Read the data from TX_DC_PS_GPIO
    READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], byte_len = 1)
    #Deselect the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])    
    
    #####DAC_SW & TX_CAL_SW Status
    if (READ_DATA[0] & (1<<7))==(1<<7):
        print('T1_DAC is connected to RX_DAC')
    else:
        print('T1_DAC is connected to TX_DAC')
    if (READ_DATA[0] & (1<<6))==(1<<6):
        print('TX_Coupled is selected')
    else:
        print('TX_DC_20GHz is selected')
    #####Phase Status
    TEMP=(READ_DATA[0] & ((1<<6)-1))
    READ_PHASE=[~(TEMP>>2)&((1<<4)-1),TEMP&((1<<2)-1)]
    # print(bin(READ_PHASE[0]),bin(READ_PHASE[1]))
    PHASE=((READ_PHASE[0]<<2)+READ_PHASE[1])*5.625
#     PHASE=round(PHASE,3)
    print(f'PHASE:{PHASE} degree')

#####RX_UC_PS_GPIO Configuration
def RX_UC_PS_GPIO_CONFIG(ADC_SW,RX_CAL_SW,PHASE):
    #Input inspeciton
    if (ADC_SW>>1)!=0:
        print('ADC_SW Input Error')
        return
    elif (RX_CAL_SW>>1)!=0:
        print('RX_CAL_SW Input Error')
        return
    elif PHASE>360 or PHASE<0:
        print('PHASE Input Error')
        return
    #####Phase to bit sequence 
    PHASE=round(PHASE/5.625)
    print(f'Setting Phase:{PHASE*5.625} degree')
    # print(bin(PHASE))
    #####Concatenate write data
    WRITE_DATA=(ADC_SW<<7)+(RX_CAL_SW<<6)+PHASE
    print(f'Write Data:{bin(WRITE_DATA)}')
    
    #Select the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x08])
    #Write Data into GPIO
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], write_data = [WRITE_DATA])
    #GPIO Configuration => All output port
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x03], write_data = [0x00])
    #Deselect the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])

#####RX_UC_PS_GPIO READ Status    
def RX_UC_PS_GPIO_READ():
    #Select the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x08])
    #Read the data from RX_UC_PS_GPIO
    READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], byte_len = 1)
    #Deselect the MUX Channel
    Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
    
    #####ADC_SW & RX_CAL_SW Status
    if (READ_DATA[0] & (1<<7))==(1<<7):
        print('T1_ADC is connected to TX_ADC')
    else:
        print('T1_ADC is connected to RX_ADC')
    if (READ_DATA[0] & (1<<6))==(1<<6):
        print('RX_UC_30GHz is selected')
    else:
        print('RX_Coupled is selected')
    #####Phase Status
    PHASE=(READ_DATA[0] & ((1<<6)-1))*5.625
#     PHASE=round(PHASE)
    print(f'PHASE:{PHASE} degree')    
    
#####TX/RX_PLL_ATT_GPIO Configuration
#Example PLL_ATT_GPIO_CONFIG('TX_PLL',3):
def PLL_ATT_GPIO_CONFIG(TRX,ATT,Tool=None):
    #ATT==[] => Initial GPIO Only 
    if ATT==[]:
        if TRX=='TX_PLL':        
            #Select the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x02])
#             #Pull-down Resistor Selection
#             Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x44], write_data = [0x00])
            #Set Output Reg to  0
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], write_data = [0x00])
            #GPIO Configuration => Ch7~Ch5:Input/Ch4~Ch0:Output
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x03], write_data = [0xE0])
            #Deselect the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
            print('TX_PLL_ATT is initialized')
            return
        elif TRX=='RX_PLL':
            #Select the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x04])
#             #Pull-down Resistor Selection
#             Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x44], write_data = [0x00])
            #Set Output Reg to  0
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], write_data = [0x00])
            #GPIO Configuration => Ch7~Ch5:Input/Ch4~Ch0:Output
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x03], write_data = [0xE0])
            #Deselect the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
            print('RX_PLL_ATT is initialized')
            return
    elif (ATT[0]<=15.5) or (ATT[0]>=0):
        if TRX=='TX_PLL':        
            #Select the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x02])
            #Attenuation Value Setting
            ATT[0]=round(ATT[0]/0.5)
#             print(bin(~ATT[0]&((1<<5)-1)))
            ATT_DATA=~ATT[0]&((1<<5)-1)            
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], write_data = [ATT_DATA])
            #Deselect the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
            print(f'Setting {TRX} Attenuation:{ATT[0]*0.5}dB')
            return
        elif TRX=='RX_PLL':
            #Select the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x04])
            #Attenuation Value Setting
            ATT[0]=round(ATT[0]/0.5)
#             print(bin(~ATT[0]&((1<<5)-1)))
            ATT_DATA=~ATT[0]&((1<<5)-1)            
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], write_data = [ATT_DATA])
            #Deselect the MUX Channel
            Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
            print(f'Setting {TRX} Attenuation:{ATT[0]*0.5}dB')
            return
    else:
        print('Function Input Error')
         
#####TX/RX_PLL_ATT_GPIO READ 
def PLL_ATT_GPIO_READ(TRX,Tool=None):
    if TRX=='TX_PLL':        
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x02])
        #Read the data from TX_PLL_GPIO
        READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], byte_len = 1)
        READ_DATA[0]=(~(READ_DATA[0]))&((1<<5)-1)
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
        print(f'{TRX} LO Attenuation:{(READ_DATA[0])*0.5}dB')
        return
    elif TRX=='RX_PLL':
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x04])
        #Read the data from RX_PLL_GPIO
        READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = 0x20, reg_ptr = [0x01], byte_len = 1)
        READ_DATA[0]=(~(READ_DATA[0]))&((1<<5)-1)
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
        print(f'{TRX} LO Attenuation:{(READ_DATA[0])*0.5}dB')
        return
    else:
        print('Function Input Error')
def PLL_PD_ADC_CONFIG(TRX,Tool=None):
    if TRX=='TX_PLL':        
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x02])
        #Initialize the ADC
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x48, reg_ptr = [0x01], write_data = [0xC5,0x83])
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
        print('TX_PLL_PD_ADC is initialized')
        return
    elif TRX=='RX_PLL':
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x04])
        #Initialize the ADC
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x48, reg_ptr = [0x01], write_data = [0xC5,0x83])
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
        print('RX_PLL_PD_ADC is initialized')
        return
    
def PLL_PD_ADC_READ(TRX,Tool=None):
    if TRX=='TX_PLL':        
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x02])
        #Read the data from PLL_PD_ADC
        READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = 0x48, reg_ptr = [0x00], byte_len = 2)
        (VSENSE,)=struct.unpack("h",struct.pack("<BB",READ_DATA[1],READ_DATA[0]))
        #LSB = 0.0625mV
        VSENSE=VSENSE*0.0625
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
        print(f'TX_PLL_PD Voltage:{VSENSE}mV')
        return
    elif TRX=='RX_PLL':
        #Select the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x04])
        #Read the data from PLL_PD_ADC
        READ_DATA=Tool.i2c_read(device = 'iic_0', slv_addr = 0x48, reg_ptr = [0x00], byte_len = 2)
        (VSENSE,)=struct.unpack("h",struct.pack("<BB",READ_DATA[1],READ_DATA[0]))
        #LSB = 0.0625mV
        VSENSE=VSENSE*0.0625
        #Deselect the MUX Channel
        Tool.i2c_write(device = 'iic_0', slv_addr = 0x70, reg_ptr = [], write_data = [0x00])
        print(f'RX_PLL_PD Voltage:{VSENSE}mV')
        return
    
def turn_off(Tool=None):

    #Power off Sequence

    ### SPI_CSB_IDLE_STATE
    Tool.SPI_init(device = 'SPI_0', SPI_CSB_IDLE_STATE = 0, SPI_CSB_MASK = 0, SPI_CPOL = 0, SPI_CPHA = 0, SPI_SDIO_mode = 0) 
    Tool.SPI_init(device = 'SPI_1', SPI_CSB_IDLE_STATE = 0, SPI_CSB_MASK = 0, SPI_CPOL = 0, SPI_CPHA = 0, SPI_SDIO_mode = 0)

    ### I2C_MUX_RSB
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['I2C_UCDC_RSTB']:0})

    # #Disable FE
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_FE']:0})

    # #Disable RX_PLL
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_RX_PLL']:0})
    # #Disable TX_PLL
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_TX_PLL']:0})

    # ##### Turn of VG to most negative voltage!!! <Critical>


    time.sleep(1)
    # #Disable VDD_4V_UCDC
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_VDD_4V_UCDC']:0})
    time.sleep(0.1)
    # #Disable VDD_3V3_UCDC
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_VDD_3V3_UCDC']:0})
    time.sleep(1)
    ##### Ensure the current =>0 mA 
    # #Disable VDD_5V_UCDC
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_DVDD_5V_UCDC']:0})
    # Disable VDD_-5V_UCDC
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_VDD_-5V_UCDC']:0})
    # Disable DVDD_3V3_UCDC
    Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {UCDC_PIN_LIST['EN_DVDD_3V3_UCDC']:0})
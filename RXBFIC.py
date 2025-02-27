import time

def f6212_G63_LNASWON_LNA1imax_local(ic_address = 0x00,Tool=None):
    tx_bytes = [
        [0x28,ic_address,0x00,0x00,0x00],
        [0x28,ic_address,0x06,0x00,0x00],
        [0x28,ic_address,0x0A,0x00,0x00],
        [0x28,ic_address,0x05,0x0B,0x30],
        [0x28,ic_address,0x64,0x00,0x00],
        [0x28,ic_address,0x01,0x0C,0x8A],
        [0x28,ic_address,0x09,0x00,0x00],
        [0x28,ic_address,0x07,0x00,0x00],
        [0x28,ic_address,0x0B,0x00,0x00],
        [0x28,ic_address,0x20,0x6C,0xDB],
        [0x28,ic_address,0x24,0x6C,0xDB],
        [0x28,ic_address,0x28,0x6C,0xDB],
        [0x28,ic_address,0x2C,0x6C,0xDB],
        [0x28,ic_address,0x30,0x6C,0xDB],
        [0x28,ic_address,0x34,0x6C,0xDB],
        [0x28,ic_address,0x38,0x6C,0xDB],
        [0x28,ic_address,0x3C,0x6C,0xDB],
        [0x28,ic_address,0x40,0x6C,0xDB],
        [0x28,ic_address,0x44,0x6C,0xDB],
        [0x28,ic_address,0x48,0x6C,0xDB],
        [0x28,ic_address,0x4C,0x6C,0xDB],
        [0x28,ic_address,0x50,0x6C,0xDB],
        [0x28,ic_address,0x54,0x6C,0xDB],
        [0x28,ic_address,0x58,0x6C,0xDB],
        [0x28,ic_address,0x5C,0x6C,0xDB],   
        [0x28,ic_address,0x21,0x2F,0xFF],   #CH1_CTRL
        [0x28,ic_address,0x25,0x2F,0xFF],
        [0x28,ic_address,0x29,0x2F,0xFF],
        [0x28,ic_address,0x2D,0x2F,0xFF],
        [0x28,ic_address,0x31,0x2F,0xFF],
        [0x28,ic_address,0x35,0x2F,0xFF],
        [0x28,ic_address,0x39,0x2F,0xFF],
        [0x28,ic_address,0x3D,0x2F,0xFF],
        [0x28,ic_address,0x41,0x2F,0xFF],
        [0x28,ic_address,0x45,0x2F,0xFF],
        [0x28,ic_address,0x49,0x2F,0xFF],
        [0x28,ic_address,0x4D,0x2F,0xFF],
        [0x28,ic_address,0x51,0x2F,0xFF],
        [0x28,ic_address,0x55,0x2F,0xFF],
        [0x28,ic_address,0x59,0x2F,0xFF],
        [0x28,ic_address,0x5D,0x2F,0xFF],
        [0x28,ic_address,0x22,0x03,0xF8],   #CH1_set
        [0x28,ic_address,0x26,0x03,0xF9],
        [0x28,ic_address,0x2A,0x03,0xF8],
        [0x28,ic_address,0x2E,0x03,0xF9],
        [0x28,ic_address,0x32,0x03,0xF8],
        [0x28,ic_address,0x36,0x03,0xF9],
        [0x28,ic_address,0x3A,0x03,0xF8],
        [0x28,ic_address,0x3E,0x03,0xF9],
        [0x28,ic_address,0x42,0x03,0xF8],
        [0x28,ic_address,0x46,0x03,0xF9],
        [0x28,ic_address,0x4A,0x03,0xF8],
        [0x28,ic_address,0x4E,0x03,0xF9],
        [0x28,ic_address,0x52,0x03,0xF8],
        [0x28,ic_address,0x56,0x03,0xF9],
        [0x28,ic_address,0x5A,0x03,0xF8],
        [0x28,ic_address,0x5E,0x03,0xF9],
        [0x28,ic_address,0x23,0x00,0x00],
        [0x28,ic_address,0x27,0x00,0x00],
        [0x28,ic_address,0x2B,0x00,0x00],
        [0x28,ic_address,0x2F,0x00,0x00],
        [0x28,ic_address,0x33,0x00,0x00],
        [0x28,ic_address,0x37,0x00,0x00],
        [0x28,ic_address,0x3B,0x00,0x00],
        [0x28,ic_address,0x3F,0x00,0x00],
        [0x28,ic_address,0x43,0x00,0x00],
        [0x28,ic_address,0x47,0x00,0x00],
        [0x28,ic_address,0x4B,0x00,0x00],
        [0x28,ic_address,0x4F,0x00,0x00],
        [0x28,ic_address,0x53,0x00,0x00],
        [0x28,ic_address,0x57,0x00,0x00],
        [0x28,ic_address,0x5B,0x00,0x00],
        [0x28,ic_address,0x5F,0x00,0x00],
        [0x28,ic_address,0x69,0x00,0x0f],
        [0x28,ic_address,0x6A,0x00,0x8F],
        [0x28,ic_address,0x6B,0x00,0x0f],
        [0x28,ic_address,0x6C,0x00,0x0f],]
    
    for tx_byte in tx_bytes:
#         print(tx_byte)
        Tool.SPI_program(device = ['SPI_1'], w_data = [[tx_byte, [0x00]*len(tx_byte), [0x00]*len(tx_byte), [0x00]*len(tx_byte)]], r_bytes = [0])
def limit_range(target, max, min):
    if target > max:
        return max
    elif target < min:
        return min
    else:
        return target
def RX_ch_set(ic_address:int, channel, gain_code:int=0, gain:float=None, phase_code:int=0, phase:float=None, DA_bypass:bool=True, disable:bool=False, rf_load:bool=True, subchannel:int=1,Tool=None):
# channel from 1 to 8, subchannel: 1~2
    reg_addr_lut = {"1v":0x22,"1h":0x2A,"2h":0x32,"2v":0x3A,"3v":0x42,"3h":0x4A,"4h":0x52,"4v":0x5A}
#     register_address = 0x1A-4 + channel*8 + subchannel*4 # address from 0x22
    register_address =reg_addr_lut[channel]
    # gain phase decode
    if gain != None:
        gain_code = int((gain+1.4)/0.45+0.5) # minimun gain = -1.4, step size = 0.45
    if phase != None:
        phase_code = int((phase%360)/5.6 + 0.5) # phase step size = 5.6
    gain_code_b=bin(gain_code);
    # if gain_code != None and phase_code != None:
#     tx_byte = [0x28 if rf_load else 0x20, ic_address, register_address, phase_code<<2|gain_code>>4, (gain_code&0x3)<<4|int(DA_bypass)<<3|int(disable)]
    tx_byte = [0x28 if rf_load else 0x20, ic_address, register_address, phase_code<<2|gain_code>>4, (gain_code&0x0f)<<4|int(DA_bypass)<<3|int(disable)]
    Tool.SPI_program(device = ['SPI_1'], w_data = [[tx_byte, [0x00]*len(tx_byte), [0x00]*len(tx_byte), [0x00]*len(tx_byte)]], r_bytes = [0])
#     print(gain_code, phase_code, tx_byte)
def f6212_init1(Tool=None):
    
    Tool.i2c_write(device= 'iic_1', slv_addr= 0x20, reg_ptr= [0x01], write_data= [0xFF])
    Tool.i2c_write(device= 'iic_1', slv_addr= 0x20, reg_ptr= [0x03], write_data= [0x00])

    # Define GPIO Output Pins
    # Tool.gpio_init_w_pin(device = 'gpio_3v3', w_pin = [16]) 
    # RST
    # Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {16:1})
    time.sleep(1)
#     f6212_init(ic_address = 0x00,Tool=Tool)
    # Tool.gpio_write(device = 'gpio_3v3', w_pin_data = {16:1})
    f6212_G63_LNASWON_LNA1imax_local(ic_address = 0x00,Tool=Tool)
    # RX_ch_set(0x00, 1, gain=27, phase=0, disable=False,Tool=Tool)
    # RX_ch_set(0x00, 2, gain=27, phase=0, disable=False ,Tool=Tool)
    # RX_ch_set(0x00, 3, gain=27, phase=0, disable=False ,Tool=Tool)
    # RX_ch_set(0x00, 4, gain=27, phase=0, disable=False ,Tool=Tool)
    # RX_ch_set(0x00, 5, gain=27, phase=0, disable=False ,Tool=Tool)
    # RX_ch_set(0x00, 6, gain=27, phase=0, disable=False ,Tool=Tool)
    # RX_ch_set(0x00, 7, gain=27, phase=0, disable=False ,Tool=Tool)
    # RX_ch_set(0x00, 8, gain=27, phase=0, disable=False ,Tool=Tool)
    RX_ch_set(0x00, "1v", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "1h", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "2h", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "2v", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "3v", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "3h", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "4h", gain=0, phase=0, disable=True ,Tool=Tool)
    RX_ch_set(0x00, "4v", gain=0, phase=0, disable=True ,Tool=Tool)
def RX_stage(stage_num,Tool=None):
    gain=17
    if stage_num == 0:
        f6212_init1(Tool=Tool)
        Tool.i2c_write(device= 'iic_1', slv_addr= 0x20, reg_ptr= [0x01], write_data= [0x00])
        Tool.i2c_write(device= 'iic_1', slv_addr= 0x20, reg_ptr= [0x03], write_data= [0x00])
    if stage_num == 1:
        f6212_init1(Tool=Tool) 
    if stage_num == 2:  #DMW XPD CAL RHCP
        RX_ch_set(0x00, '1v', gain=gain, phase=0, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '1h', gain=gain, phase=60, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2h', gain=gain, phase=45, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2v', gain=gain, phase=170, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3v', gain=gain, phase=150, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3h', gain=gain, phase=240, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4h', gain=gain, phase=230, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4v', gain=gain, phase=345, disable=False ,DA_bypass=True,Tool=Tool)
    if stage_num==3:#DMW area CAL RHCP
        RX_ch_set(0x00, '1v', gain=gain, phase=0, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '1h', gain=gain, phase=60, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2v', gain=gain, phase=155, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2h', gain=gain, phase=30, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3v', gain=gain, phase=235, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3h', gain=gain, phase=310, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4v', gain=gain, phase=20, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4h', gain=gain, phase=280, disable=False ,DA_bypass=True,Tool=Tool)
    if stage_num==4:#beamform RHCP p90t30
        RX_ch_set(0x00, '1v', gain=gain, phase=0, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '1h', gain=gain, phase=60, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2h', gain=gain, phase=45+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2v', gain=gain, phase=170+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3v', gain=gain, phase=150+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3h', gain=gain, phase=240+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4h', gain=gain, phase=230, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4v', gain=gain, phase=345, disable=False ,DA_bypass=True,Tool=Tool)

    if stage_num==5:#beamform RHCP p90t-30
        RX_ch_set(0x00, '1v', gain=gain, phase=0, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '1h', gain=gain, phase=60, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2h', gain=gain, phase=45-90+360, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2v', gain=gain, phase=170-90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3v', gain=gain, phase=150-90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3h', gain=gain, phase=240-90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4h', gain=gain, phase=230, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4v', gain=gain, phase=345, disable=False ,DA_bypass=True,Tool=Tool)

    if stage_num==6:#beamform RHCP p0t30
        RX_ch_set(0x00, '1v', gain=gain, phase=0+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '1h', gain=gain, phase=60+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2h', gain=gain, phase=45+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2v', gain=gain, phase=170+90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3v', gain=gain, phase=150, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3h', gain=gain, phase=240, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4h', gain=gain, phase=230, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4v', gain=gain, phase=345, disable=False ,DA_bypass=True,Tool=Tool)
    if stage_num==7:#beamform RHCP p0t-30
        RX_ch_set(0x00, '1v', gain=gain, phase=0-90+360, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '1h', gain=gain, phase=60-90+360, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2h', gain=gain, phase=45-90+360, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '2v', gain=gain, phase=170-90, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3v', gain=gain, phase=150, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '3h', gain=gain, phase=240, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4h', gain=gain, phase=230, disable=False ,DA_bypass=True,Tool=Tool)
        RX_ch_set(0x00, '4v', gain=gain, phase=345, disable=False ,DA_bypass=True,Tool=Tool)

ch_name = {
    "1h1": 0,
    "1h2": 1,
    "1v1": 2,
    "1v2": 3,
    "2h1": 4,
    "2h2": 5,
    "2v1": 6,
    "2v2": 7,
    "3h1": 8,
    "3h2": 9,
    "3v1": 10,
    "3v2": 11,
    "4h1": 12,
    "4h2": 13,
    "4v1": 14, 
    "4v2": 15
    }
def f6212_localRegisterWrite(ic_address:int, register_address:int=None, register_value:int=None, register_address_value:list=None, rf_load:bool=True,Tool=None):
    if register_address != None and register_value != None:
        tx_byte = [0x28 if rf_load else 0x20, ic_address, register_address, register_address_value >> 8, register_address_value & 0xff]
        Tool.SPI_program(device = ['SPI_1'], w_data = [[tx_byte, [0x00]*len(tx_byte), [0x00]*len(tx_byte), [0x00]*len(tx_byte)]], r_bytes = [0])
    elif register_address_value != None:
        tx_byte = [0x28 if rf_load else 0x20, ic_address] + register_address_value
        Tool.SPI_program(device = ['SPI_1'], w_data = [[tx_byte, [0x00]*len(tx_byte), [0x00]*len(tx_byte), [0x00]*len(tx_byte)]], r_bytes = [0])
    else:
        raise Exception("[error] f6212 local register write error. Missing arguement!")
def f6212_localRegisterRead(ic_address:int, register_address:int=None,Tool=None):
    if register_address != None:
        tx_byte = [0x00, ic_address, register_address]
        Tool.SPI_program(device = ['SPI_1'], w_data = [[tx_byte, [0x00]*len(tx_byte), [0x00]*len(tx_byte), [0x00]*len(tx_byte)]], r_bytes = [2])
       
    else:
        raise Exception("[error] f6212 local register write error. Missing arguement!")
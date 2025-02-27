import time

def f5288_init(ic_address, Tool=None):
    print("write to ic : "+ str(ic_address))
    tx_datas = init_register_data
    for tx in tx_datas:
        Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address] + tx,
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
        time.sleep(0.01)

def f5288_power_on(ic_address,H_en = 0, V_en = 0, H_tx = 0, V_tx = 0, power_down = False, Tool=None):
    if power_down:
        Tool.SPI_program(device = ['SPI_0'], w_data = [[[0x28,ic_address,0x00,0x00,0x00]]+[[0]*5]*3], r_bytes = [0])
    else:
        Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address,0x05,0x80,0x93],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
        time.sleep(0.01)
        # Tool.SPI_program(device = ['SPI_0'], w_data = [[
        #     [0x28,ic_address,0x00,0x00,(H_tx<<3)|(V_tx<<2)|(H_en<<1)|(V_en)],
        #     [0x00,ic_address,0x00,0x00,0x00],
        #     [0x00,ic_address,0x00,0x00,0x00],
        #     [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])

def TX_ch_set(gain, phase, channel, ic_address, Tool = None):
    gain_code = limit_range(int((gain / 30.47 + 1) * 255), 255, 0)
    reg_addr_lut = {"1v":0x41,"2v":0x45,"3v":0x49,"4v":0x4d,"1h":0x51,"2h":0x55,"3h":0x59,"4h":0x5d}
    phase_code = limit_range((int((phase/5.6) + 0.5)), 0x3f, 0x00)
    # print([0x28,ic_address] + [reg_addr_lut[channel]] + [phase_code<<2, gain_code])
    Tool.SPI_program(device = ['SPI_0'], w_data = [[
        [0x28,ic_address] + [reg_addr_lut[channel]] + [phase_code<<2, gain_code],
        [0x00,ic_address,0x00,0x00,0x00],
        [0x00,ic_address,0x00,0x00,0x00],
        [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
    time.sleep(0.01)
        
def TX_ch_on(channel, ic_address, Tool=None):
    if isinstance(channel, list):
        h_setting = 0xe0
        v_setting = 0xe0
        if '1v' in channel:
            v_setting |= 0x01
        if '2v' in channel:
            v_setting |= 0x02
        if '3v' in channel:
            v_setting |= 0x04
        if '4v' in channel:
            v_setting |= 0x08
        if '1h' in channel:
            h_setting |= 0x01
        if '2h' in channel:
            h_setting |= 0x02
        if '3h' in channel:
            h_setting |= 0x04
        if '4h' in channel:
            h_setting |= 0x08
    else:
        if channel == '1v':
            v_setting = 0xe1
            h_setting = 0xe0
        elif channel == '2v':
            v_setting = 0xe2
            h_setting = 0xe0
        elif channel == '3v':
            v_setting = 0xe4
            h_setting = 0xe0
        elif channel == '4v':
            v_setting = 0xe8
            h_setting = 0xe0
        elif channel == '1h':
            v_setting = 0xe0
            h_setting = 0xe1
        elif channel == '2h':
            v_setting = 0xe0
            h_setting = 0xe2
        elif channel == '3h':
            v_setting = 0xe0
            h_setting = 0xe4
        elif channel == '4h':
            v_setting = 0xe0
            h_setting = 0xe8
        else:
            h_setting = 0xe0
            v_setting = 0xe0
    # write to f5288 # v go first
    Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address] + [0x01] + [0x7f, v_setting],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
    time.sleep(0.01)
    Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address] + [0x02] + [0x7f, h_setting],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
    time.sleep(0.01)
    
def TX_ch_off(ic_address, Tool = None):
    # print("TX ch off")
    Tool.SPI_program(device = ['SPI_0'], w_data = [[
        [0x28,ic_address] + [0x01] + [0x7f, 0xf0],
        [0x00,ic_address,0x00,0x00,0x00],
        [0x00,ic_address,0x00,0x00,0x00],
        [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
    time.sleep(0.01)
    Tool.SPI_program(device = ['SPI_0'], w_data = [[
        [0x28,ic_address] + [0x02] + [0x7f, 0xf0],
        [0x00,ic_address,0x00,0x00,0x00],
        [0x00,ic_address,0x00,0x00,0x00],
        [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
    time.sleep(0.01)

ic_addr_lut = {
    1 : 13,
    2 : 12,
    3 : 11,
    4 : 10, 
    5 : 14,
    6 : 15,
    7 : 8,
    8 : 9,
    9 : 3,
    10: 2,
    11: 7,
    12: 6,
    13: 0,
    14: 1,
    15: 4,
    16: 5 
}

init_register_data = [
    [0x0E, 0x4B, 0x30],
    [0x0D, 0x02, 0x04],
    [0x0B, 0x00, 0x00],
    [0x0C, 0x00, 0x00],
    [0x11, 0x00, 0x00],
    [0x00, 0x00, 0x00],
    [0x30, 0x1F, 0x0F],
    [0x20, 0x1F, 0x0F],
    [0x05, 0x80, 0x92],
    [0x0F, 0x00, 0x00],
    [0x10, 0x00, 0x00],
    [0x3A, 0x00, 0x42],
    [0x52, 0x00, 0x03],
    [0x56, 0x00, 0x03],
    [0x5A, 0x00, 0x03],
    [0x5E, 0x00, 0x03],
    [0x31, 0x0B, 0xA8],
    [0x32, 0x02, 0x0C],
    [0x50, 0xC0, 0xFF],
    [0x54, 0xC0, 0xFF],
    [0x58, 0xC0, 0xFF],
    [0x5C, 0xC0, 0xFF],
    [0x42, 0x00, 0x03],
    [0x46, 0x00, 0x03],
    [0x4A, 0x00, 0x03],
    [0x4E, 0x00, 0x03],
    [0x21, 0x0B, 0xA8],
    [0x22, 0x02, 0x0C],
    [0x40, 0xC0, 0xFF],
    [0x44, 0xC0, 0xFF],
    [0x48, 0xC0, 0xFF],
    [0x4C, 0xC0, 0xFF],
    [0x07, 0x06, 0x30],
    [0x06, 0x00, 0x00],
    [0x11, 0x00, 0x00],
    [0x12, 0x00, 0x00],
    [0x53, 0x00, 0x04],
    [0x57, 0x00, 0x04],
    [0x5B, 0x00, 0x04],
    [0x5F, 0x00, 0x04],
    [0x36, 0x00, 0xE9],
    [0x35, 0x1C, 0xB7],
    [0x37, 0x0C, 0x5C],
    [0x51, 0x03, 0x00],
    [0x55, 0x03, 0x00],
    [0x59, 0x03, 0x00],
    [0x5D, 0x03, 0x00],
    [0x43, 0x00, 0x04],
    [0x47, 0x00, 0x04],
    [0x4B, 0x00, 0x04],
    [0x4F, 0x00, 0x04],
    [0x26, 0x00, 0xE9],
    [0x25, 0x1C, 0xB7],
    [0x27, 0x0C, 0x5C],
    [0x41, 0x03, 0x00],
    [0x45, 0x03, 0x00],
    [0x49, 0x03, 0x00],
    [0x4D, 0x03, 0x00],
    [0x01, 0x3F, 0xFF],
    [0x02, 0x3F, 0xFF],
    [0x50, 0xC0, 0xFF],
    [0x54, 0xC0, 0xFF],
    [0x58, 0xC0, 0xFF],
    [0x5C, 0xC0, 0xFF],
    [0x40, 0xC0, 0xFF],
    [0x44, 0xC0, 0xFF],
    [0x48, 0xC0, 0xFF],
    [0x4C, 0xC0, 0xFF]
]

def limit_range(target, max, min):
    if target > max:
        return max
    elif target < min:
        return min
    else:
        return target

def TX_stage(stage_num,Tool=None):
    gain=-20
    sleep_time =5
    if stage_num == 0:
        channel = ['1v', '2v', '3v', '4v', '1h', '2h', '3h', '4h']
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        for ch in channel:
            TX_ch_set(gain=-30.5, phase=0, channel=ch, ic_address=0x00, Tool=Tool)
            TX_ch_off(ic_address=0x00, Tool=Tool)
            f5288_power_on(ic_address=0x00, power_down=True, Tool=Tool)
        time.sleep(1)
        Tool.i2c_write(device= 'iic_0', slv_addr= 0x38, reg_ptr= [0x01], write_data= [0x00])
        Tool.i2c_write(device= 'iic_0', slv_addr= 0x38, reg_ptr= [0x03], write_data= [0x00])
        time.sleep(1)
#         POWER_SUPPLY_OFF()
        
    if stage_num == 1:
        gain=-20
        sleep_time =5
#         POWER_SUPPLY_ON()
        time.sleep(0.1)
        Tool.i2c_write(device= 'iic_0', slv_addr= 0x38, reg_ptr= [0x01], write_data= [0x11])
        Tool.i2c_write(device= 'iic_0', slv_addr= 0x38, reg_ptr= [0x03], write_data= [0x00])
        time.sleep(0.1)
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        f5288_init(ic_address=ic_address, Tool=Tool)
        
        Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address,0x05,0x80,0x93],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
        time.sleep(0.01)

        Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address,0x00,0x00,0x03],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
        time.sleep(0.01)
        Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address] + [0x01] + [0x7f, 0xef],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
# #         #H channel
# #       
# #         print("turn on h channel")
        Tool.SPI_program(device = ['SPI_0'], w_data = [[
            [0x28,ic_address] + [0x02] + [0x7f, 0xef],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00],
            [0x00,ic_address,0x00,0x00,0x00]]], r_bytes = [0])
    if stage_num == 2:
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        gain=-20
        #R
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='1v', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=60, channel='1h', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165, channel='2v', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=30, channel='2h', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165, channel='3v', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=210, channel='3h', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=340, channel='4v', Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=195, channel='4h', Tool=Tool)
    if stage_num == 3:
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        #L
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='1v', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=270, channel='1h', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=180, channel='2v', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=270, channel='2h', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=180, channel='3v', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=90, channel='3h', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='4v', ic_id= ic_id, Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=90, channel='4h', ic_id= ic_id, Tool=Tool)
    if stage_num == 4:# beamforming to 30 deg
        gain=-20
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        #L
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='1v', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=60, channel='1h', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165+90, channel='2v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=30+90, channel='2h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165+90, channel='3v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=210+90, channel='3h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=340, channel='4v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=195, channel='4h', ic_id= ic_id,Tool=Tool)
    if stage_num == 5:#beamforming to -30 deg
        gain=-20
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        #R
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='1v', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=60, channel='1h', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165-90, channel='2v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=300, channel='2h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165-90, channel='3v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=210-90, channel='3h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=340, channel='4v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=195, channel='4h', ic_id= ic_id,Tool=Tool)
    if stage_num == 6:# beamforming to 45 deg
        gain=-20
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        #L
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='1v', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=60, channel='1h', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165+127, channel='2v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=30+127, channel='2h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165+127, channel='3v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=210+127, channel='3h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=340, channel='4v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=195, channel='4h', ic_id= ic_id,Tool=Tool)
    if stage_num == 7:#beamforming to -45 deg
        gain=-20
        ic_id = 13
        ic_address = ic_addr_lut[ic_id]
        #R
        TX_ch_set(ic_address=ic_address, gain=gain, phase=0, channel='1v', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=60, channel='1h', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165-127, channel='2v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=30-127+360, channel='2h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=165-127, channel='3v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=210-127, channel='3h', ic_id= ic_id ,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=340, channel='4v', ic_id= ic_id,Tool=Tool)
        TX_ch_set(ic_address=ic_address, gain=gain, phase=195, channel='4h', ic_id= ic_id,Tool=Tool)

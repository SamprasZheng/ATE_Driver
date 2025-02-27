# from Yaskawa import FS100
from Yaskawa import FS100


robot = FS100("10.100.73.11")

def servo_on():
    """
        turn on robot servo
    """
    status = {}
    if FS100.ERROR_SUCCESS == robot.get_status(status):
        if not status['servo_on']:
            robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_ON)
    else:
        exit(1)

def servo_off():
    """
        turn off robot servo
    """
    robot.switch_power(FS100.POWER_TYPE_SERVO, FS100.POWER_SWITCH_OFF)

def read_position():
    """
        read robot pulse values
    """
    pos_info = {}
    if FS100.ERROR_SUCCESS == robot.read_position(pos_info, data_type=FS100.DATA_TYPE_PULSE):
        return list(pos_info["pos"])

def move_rotation(stops:list, speed=30, tool_no:int=1, user_coor_no:int=1):
    """
        move manipulator at user coordinate XY plane
        args:
            stop (list): user coordinate stop point
            speed (int): robot move speed. 0.1 degree/s 
            tool_no (int): tool coordinate number
            user coor_no (int): user coordinate number
            
            move_type (int): Type of move path. One of following:
                FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS,
                FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS,
                FS100.MOVE_TYPE_LINEAR_INCREMENTAL_POS
    """
    err_no = robot.move( cb_status = None,
    move_type = FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS, 
    coordinate = FS100.MOVE_COORDINATE_SYSTEM_USER, 
    speed_class = FS100.MOVE_SPEED_CLASS_DEGREE, 
    speed = speed, # * 0.1dps 
    pos = stops, 
    form = 0, extended_form = 0, robot_no = 1, station_no = 0, 
    tool_no = tool_no, 
    user_coor_no = user_coor_no, 
    wait = True)

    if err_no != FS100.ERROR_SUCCESS:
        servo_off()

def move_pulse(pulse:list, speed=30, tool_no:int=1):
    """
        move robot with robot pulse
        args:
            pulse (list): pulse stop value
            speed (int): move speed. 0.01 % 
            tool_no (int): tool coordinate number
    """
    err_no = robot.move_pulse( cb_status = None,
    move_type = FS100.MOVE_TYPE_JOINT_ABSOLUTE_POS, 
    speed_class = FS100.MOVE_SPEED_CLASS_PERCENT, 
    speed = speed, # * 0.1dps 
    pos = pulse, 
    robot_no = 1, station_no = 0, 
    tool_no = tool_no, 
    wait = True)

    if err_no != FS100.ERROR_SUCCESS:
        servo_off()

def move_xy(stops:list, speed=30, tool_no:int=1, user_coor_no:int=1):
    """
        move manipulator at user coordinate XY plane
        args:
            stop (list): user coordinate stop point
            speed (int): robot move speed. 0.1 mm/s
            tool_no (int): tool coordinate number
            user coor_no (int): user coordinate number
    """
    err_no = robot.move( cb_status = None,
    move_type = FS100.MOVE_TYPE_LINEAR_ABSOLUTE_POS, 
    coordinate = FS100.MOVE_COORDINATE_SYSTEM_USER, 
    speed_class = FS100.MOVE_SPEED_CLASS_MILLIMETER, 
    speed = speed, # * 0.1dps 
    pos = stops, 
    form = 0, extended_form = 0, robot_no = 1, station_no = 0, 
    tool_no = tool_no, 
    user_coor_no = user_coor_no, 
    wait = True)

    if err_no != FS100.ERROR_SUCCESS:
        servo_off()

if __name__ == "__main__":
    # before you run the following code, you should set the user coordinate and tool coordinate

    """ servo on """
    servo_on()

    move_xy([(0, 0, 20*10000, 0, 0, 0, 0)], speed=700, tool_no=13, user_coor_no=30)
    print("into chamber...")
    
    move_rotation([(0, 0, 20*10000, 75*10000, 0, 0, 0)], speed=100, tool_no=13, user_coor_no=30)
    print("to degree 75")

    move_rotation([(0, 0, 20*10000, 0*10000, 0, 0, 0)], speed=100, tool_no=13, user_coor_no=30)
    print("to degree 0")
    
    move_xy([(0, 0, 0, 0, 0, 0, 0)], speed=700, tool_no=13, user_coor_no=30)
    print("to origin!")

    """ servo off """
    servo_off()

    """ update user cooridate """
    # do it manually

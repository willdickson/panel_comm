from panel_comm import PanelComm
import time

pattern_id = 1
gain_x = 0.0  
offset_x = 0.0
gain_y = 0.0
sleep_t = 0.2
num_test = 20

offset_y_list = [0.05*i for i in range(num_test)]

ctlr = PanelComm(baudrate=921600)
ctlr.set_pattern_id(pattern_id)

for offset_y in offset_y_list:
    ctlr.set_gain_offset(gain_x, offset_x, gain_y, offset_y)
    ctlr.start()
    time.sleep(sleep_t)
    ctlr.stop()

for offset_y in reversed(offset_y_list):
    ctlr.set_gain_offset(gain_x, offset_x, gain_y, offset_y)
    ctlr.start()
    time.sleep(sleep_t)
    ctlr.stop()

ctlr.all_off()


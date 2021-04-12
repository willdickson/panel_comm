from panel_comm import PanelComm
import time

pattern_id = 1
gain_x = 0.0  
offset_x = 0.0
gain_y = 0.0 
offset_y = 0.1
sleep_t = 5.0

ctlr = PanelComm(baudrate=921600)

ctlr.set_pattern_id(pattern_id)
ctlr.set_gain_offset(gain_x, offset_x, gain_y, offset_y)

ctlr.start()
time.sleep(sleep_t)
ctlr.stop()

ctlr.all_off()


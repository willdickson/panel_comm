#!/usr/bin/env python
#
# Example using panel_com
from panel_comm import PanelComm
import time

sleep_t = 15.0
com_port_num = 0
pattern_id = 2
gain_x, offset_x = -1, 1
gain_y, offset_y = 0, 0

print('testing PanelCom')
ctlr = PanelComm(baudrate=921600)

num = 5

for i in range(num):
    print(f'{i+1}/{num} on')
    ctlr.all_on()
    time.sleep(1.0)
    print(f'{i+1}/{num} off')
    ctlr.all_off()
    time.sleep(1.0)
    print()

print('done')

#!/usr/bin/env python
#
# Example using panel_com
from panel_com import PanelCom
import time

sleep_t = 15.0
com_port_num = 0
pattern_id = 2
gain_x, offset_x = -1, 1
gain_y, offset_y = 0, 0

print 'testing PanelCom'
ctlr = PanelCom()

ctlr.SetPatternID(pattern_id)
ctlr.SetGainOffset(gain_x, offset_x, gain_y, offset_y)

ctlr.Start()
time.sleep(sleep_t)
ctlr.Stop()
ctlr.AllOff()

print 'done'

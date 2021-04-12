import sys
import time
from panel_comm import PanelComm

chan = int(sys.argv[1])

ctlr = PanelComm(baudrate=921600)
ctlr.dio_test(chan)



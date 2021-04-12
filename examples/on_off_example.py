from panel_comm import PanelComm
import time

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

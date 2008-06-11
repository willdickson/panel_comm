"""
panel_com.py

Purpose: provides a serial interface class to Michael Reiser's panel
controller.

 Revision Histroy:
   * original in Matlab by MBR (2004?)
   * translated into Python by SAB (2006?)
   * made into a class by JAB 4/8/07
   * made into a stand alone python package by Will Dickson
 
"""

# Constants
GAIN_MAX = 10.0
GAIN_MIN = -10.0
OFFSET_MAX = 5.0
OFFSET_MIN = -5.0

import serial
import types

class PanelCom:
    def __init__( self, userport='/dev/ttyS0' ):
        self.ser = serial.Serial(
            port=userport,               #number of device, numbering starts at
                                         #zero. if everything fails, the user
                                         #can specify a device string, note
                                         #that this isn't portable anymore
                                         #if no port is specified an unconfigured
                                         #an closed serial port object is created
            baudrate=19200,              #baudrate
            bytesize=serial.EIGHTBITS,   #number of databits
            parity=serial.PARITY_NONE,   #enable parity checking
            stopbits=serial.STOPBITS_ONE,#number of stopbits
            timeout=None,                #set a timeout value, None for waiting forever
            xonxoff=0,                   #enable software flow control
            rtscts=0,                    #enable RTS/CTS flow control
        )

    #################################################################################
    def SetPatternID(self,patternid):
        if type(patternid) != types.IntType: raise TypeError
        if patternid < 0: raise ValueError
        self.send(chr(0x02) + chr(0x03) + chr(patternid))

    def BlinkLED( self ): self.send(chr(0x01) + chr(0x50))

    def AllOn( self ): self.send(chr(0x01) + chr(0xFF))

    def AllOff( self ): self.send(chr(0x01) + chr(0x00))

    def Greenscale( self, level ):
        if type(level) != types.IntType: raise TypeError
        if level < 0 or level > 7: raise ValueError
        self.send(chr(0x01) + chr(0x40 + level))

    def Start( self ): self.send(chr(0x01) + chr(0x20))

    def Stop( self ): self.send(chr(0x01) + chr(0x30))

    def Reset( self ): self.send(chr(0x02) + chr(0x01) + chr(0x00))

    def SetMode( self, modex, modey ):
        if type(modex) != types.IntType or type(modey) != types.IntType:
            raise TypeError
        if modex < 0 or modey < 0 or modex > 4 or modey > 4:
            raise ValueError
        self.send(chr(0x03) + chr(0x10) + chr(modex) + chr(modey))

    def SetGainOffset(self,gainx,offsetx,gainy,offsety):
        gainx_num = get_char_num(round(100.0*gainx/GAIN_MAX))
        gainy_num = get_char_num(round(100.0*gainy/GAIN_MAX))
        offsetx_num = get_char_num(round(100.0*offsetx/OFFSET_MAX))
        offsety_num = get_char_num(round(100.0*offsety/OFFSET_MAX))
        msg = chr(0x05) + chr(0x71) + chr(gainx_num) + chr(offsetx_num) + chr(gainy_num) + chr(offsety_num)
        self.send(msg)

    def SetPositions(self,xpos,ypos):
        if type(xpos) != types.IntType or type(ypos) != types.IntType:
            raise TypeError
        if xpos < 0 or xpos > 255 or ypos < 0 or ypos > 255:
            raise ValueError
        self.send(chr(0x05) + chr(0x70) + chr(xpos) + chr(0x00) + chr(ypos) + chr(0x00))

    def Address( self, oldaddr, newaddr ):
        if type(oldaddr) != types.IntType or type(newaddr) != types.IntType:
            raise TypeError
        if oldaddr < 0 or newaddr < 0: raise ValueError
        self.send(chr(0x03) + chr(0xFF) + chr(oldaddr) + chr(newaddr))

    #################################################################################
    def send(self,buf):
        #print "sending:", repr(buf)
        self.ser.write( buf )

def get_char_num(x):
    """
    Convert signed integer to number in range 0 - 256
    """
    return int((256+x)%256)


# --------------------------------------------------------------------------------------
if __name__=='__main__':
    
    import time

    sleep_t = 15.0
    com_port_num = 0
    pattern_id = 2
    gain_x, offset_x = -1, 1
    gain_y, offset_y = 0, 0

    print 'testing PanelCom'
    ctlr = PanelCom(0)

    ctlr.SetPatternID(pattern_id)
    ctlr.SetGainOffset(gain_x, offset_x, gain_y, offset_y)

    ctlr.Start()
    time.sleep(sleep_t)
    ctlr.Stop()
    ctlr.AllOff()

    print 'done'

    

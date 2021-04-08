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
from __future__ import print_function
import serial


# Constants
GAIN_MAX = 10.0
GAIN_MIN = -10.0
OFFSET_MAX = 5.0
OFFSET_MIN = -5.0

class PanelComm(serial.Serial):
    def __init__( self, userport='/dev/ttyUSB0', baudrate=921600):
        super().__init__( 
                port=userport,               
                baudrate=baudrate,           
                bytesize=serial.EIGHTBITS,   
                parity=serial.PARITY_NONE,   
                stopbits=serial.STOPBITS_ONE,
                timeout=None,                
                xonxoff=0,                   
                rtscts=0                    
                )
        self.verbose = False

    def set_pattern_id(self,patternid):
        if type(patternid) != int:
            raise TypeError('patternid must be an integer')
        if patternid < 0: 
            raise ValueError('patternid must be > 0')
        self.send(bytearray([0x02, 0x03, patternid]))

    def blink_led( self ): 
        self.send(bytearray([0x01, 0x50]))

    def all_on( self ): 
        self.send(bytearray([0x01, 0xFF]))

    def all_off( self ): 
        self.send(bytearray([0x01, 0x00]))

    def greenscale( self, level ):
        if type(level) != int: 
            raise TypeError('level must be an int')
        if level < 0 or level > 7: 
            raise ValueError('level must be in range [0,1,2,3,4,5,6,7]')
        self.send(bytearray([0x01, 0x40, level]))

    def start( self ): 
        self.send(bytearray([0x01, 0x20]))

    def stop( self ): 
        self.send(bytearray([0x01, 0x30]))

    def reset( self ): 
        self.send(bytearray([0x02, 0x01, 0x00]))

    def set_mode( self, modex, modey ):
        if type(modex) != int: 
            raise TypeError('modex must be an int')
        if type(modey) != int:
            raise TypeError('modey must be an int')
        if modex < 0 or modex > 4:
            raise ValueError('modex must in range [0,1,2,3,4]')
        if modey < 0 or modey > 4: 
            raise ValueError('modey must in range [0,1,2,3,4]')
        self.send(bytearray([0x03, 0x10, modex, modey]))

    def set_gain_offset(self,gainx,offsetx,gainy,offsety):
        gainx_num = get_char_num(round(100.0*gainx/GAIN_MAX))
        gainy_num = get_char_num(round(100.0*gainy/GAIN_MAX))
        offsetx_num = get_char_num(round(100.0*offsetx/OFFSET_MAX))
        offsety_num = get_char_num(round(100.0*offsety/OFFSET_MAX))
        msg = bytearray([0x05, 0x71, gainx_num, offsetx_num, gainy_num, offsety_num])
        self.send(msg)

    def set_positions(self,xpos,ypos):
        if type(xpos) != int:
            raise TypeError('xpos must be int')
        if type(ypos) != int:
            raise TypeError('ypos must be int')
        if xpos < 0 or xpos > 255: 
            raise ValueError('xpos must in in range [0,255]')
        if ypos < 0 or ypos > 255:
            raise ValueError('ypos must in in range [0,255]')
        msg = bytearray([0x05, 0x70, xpos, 0x00, ypos, 0x00])
        self.send(msg)

    def address( self, oldaddr, newaddr ):
        if type(oldaddr) != int: 
            raise TypeError('oldaddr must be an int')
        if type(newaddr) != int:
            raise TypeError('newaddr must be an int')
        if oldaddr < 0: 
            raise ValueError('oldaddr must be >= 0')
        if newaddr < 0: 
            raise ValueError('newaddr must be >= 0')
        self.send(bytearray([0x03, 0xFF, oldaddr, newaddr]))

    def send(self,buf):
        if self.verbose:
            print("sending:", repr(buf))
        self.write(buf)

def get_char_num(x):
    """
    Convert signed integer to number in range 0 - 256
    """
    return int((256+x)%256)


import minimalmodbus
import serial
import sys
from pymodbus.client import ModbusSerialClient
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url

path_url = Path_url()
class Modbus_PH():

    
    def start_ph(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
    
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x05,0xFF,0x00,0x9C,0x08])
        send.write(data_bytes)

    def stop_ph(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x05,0x00,0x00,0xDD,0xF8])
        send.write(data_bytes)

    def read_ph_counter(self):
        read_ph = open('/home/linaro/txt_file/counter_ph.txt','r')
        return int(read_ph.read())
    
    def write_ph_counter(self):
        counter_ph = self.read_ph_counter()
        counter_ph += 1
        with open('/home/linaro/txt_file/counter_ph.txt','w') as write_ph:
            write_ph.write(str(counter_ph))
            write_ph.close()
    def set_ph_counter_zero(self):
        with open('/home/linaro/txt_file/counter_ph.txt','w') as write_ph:
            write_ph.write(str(0))
            write_ph.close()

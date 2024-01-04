import serial
import sys
from pymodbus.client import ModbusSerialClient
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url

path_url = Path_url()

class Modbus_relay():

    
    def open_lamp_ozone(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x00,0xFF,0x00,0x8C,0x09])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x00\xFF\x00\x8C\x09")

    def close_lamp_ozone(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x00,0x00,0x00,0xCD,0xF9])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x00\x00\x00\xCD\xF9")

    def open_lamp_uv(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x01,0xFF,0x00,0xDD,0xC9])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x01\xFF\x00\xDD\xC9")
    def close_lamp_uv(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x01,0x00,0x00,0x9C,0x39])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x01\x00\x00\x9C\x39")

    def open_ozone_choc(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x02,0xFF,0x00,0x2D,0xC9])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x02\xFF\x00\x2D\xC9")
    def close_ozone_choc(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x02,0x00,0x00,0x6C,0x39])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x02\x00\x00\x6C\x39")
    
    def open_pompe_air(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x03,0xFF,0x00,0x7C,0x09])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x03\xFF\x00\x7C\x09")
    def close_pompe_air(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x03,0x00,0x00,0x3D,0xF9])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x03\x00\x00\x3D\xF9")

    def open_besgo(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x04,0xFF,0x00,0xCD,0xC8])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x04\xFF\x00\xCD\xC8")
    def close_besgo(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x04,0x00,0x00,0x8C,0x38])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x04\x00\x00\x8C\x38")
    
    def open_ph(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x05,0xFF,0x00,0x9C,0x08])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x05\xFF\x00\x9C\x08")
    def close_ph(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x05,0x00,0x00,0xDD,0xF8])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x05\x00\x00\xDD\xF8")
    
    def open_orp(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x06,0xFF,0x00,0x6C,0x08])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x06\xFF\x00\x6C\x08")
    def close_orp(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x06,0x00,0x00,0x2D,0xF8])
        send.write(data_bytes)
        # self.write(b"\x02\x05\x00\x06\x00\x00\x2D\xF8")
    
    def open_apf(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x07,0xFF,0x00,0x3D,0xC8])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x07\xFF\x00\x3D\xC8")
    def close_apf(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.relay_address,0x05,0x00,0x07,0x00,0x00,0x7C,0x38])
        send.write(data_bytes)
        # self.send.write(b"\x02\x05\x00\x07\x00\x00\x7C\x38")
    


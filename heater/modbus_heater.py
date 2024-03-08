import serial
import sys
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url
from pymodbus.client import ModbusSerialClient

path_url = Path_url()

class Modbus_heatpump():
    def read_heatpump_plc(self):
        try:
            status_plc_out = []
            client = ModbusSerialClient(
                    method='rtu',
                    port=path_url.modbus_port,
                    baudrate=9600,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            client.connect()
            res = client.read_coils(512, 4, path_url.plc_address2)
            status_plc_out.append(res.bits[0])
            status_plc_out.append(res.bits[1])
            status_plc_out.append(res.bits[2])
            status_plc_out.append(res.bits[3])
            return status_plc_out
        except:
            pass

    # def open_heatpump(self):
    #     try:
    #         heatpump = serial.Serial(
    #                 port=path_url.modbus_port,
    #                 baudrate = 9600,
    #                 parity=serial.PARITY_NONE,
    #                 stopbits=serial.STOPBITS_ONE,
    #                 bytesize=serial.EIGHTBITS,
    #                 timeout=1)
    #         heatpump.write(b"\x06\x05\x02\x01\xFF\x00\xDD\xF5")
    #         heatpump.close()
    #     except:
    #         pass
        
    # def close_heatpump(self):
    #     try:
    #         send = serial.Serial(
    #                 port=path_url.modbus_port,
    #                 baudrate = 9600,
    #                 parity=serial.PARITY_NONE,
    #                 stopbits=serial.STOPBITS_ONE,
    #                 bytesize=serial.EIGHTBITS,
    #                 timeout=1)
    #         send.write(b"\x06\x05\x02\x01\x00\x00\x9C\x05")
    #         send.close()
    #     except:
    #         pass

    def start_chauffage(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x26,0x02,0xFF,0x00,0x26,0xB2])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x02\xFF\x00\x26\xB2")
        except:
            pass

    def stop_chauffage(self):
        try:
            send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x26,0x02,0x00,0x00,0x67,0x42])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x02\x00\x00\x67\x42")
        except:
            pass
    def stop_pump_ozone(self):
        try:
            ozone = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([path_url.plc_address,0x05,0x26,0x01,0x00,0x00,0x97,0x42])
            ozone.write(data_bytes)
            # ozone.write(b"\x01\x05\x26\x01\x00\x00\x97\x42")
            # ozone.close()
        except:
            pass
    

    def open_heatpump(self):
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
    def close_heatpump(self):
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


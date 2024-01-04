import minimalmodbus
import serial
import sys
from pymodbus.client import ModbusSerialClient
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url
import requests

path_url = Path_url()

class Modbus_read():
    def read_pressure(self):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.plc_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1  
            pressure =  instrument.read_register(18183)
            string_temp = str(pressure)
            len_string = len(string_temp)
            sum = ""
            if len_string == 2:
                sum = "0."+string_temp
            elif len_string == 3:
                string_integer = string_temp[0:1]
                string_double = string_temp[1:len_string]
                sum = string_integer+"."+string_double
            else:
                sum = 0
            print(str(string_temp)+"---xxx---"+str(sum))
            return sum
        except:
            pass
    
    def read_status_relay(self):
        try:
            status_relay = []
            client1 = ModbusSerialClient(
                    method='rtu',
                    port=path_url.modbus_port,
                    baudrate=9600,
                    timeout=3,
                    parity='N',
                    stopbits=1,
                    bytesize=8
                )
            client1.connect()
            res1 = client1.read_coils(0, 8, path_url.relay_address)
            status_relay.append(res1.bits[0])
            status_relay.append(res1.bits[1])
            status_relay.append(res1.bits[2])
            status_relay.append(res1.bits[3])
            status_relay.append(res1.bits[4])
            status_relay.append(res1.bits[5])
            status_relay.append(res1.bits[6])
            status_relay.append(res1.bits[7])
            return status_relay   
        except:
            pass
    def read_status_plc_in(self):
        try:
            status_plc_in = []
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
            res = client.read_coils(256, 4,path_url.plc_address)
            status_plc_in.append(res.bits[0])
            status_plc_in.append(res.bits[1])
            status_plc_in.append(res.bits[2])
            status_plc_in.append(res.bits[3])
            status_plc_in.append(res.bits[4])
            status_plc_in.append(res.bits[5])
            status_plc_in.append(res.bits[6])
            status_plc_in.append(res.bits[7])
            return status_plc_in
        except:
            pass

    def read_status_plc_out(self):
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
            res = client.read_coils(512, 4,path_url.plc_address)
            status_plc_out.append(res.bits[0])
            status_plc_out.append(res.bits[1])
            status_plc_out.append(res.bits[2])
            status_plc_out.append(res.bits[3])
            return status_plc_out
        except:
            pass
    
    def read_temperature(self):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.plc_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1  
            temp =  instrument.read_register(18179)
            string_temp = str(temp)
            len_string = len(string_temp)
            len_decimal = len_string - 1
            string_integer = string_temp[0:len_decimal - 1]
            string_dec = string_temp[len_decimal : len_string]
            temperature =  string_integer+'.'+string_dec
            return temperature
        except:
            pass

    
    def read_ph(self):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.ph_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1
            read_ph1 =  instrument.read_register(2)
            read_ph2 =  instrument.read_register(3)
            request = requests.get("http://localhost:8080/process_ph_orp?data1="+str(read_ph1)+"&data2="+str(read_ph2))
            return request.text
        except:
            pass

    def read_orp(self):
        try:
            instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.orp_address)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud
            instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1
            read_ph2=  instrument.read_register(2)
            read_ph3 =  instrument.read_register(3)
            request = requests.get("http://localhost:8080/process_ph_orp?data1="+str(read_ph2)+"&data2="+str(read_ph3))

            return request.text
        except:
            pass

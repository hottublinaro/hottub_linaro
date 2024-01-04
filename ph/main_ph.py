from urllib.request import urlopen
import json
import sys
from setting.path_url import Path_url
from  modbus_ph import Modbus_PH
sys.path.append('/home/linaro/hottub_linaro/orp/')
from modbus_orp import Modbus_ORP
sys.path.append('/home/linaro/hottub_linaro/apf/')
from modbus_apf import Modbus_APF

path_url = Path_url()
url_substance = path_url.url_substance
url_ph = path_url.url_ph
url_orp = path_url.url_orp
url_apf = path_url.url_apf

modbus_ph = Modbus_PH()
modbus_orp = Modbus_ORP()
modbus_apf = Modbus_APF()

class Main_PH():
    counter_ph = 0 
    counter_orp = 0
    counter_apf = 0
    read_ph_address = 0
    read_orp_address = 0
    set_relay = ''
    current_hour = ''
    def __init__(self, set_ph, set_orp, set_relay, current_hour):
        self.read_ph_address = set_ph
        self.read_orp_address = set_orp
        self.set_relay = set_relay
        self.current_hour = current_hour


    def start_ph(self):
        print('-------start PH ORP APF-------')
        #load setting ph
        response_ph_setting = urlopen(url_substance)
        ph_json = json.loads(response_ph_setting.read())

        #load time ph
        response_ph = urlopen(url_ph)
        data_ph = json.loads(response_ph.read())

        #load time orp
        response_orp = urlopen(url_orp)
        data_orp = json.loads(response_orp.read())

        #load time apf
        response_apf = urlopen(url_apf)
        data_apf = json.loads(response_apf.read())
        
        #read status 8 relay
        relay8 = self.set_relay
        #working ph orp 
        self.process_woking(data_ph[0]['ph_'+str(int(self.current_hour) + 1)], ph_json, relay8, data_orp[0]['orp_'+str(int(self.current_hour) + 1)], data_apf[0]['apf_'+str(int(self.current_hour) + 1)])
       

    def process_woking(self, data_ph, ph_json, relay8, data_orp, data_apf):
        if data_ph == "1":
            self.process_ph(ph_json, relay8)
        else:
            if relay8[5] == True:
                modbus_ph.stop_ph()
        if data_orp == "1":
            self.process_orp(ph_json, relay8)
        else:
            if relay8[6] == True:
                modbus_orp.stop_orp()
        # if data_apf == "1":
        #     self.process_apf(ph_json, relay8)
        # else:
        #     if relay8[7] == True:
        #         modbus_apf.stop_apf()

    def process_ph(self, ph_json, relay8):
        read_ph = self.read_ph_address
        #อ่าน สถานะ relay
      
        if float(read_ph) >= float(ph_json[0]['ph_set']):
            print("------------counter ph start---------------"+str(modbus_ph.read_ph_counter()))
            if int(modbus_ph.read_ph_counter()) == 0:
                print("------------counter ph start---------------"+str(relay8[5]))
                if relay8[5] == False:
                    print("------------counter ph start---------+++++++++++++++++++------")
                    modbus_ph.start_ph()
                modbus_ph.write_ph_counter()
            else :
                if relay8[5] == True:
                    modbus_ph.stop_ph()
                modbus_ph.write_ph_counter()
            if int(modbus_ph.read_ph_counter()) >= (int(ph_json[0]['ph_freq']) * 60) :
            # if (int(modbus_ph.read_ph_counter()) >= 10) :
                modbus_ph.set_ph_counter_zero()
                
        elif float(read_ph) <= float(ph_json[0]['ph_lower']):
            if relay8[5] == True:
                modbus_ph.stop_ph()
                modbus_ph.set_ph_counter_zero()

    def process_orp(self, orp_json,relay8):
        read_orp = self.read_orp_address
        #อ่าน สถานะ relay
        print("ORP WORKING XXXXXXX : "+str(orp_json[0]['orp_set']))
        print("ORP WORKING XXXXXXX : "+str(read_orp))
        print("ORP WORKING XXXXXXX : "+str(modbus_orp.read_orp_counter()))
        if float(read_orp) <= float(orp_json[0]['orp_set']):
            if modbus_orp.read_orp_counter() == 0:
                if relay8[6] == False:
                    modbus_orp.start_orp()
                modbus_orp.write_orp_counter()
            else :
                if relay8[6] == True:
                    modbus_orp.stop_orp()
                modbus_orp.write_orp_counter()
            #แปลงค่า ครึ่งวิให้เป็น วิ * 2
            if modbus_orp.read_orp_counter() >= (int(orp_json[0]['orp_freq']) * 60) :
                modbus_orp.set_orp_counter_zero()
        elif float(read_orp) >= float(orp_json[0]['orp_lower']):
            if relay8[6] == True:
                modbus_orp.stop_orp()
                modbus_orp.set_orp_counter_zero()
        

    def process_apf(self, apf_json,relay8):
        relay8 = relay8
        if modbus_apf.read_apf_counter() == 0:
            if relay8[7] == False:
                modbus_apf.start_apf()
            modbus_apf.write_ph_counter()
        else :
            if relay8[7] == True:
                modbus_apf.stop_apf()
            modbus_apf.write_ph_counter()
            #แปลงค่า ครึ่งวิให้เป็น วิ * 2
        if (float(apf_json[0]['apf_freq'])) == modbus_apf.read_apf_counter() :
            modbus_apf.set_ph_counter_zero()

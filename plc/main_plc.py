from modbus import Modbus
import time
from urllib.request import urlopen
import json
import sys
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url
sys.path.append('/home/linaro/hottub_linaro/relay/')
from modbus_relay import Modbus_relay

path_url = Path_url()
url = path_url.url_setting_mode
url_filtration_time = path_url.url_filtration_time
url_setting = path_url.url_setting


mod = Modbus()
modbus_relay = Modbus_relay()

status_plc_out = ''

class Main_PLC():
    status_relay = ''
    status_filtration = False
    system_datetime = ""
    status_working = 1
    temperature = 0.00
    status_plc = ''
    current_hour = ""
    def __init__(self, system_datetime, temperature, plc, relay_8, current_hour):
        self.system_datetime = system_datetime
        self.temperature = temperature
        self.status_plc = plc
        self.status_relay = relay_8
        self.current_hour = current_hour

    def start_plc(self):
        status_plc_out = self.status_plc
        self.status_filtration = status_plc_out[0]
        #ดึงการตั้งค่าเวลา
        response = urlopen(url)
        data_json = json.loads(response.read())

        #ดึงสถานะการตั้งค่าเวลา filtration
        filtration_time = urlopen(url_filtration_time)
        data_time_status = json.loads(filtration_time.read())

        #ดึงข้อมูล config
        response_setting = urlopen(url_setting)
        data_setting = json.loads(response_setting.read())


        if data_json[0]['sm_filtration'] == "1":
            with open('/home/linaro/txt_file/status_working_auto.txt','w') as write_status_auto:
                write_status_auto.write("False")
                write_status_auto.close()
            if status_plc_out[0] == False:
                mod.start_filtration()
                self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)
            else:
                self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)

            if str(data_json[0]['sm_ozone_choc']) == "2":
                 self.close_ozone_choc()

            

        elif data_json[0]['sm_filtration'] == "2":     
            print("Filtration Auto Mode")
            if str(data_time_status[int(self.current_hour)]) != "0":
                self.auto_filtration_working(data_time_status[int(self.current_hour)], status_plc_out, data_json, data_setting)
            else:
                print('close all')
                read_status_heater = open('/home/linaro/txt_file/status_working_heater.txt','r')
                set_heater_text = read_status_heater.readline().strip()
                if str(set_heater_text)  == "False":
                    if status_plc_out[0] == True:
                        mod.stop_filtration()
                    if status_plc_out[0] == False:
                        if status_plc_out[1] == True:
                            mod.stop_ozone_pump()
                        if status_plc_out[1] == False:
                            mod.stop_chauffage()

               
          
        else :
            print("---------Close Filtration---------")
            if status_plc_out[0] == True:
              
                mod.stop_filtration()
            if status_plc_out[0] == False:
                if status_plc_out[1] == True:
                    mod.stop_ozone_pump()
                if status_plc_out[1] == False:
                    mod.stop_chauffage()

    def auto_filtration_working(self, data_time_status,status_plc_out, data_json, data_setting):
        with open('/home/linaro/txt_file/status_working_auto.txt','w') as write_status_auto:
            write_status_auto.write("True")
            write_status_auto.close()
        if str(data_time_status) != "0":
            if status_plc_out[0] == False:
                mod.start_filtration()
            else:
                if str(data_json[0]['sm_ozone_choc']) == "1":
                    self.start_ozone_choc()
                elif str(data_json[0]['sm_ozone_choc']) == "2":
                    if str(data_time_status) == "2":
                        self.start_ozone_choc()
                    else :
                        self.close_ozone_choc()
                elif str(data_json[0]['sm_ozone_choc']) == "0":
                    self.close_ozone_choc()
        
        else:
            if str(data_json[0]['sm_ozone_choc']) == "1":
                self.start_ozone_choc()
            elif str(data_json[0]['sm_ozone_choc']) == "2":
                if str(data_time_status) == "2":
                    self.start_ozone_choc()
                else :
                    self.close_ozone_choc()
            elif str(data_json[0]['sm_ozone_choc']) == "0":
                self.close_ozone_choc()
            read_status_heater = open('/home/linaro/txt_file/status_working_heater.txt','r')
            set_heater_text = read_status_heater.read().rstrip('\n')
            print("xxxxxxxxxxx"+str(set_heater_text))
            if str(set_heater_text) == "False":
                if status_plc_out[0] == True:
                    mod.stop_filtration() 
        self.pompe_ozone_and_chauffage(status_plc_out, data_json, data_setting)


    def pompe_ozone_and_chauffage(self, status_plc_out, data_json, data_setting):
        print("-------------------pompe ozone and chauffage------------------")
        if status_plc_out[0] == True :
                #pompe zone
                if data_json[0]['sm_pomp_ozone'] != "0" :
                    if str(data_json[0]['sm_pomp_ozone']) == "1":
                        if status_plc_out[1] == False:
                            mod.start_ozone_pump()
                    elif str(data_json[0]['sm_pomp_ozone']) == "2" :
                        if self.status_relay[2] == True:
                            if status_plc_out[1] == False:
                                mod.start_ozone_pump()
                        else:
                            if status_plc_out[1] == True:
                                mod.stop_ozone_pump()
                else:
                    if status_plc_out[1] == True :
                        mod.stop_ozone_pump()
        else:
            if status_plc_out[1] == True :
                mod.stop_ozone_pump()

                            
    def start_ozone_choc(self):
         if self.status_relay[2] == False:
            modbus_relay.open_ozone_choc()
            
    def close_ozone_choc(self):
        if self.status_relay[2] == True:
            modbus_relay.close_ozone_choc()

    
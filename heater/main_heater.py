import json
import sys
from urllib.request import urlopen
from modbus_heater import Modbus_heatpump
sys.path.append('/home/linaro/hottub_linaro/relay/')
from modbus_relay import Modbus_relay
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url
sys.path.append('/home/linaro/hottub_linaro/plc/')
from modbus import Modbus


path_url = Path_url()
url_setting = path_url.url_setting
url = path_url.url_setting_mode
mod_heatpump = Modbus_heatpump()
modbus_relay  = Modbus_relay()
plc_mod = Modbus()


class Main_Heater():

    def start_heater(self,  temperature, plc, relay_8):
        if relay_8[7] == True:
            mod_heatpump.close_heatpump()
        if relay_8[4] == False:
            response_setting = urlopen(url_setting)
            data_setting = json.loads(response_setting.read())

            setting = urlopen(url)
            data_mode = json.loads(setting.read())
            if str(data_mode[0]['sm_filtration']) != "0":
                if str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == True:
                    set_temp = float(data_setting[0]['setting_temperature'])
                    temp_div = float(data_setting[0]['setting_temp_deff'])
                    read = float(temperature)
                    print(set_temp)
                    print(temp_div)
                    print(read)

                    # minus = float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff'])
                    if  float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                        print("เปิดปั้ม")
                        with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("True")
                            read_status_auto.close()
                        if plc[2] == False:
                            mod_heatpump.start_chauffage()
                    elif float(temperature) >= float(data_setting[0]['setting_temperature']): 
                        print("ปิดปั้ม")
                        with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                            read_status_auto.close()
                        if plc[2] == True:
                            mod_heatpump.stop_chauffage()
                elif str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == False:
                    set_temp = float(data_setting[0]['setting_temperature'])
                    temp_div = float(data_setting[0]['setting_temp_deff'])
                    read = float(temperature)
                    print(set_temp)
                    print(temp_div)
                    print(read)
                    if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >  float(temperature):
                        with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("True")
                            read_status_auto.close()
                        if plc[0] == False:
                            plc_mod.start_filtration()
                    else :
                        print("ปิดปั้ม")
                        with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                            read_status_auto.close()
                        if plc[2] == True:
                            mod_heatpump.stop_chauffage()
                else:
                    with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                        read_status_auto.write("False")
                        read_status_auto.close()
                    if plc[2] == True:
                        mod_heatpump.stop_chauffage()
            else:
                with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                    read_status_auto.write("False")
                    read_status_auto.close()
                if plc[2] == True:
                    mod_heatpump.stop_chauffage()

        else:
            with open('/home/linaro/txt_file/status_working_heater.txt','w') as read_status_auto:
                read_status_auto.write("False")
                read_status_auto.close()
            if plc[2] == True:
                mod_heatpump.stop_chauffage()
                
            if plc[2] == False:
                if plc[1] == True:
                    mod_heatpump.stop_pump_ozone()


        

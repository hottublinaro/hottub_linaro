from urllib.request import urlopen
import json
import sys
from setting.path_url import Path_url
import datetime
from modbus_besgo import Modbus_besgo
sys.path.append('/home/linaro/hottub_linaro/plc/')
from modbus import Modbus

path_url = Path_url()
url_besgo = path_url.url_besgo
url_besgo_setting= path_url.url_besgo_setting
mod_besgo = Modbus_besgo()
mod_plc = Modbus()


class Main_Besgo():
    status_working_besgo = False
    counter_besgo_working = 0
    current_time = ''
    set_relay8 = ''
    set_plc_out = ''
    status_working = ""
    set_time_working = ''


    def start_besgo(self, current_time, set_relay8, set_plc_out, setting_mode):
      
        system_time = datetime.datetime.now()
        day = system_time.strftime("%a")
        besgo_response = urlopen(url_besgo)
        besgo_json = json.loads(besgo_response.read())
       
        besgo_settin_response = urlopen(url_besgo_setting)
        besgo_setting_json = json.loads(besgo_settin_response.read())
        #read array 8 chanel
        relay8 = set_relay8
        plc_read = set_plc_out
        print("--------Besgo-------"+str(besgo_setting_json[0]['backwash_mode']))
        if str(besgo_setting_json[0]['backwash_mode']) == "1":
            with open('/home/linaro/txt_file/status_besgo.txt','w') as write_status_besgo:
                write_status_besgo.write("True")
                write_status_besgo.close()
            if plc_read[0] == False:
                mod_plc.start_filtration()
            if relay8[4] == False and plc_read[0] == True:
                mod_besgo.open_besgo()
                
            if relay8[4] == True:
                mod_besgo.close_all_working(relay8)
            
        elif str(besgo_setting_json[0]['backwash_mode']) == "2":
            print("backwash AUTO")
            for item in besgo_json:
                time_set = item.split('-')
                if current_time >= time_set[0] and current_time <= time_set[0]:
                    if plc_read[0] == False:
                        mod_plc.start_filtration()
                    else:
                        if relay8[4] == False and plc_read[0] == True:
                            if self.status_working != "complete" or self.set_time_working != current_time:
                                print("open bessgo working")
                                mod_besgo.open_besgo()
                                self.counter_besgo_working = self.counter_besgo_working + 1
                                self.set_time_working = current_time
                                with open('/home/linaro/txt_file/status_besgo.txt','w') as write_status_besgo:
                                    write_status_besgo.write("True")
                                    write_status_besgo.close()
                                self.status_working = "working"
                        if relay8[4] == True:
                            mod_besgo.close_all_working(relay8)
                elif current_time >= time_set[1]:
                    print("ไม่ทำงาน besgo")
                    if relay8[4] == True:
                        mod_besgo.close_besgo()
                    with open('/home/linaro/txt_file/status_besgo.txt','w') as write_status_besgo:
                        write_status_besgo.write("False")
                        write_status_besgo.close()
                    self.counter_besgo_working = 0
                    self.status_working = ""
           
                                  
        else:
            if relay8[4] == True:
                mod_besgo.close_besgo()
            if int(setting_mode[0]['sm_filtration']) == 0:
                if relay8[4] == False:
                    mod_plc.stop_filtration()
            with open('/home/linaro/txt_file/status_besgo.txt','w') as write_status_besgo:
                write_status_besgo.write("False")
                write_status_besgo.close()
    

       
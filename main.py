import time
import sys
import datetime
from restart import *
from write_file import Write_file
from modbus_read import Modbus_read
from urllib.request import urlopen
import json
from close_all import Close_All
import threading


sys.path.append('/home/linaro/hottub_linaro/besgo/')
from main_besgo import Main_Besgo
sys.path.append('/home/linaro/hottub_linaro/plc/')
from main_plc import Main_PLC
from modbus import Modbus
sys.path.append('/home/linaro/hottub_linaro/relay/')
from main_relay import Main_relay
sys.path.append('/home/linaro/hottub_linaro/ph/')
from main_ph import Main_PH
sys.path.append('/home/linaro/hottub_linaro/volttag/')
from main_volt_tag import Main_volt_tag
sys.path.append('/home/linaro/hottub_linaro/setting/')
from path_url import Path_url
sys.path.append('/home/linaro/hottub_linaro/heater/')
from main_heater import Main_Heater
from main_heatpump import Main_heatpump
from modbus_heater import Modbus_heatpump


modbus_read = Modbus_read()
path_url = Path_url()
besgo = Main_Besgo()
close_all  = Close_All()
volt = Main_volt_tag()
heater  = Main_Heater()
plc_mod = Modbus()
write_file = Write_file()
main_heatpump = Main_heatpump()
modbus_heater = Modbus_heatpump()

counter_pressure = 0
url_setting = path_url.url_setting
url_setting_mode = path_url.url_setting_mode
url_selection = path_url.url_selection
url_heatpump = path_url.url_heatpump
url_night_time =  path_url.url_night_time

def counter_machine():
    while True:
        try:
            with open('/home/linaro/txt_file/row_counter_machine.txt','r') as read_row:
                read_row_file = read_row.readline().strip()
            if read_row_file != '':
                if int(read_row_file) < 60:
                    sum_rows = int(read_row_file) + 1
                    with open('/home/linaro/txt_file/row_counter_machine.txt','w') as write_row:
                        write_row.write(str(sum_rows))
                else:
                    with open('/home/linaro/txt_file/row_counter_machine.txt','w') as write_row:
                        write_row.write('0')
                    with open('/home/linaro/txt_file/row_counter_machine.txt','r') as read_counter_ma:
                        counter_ma = read_counter_ma.readline().strip()
                        sum_counter_ma = int(counter_ma) + 1
                    with open('/home/linaro/txt_file/row_counter_machine.txt','w') as write_counter_ma:
                        write_counter_ma.write(str(sum_counter_ma))

            else:
                with open('/home/linaro/txt_file/row_counter_machine.txt','w') as write_row:
                    write_row.write("0")
            time.sleep(1)
        except:
            pass
before_backwash = threading.Thread(target=counter_machine, args=())
before_backwash.start()
try:
    while True:
        print("WORKING HOTTUB")
        system_time = datetime.datetime.now()
        current_time = system_time.strftime("%H:%M")
        current_time_sec = system_time.strftime("%H:%M:%S")
        current_hour =  system_time.strftime("%H")
        current_minute =  system_time.strftime("%M")
        sec_time =  system_time.strftime("%S")
      
        response_setting = urlopen(url_setting)
        data_setting = json.loads(response_setting.read())

        response_setting_mode =  urlopen(url_setting_mode)
        setting_mode = json.loads(response_setting_mode.read())


        response_selection =  urlopen(url_selection)
        setting_selection = json.loads(response_selection.read())

        #heatpump api
        response_heatpump = urlopen(url_heatpump)
        setting_heatpump = json.loads(response_heatpump.read())
        hour_start_heatpump = setting_heatpump[0]['heatpump_start']
        hour_end_heatpump = setting_heatpump[0]['heatpump_end']
        heatpump_split_hour_start = hour_start_heatpump.split(':')
        heatpump_split_hour_end = hour_end_heatpump.split(':')


        #night time setting url
        response_night_time = urlopen(url_night_time)
        setting_night_time = json.loads(response_night_time.read())
        hour_start_night_time = setting_night_time[0]['night_time_start']
        hour_end_night_time = setting_night_time[0]['night_time_end']
        night_time_split_start = hour_start_night_time.split(':')
        night_time_split_end = hour_end_night_time.split(':')

        read_pressure =  modbus_read.read_pressure()
        print('pressure : '+str(read_pressure))

        relay_8 = modbus_read.read_status_relay()
        print("Relay : "+str(relay_8))

        #read plc
        plc = modbus_read.read_status_plc_out()
        print('PLC  OUT : '+str(plc))
       
        plc_in = modbus_read.read_status_plc_in()
        print('PLC IN: '+str(plc_in))
        #read temperature
        temperature = modbus_read.read_temperature()
        print('Temperature : '+str(temperature))
        # read ph
        ph = 0
        if int(setting_selection[0]['ph']) == 1:
            ph = modbus_read.read_ph()
        print("PH : "+str(ph))
        #read orp
        orp = 0
        if int(setting_selection[0]['orp']) == 1:
            orp = modbus_read.read_orp()
        print("ORP : "+str(orp))
      
        # #write file 

        write_file.start_write(relay_8, plc, temperature, ph, orp, read_pressure, plc_in)

        read_status_besgo = open('/home/linaro/txt_file/status_besgo.txt','r')
        status_bes = read_status_besgo.read().rstrip('\n')
      

        #อ่านค่า set pressure จาก front
        read_set_pressure = open('/home/linaro/txt_file/set_pressure.txt','r')
        set_pressure_text = read_set_pressure.read().rstrip('\n')
        split_set_pressure = set_pressure_text.split(",")
      
        #check nighttime swicth
        if str(setting_night_time[0]['night_time_enable']) == "0":
            if plc_in[2] == False:
                if int(current_hour) < 21 and int(current_hour) > 7 : 
                    print("in of time")
                    #check bypass mode
                    if str(setting_mode[0]['sm_bypass']) == "0":
                        count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                        if count_down.read() == '':    
                            besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                            if relay_8[4] == True:
                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                        main_heatpump.start_heatpump(temperature, plc, relay_8)
                                    else:
                                        heater.start_heater(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)

                            if str(status_bes) == "False":
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()
                                
                                main_ph = Main_PH(ph, orp, relay_8,current_hour)
                                if plc[0] == True:
                                    main_ph.start_ph()

                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                        main_heatpump.start_heatpump(temperature, plc, relay_8)
                                    else:
                                        if int(setting_selection[0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1: 
                                        heater.start_heater(temperature, plc, relay_8)

                                #นับเวลาตรวจสอบ pressure ไม่มีแรงดัน
                                if plc[0] == True and relay_8[4] == False:
                                    if float(split_set_pressure[0]) > float(read_pressure):
                                        counter_pressure = counter_pressure + 1
                                        print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                        if counter_pressure == int(split_set_pressure[1]) :
                                            minus_hour = int(current_hour) + int(split_set_pressure[2])
                                            set_new_time = str(minus_hour)+':'+str(sec_time)
                                            write_file.write_over_presssure(set_new_time)

                                    
                        else:
                            print("close Anoter Time")
                            close_all.start_close_plc(plc)
                            if plc[0] == False:
                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()
                                if plc[2] == True:
                                    modbus_heater.stop_chauffage()
                                if relay_8[7] == True:
                                    modbus_heater.close_heatpump()

                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                            
                        
                    else:
                        count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                        if count_down.read() != '':
                            write_file.clear_pressure_time()
                            counter_pressure = 0
                        besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)

                        if str(status_bes) == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                            main_ph = Main_PH(ph, orp, relay_8,current_hour)
                            if plc[0] == True:
                                main_ph.start_ph()
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                else:
                    print("out of time")
                    close_all.start_close_plc(plc)
                    if plc[0] == False:
                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()
                        if plc[2] == True:
                            modbus_heater.stop_chauffage()
                        if relay_8[7] == True:
                            modbus_heater.close_heatpump()
                    time.sleep(0.5)
            else:
                print("PLC NOT FALSE"+str(relay_8[4]))
                #check bypass mode
                if str(setting_mode[0]['sm_bypass']) == "0":
                    count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                    if count_down.read() == '':
                        besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                        
                        if str(status_bes) == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                            main_ph = Main_PH(ph, orp, relay_8,current_hour)
                            if plc[0] == True:
                                main_ph.start_ph()

                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                            if plc[0] == True and relay_8[4] == False:
                                if float(split_set_pressure[0]) > float(read_pressure):
                                    counter_pressure = counter_pressure + 1
                                    print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                    if counter_pressure == int(split_set_pressure[1]) :
                                        minus_hour = int(current_hour) + int(split_set_pressure[2])
                                        set_new_time = str(minus_hour)+':'+str(sec_time)
                                        write_file.write_over_presssure(set_new_time)
                    else:
                        close_all.start_close_plc(plc)
                        if plc[0] == False:
                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()
                            if plc[2] == True:
                                modbus_heater.stop_chauffage()
                            if relay_8[7] == True:
                                modbus_heater.close_heatpump()

                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)
                            
                        
                else:
                    count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                    if count_down.read() != '':
                        write_file.clear_pressure_time()
                        counter_pressure = 0

                    besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                    if relay_8[4] == True:
                        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                            if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                main_heatpump.start_heatpump(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                        else:
                            if int(setting_selection[0]['heater_1']) == 1:
                                heater.start_heater(temperature, plc, relay_8)
                    if str(status_bes) == "False":
                        main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                        main_plc.start_plc()

                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()

                        main_ph = Main_PH(ph, orp, relay_8,current_hour)
                        if plc[0] == True:
                            main_ph.start_ph()
                        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                            if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                main_heatpump.start_heatpump(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                        else:
                            if int(setting_selection[0]['heater_1']) == 1:
                                heater.start_heater(temperature, plc, relay_8)
                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)
        else:
            if str(setting_night_time[0]['night_time_status']) == "0":
                if int(current_hour) < 21 and int(current_hour) > 7 : 
                    print("in of time")
                    #check bypass mode
                    if str(setting_mode[0]['sm_bypass']) == "0":
                        count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                        if count_down.read() == '':    
                            besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                            if relay_8[4] == True:
                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                        main_heatpump.start_heatpump(temperature, plc, relay_8)
                                    else:
                                        if int(setting_selection[0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)

                            if str(status_bes) == "False":
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()
                                
                                main_ph = Main_PH(ph, orp, relay_8,current_hour)
                                if plc[0] == True:
                                    main_ph.start_ph()

                                if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                    if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                        main_heatpump.start_heatpump(temperature, plc, relay_8)
                                    else:
                                        if int(setting_selection[0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)

                                #นับเวลาตรวจสอบ pressure ไม่มีแรงดัน
                                if plc[0] == True and relay_8[4] == False:
                                    if float(split_set_pressure[0]) > float(read_pressure):
                                        counter_pressure = counter_pressure + 1
                                        print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                        if counter_pressure == int(split_set_pressure[1]) :
                                            minus_hour = int(current_hour) + int(split_set_pressure[2])
                                            set_new_time = str(minus_hour)+':'+str(sec_time)
                                            write_file.write_over_presssure(set_new_time)

                                    
                        else:
                            print("close Anoter Time")
                            close_all.start_close_plc(plc)
                            if plc[0] == False:
                                main_relay = Main_relay(relay_8, plc[0])
                                main_relay.start_relay()
                                if plc[2] == True:
                                    modbus_heater.stop_chauffage()
                                if relay_8[7] == True:
                                    modbus_heater.close_heatpump()

                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                            
                        
                    else:
                        count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                        if count_down.read() != '':
                            write_file.clear_pressure_time()
                            counter_pressure = 0
                        besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)

                        if str(status_bes) == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                            main_ph = Main_PH(ph, orp, relay_8,current_hour)
                            if plc[0] == True:
                                main_ph.start_ph()
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                            
                        time.sleep(0.5)
                        volt.start_volt(setting_selection)
                else:
                    print("out of time")
                    close_all.start_close_plc(plc)
                    if plc[0] == False:
                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()
                        if plc[2] == True:
                            modbus_heater.stop_chauffage()
                        if relay_8[7] == True:
                            modbus_heater.close_heatpump()
                    time.sleep(0.5)
            else:
                print("PLC NOT FALSE"+str(relay_8[4]))
                #check bypass mode
                if str(setting_mode[0]['sm_bypass']) == "0":
                    count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                    if count_down.read() == '':
                        besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                        if relay_8[4] == True:
                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                        
                        if str(status_bes) == "False":
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()

                            main_ph = Main_PH(ph, orp, relay_8,current_hour)
                            if plc[0] == True:
                                main_ph.start_ph()

                            if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                                if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                    main_heatpump.start_heatpump(temperature, plc, relay_8)
                                else:
                                    if int(setting_selection[0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                            if plc[0] == True and relay_8[4] == False:
                                if float(split_set_pressure[0]) > float(read_pressure):
                                    counter_pressure = counter_pressure + 1
                                    print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                    if counter_pressure == int(split_set_pressure[1]) :
                                        minus_hour = int(current_hour) + int(split_set_pressure[2])
                                        set_new_time = str(minus_hour)+':'+str(sec_time)
                                        write_file.write_over_presssure(set_new_time)
                    else:
                        close_all.start_close_plc(plc)
                        if plc[0] == False:
                            main_relay = Main_relay(relay_8, plc[0])
                            main_relay.start_relay()
                            if plc[2] == True:
                                modbus_heater.stop_chauffage()
                            if relay_8[7] == True:
                                modbus_heater.close_heatpump()

                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)
                            
                        
                else:
                    count_down = open('/home/linaro/txt_file/count_down_close_system.txt','r')
                    if count_down.read() != '':
                        write_file.clear_pressure_time()
                        counter_pressure = 0

                    besgo.start_besgo(current_time_sec, relay_8, plc, setting_mode)
                    if relay_8[4] == True:
                        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                            if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                main_heatpump.start_heatpump(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                        else:
                            if int(setting_selection[0]['heater_1']) == 1:
                                heater.start_heater(temperature, plc, relay_8)
                    if str(status_bes) == "False":
                        main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour)
                        main_plc.start_plc()

                        main_relay = Main_relay(relay_8, plc[0])
                        main_relay.start_relay()

                        main_ph = Main_PH(ph, orp, relay_8,current_hour)
                        if plc[0] == True:
                            main_ph.start_ph()
                        if int(setting_selection[0]['heat_pump_heater']) == 1 or int(setting_selection[0]['heat_pump_cooling']) == 1 or  int(setting_selection[0]['heat_pump_all']) == 1:
                            if int(current_hour) >= int(heatpump_split_hour_start[0])  and int(current_hour) < int(heatpump_split_hour_end[0]) :
                                main_heatpump.start_heatpump(temperature, plc, relay_8)
                            else:
                                if int(setting_selection[0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8)
                        else:
                            if int(setting_selection[0]['heater_1']) == 1:
                                heater.start_heater(temperature, plc, relay_8)
                        
                    time.sleep(0.5)
                    volt.start_volt(setting_selection)
           

except:
    restart_programs()


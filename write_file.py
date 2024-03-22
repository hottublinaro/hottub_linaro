
class Write_file():


    def start_write(self, relay_8, plc_status, temperature, ph, orp, pressure, plc_in):
        print("writefile open")
        with open('/home/linaro/txt_file/status_relay_8.txt','w') as relay_file:
            relay_file.write(str(relay_8))
            relay_file.close()

        with open('/home/linaro/txt_file/status_plc.txt','w') as plc_file:
            plc_file.write(str(plc_status))
            plc_file.close()

        with open('/home/linaro/txt_file/status_plc_in.txt','w') as plc_file_in:
            plc_file_in.write(str(plc_in))
            plc_file_in.close()

        with open('/home/linaro/txt_file/temperature.txt','w') as temperature_file:
            temperature_file.write(str(temperature))
            temperature_file.close()


        with open('/home/linaro/txt_file/ph.txt','w') as ph_file:
            ph_file.write(str(ph))
            ph_file.close()
        
        with open('/home/linaro/txt_file/orp.txt','w') as orp_file:
            orp_file.write(str(orp))
            orp_file.close()

        with open('/home/linaro/txt_file/pressure.txt','w') as pressure_file:
            pressure_file.write(str(pressure))
            pressure_file.close()
        print("writefile close")

    def write_over_presssure(self,pressure):
        print("writefile pressure open")
        with open('/home/linaro/txt_file/count_down_close_system.txt','w') as pressure_file:
            pressure_file.write(str(pressure))
            pressure_file.close()
        print("writefile pressure close")

    def clear_pressure_time(self):
        with open('/home/linaro/txt_file/count_down_close_system.txt','w') as count_down_read:
            count_down_read.write('')
            count_down_read.close()
    def write_file_datetime_rtc(self, date_time_rtc):
         with open('/home/linaro/txt_file/time_rtc.txt','w') as write_datetime:
            write_datetime.write(date_time_rtc)
            


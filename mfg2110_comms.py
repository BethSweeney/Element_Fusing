import serial

class MFG2110Comms():

    global ser
    def __init__(self, port:str ,baudrate:int, timeout:int):
        self.start_connection(port,baudrate,timeout)
        self.check_name()
        self.check_current_setting()

        #self.send_signal(wave,frequency,amplitude,offset)

## Initialise connection with fg - connect to port
    def start_connection(self, port:str,baudrate:int, timeout:int) -> None: 
        global ser
        try:
            ser = serial.Serial(port,baudrate,timeout=timeout)
            if ser.isOpen:
                print("You are connected to port:" + port)

        except Exception as e:
            print(e)
            try:
                ser.close()
            except:
                print('Connection never established - check port.')
            exit()            


## check name of fg
    def check_name(self) -> None:
        global ser
        try:
            ser.write('*IDN?\n'.encode())
            print('Function Generator name is: ' + ser.readline().decode())

        except Exception as e:
            print(e)
            ser.close()
            exit()


## check current settings of fg
    def check_current_setting(self)-> None:
        global ser
        try:
            ser.write('SOUR1:APPL?\r\n'.encode())
            print('Current Settings are: '+ser.readline().decode())

        except Exception as e:
            print(e)
            ser.close()
            exit()


## Send signal to function generator
    def send_signal(self, wave:str, frequency:str, amplitude:str, offset:str)-> None:
        
        waves = bytes(wave,'utf-8')
        freq = b' '+bytes(frequency,'utf-8')
        amp = b','+bytes(amplitude,'utf-8')
        off_set = b','+bytes(offset,'utf-8')
    
        ser.write(b'SOUR1:APPL:'+waves+freq+amp+off_set+b'\r\n')
        print('Wave:'+wave+'\n'+'Frequency:'+frequency+'\n'+'Amplitude:'+amplitude+'\n'+'DC offset:'+offset+'\n')


## close communication
    def close_comms(self) -> None:
        s.close()
        print("MFG2110Comms: Closed.")



if __name__=="__main__":
    fg = MFG2110Comms(port='COM6',baudrate= 115200, timeout= 6)
            

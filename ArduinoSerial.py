"""
import time

def SetCallbackFromArduino(CallbackClass):
    time.sleep(1)
    CallbackClass.callback()

class arduinocallback:
    receive_data = False
    data = 0

    def __init__(self):
        self.receive_data = False
        self.data = 0

    def callback(self):
        print("callback received!")
        self.receive_data = True
        return

def main():
    ad = arduinocallback()
    SetCallbackFromArduino(ad)
    while(True):
        if(ad.receive_data):
            break
        
    print("wa!")
    return

main()
"""
import serial
import sys
import glob
import msvcrt
class ArduinoSerial:
    ser = None

    def __init__(self):
        self.ser = None

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
    
    def Setup(self):
        list = self.serial_ports()
        if(len(list) == 0):
            input("시리얼 포트가 없습니다. 엔터를 누르면 종료됩니다.")
            return False
        print("시리얼 포트를 선택해주세요.")
        for index, value in enumerate(list, start=1):
            print(str(index) + ". " + value)
        while(True):
            port = int(input(":"))
            if(port > len(list) or port < 1):
                print("다시 입력해주세요.")
            else:
                break

        print("보드레이트를 입력해주세요. (빈칸 입력 시 9600)")
        while(True):
            boardrate_s = input(":")
            try:
                boardrate = int(boardrate_s)
            except ValueError as e:
                if(boardrate_s == ""):
                    boardrate = 9600
                    boardrate_s = "9600"
                break
            if(boardrate > 1):
                break
            print("다시 입력해주세요.")

        print("포트 : " + list[port - 1] + ", 보드레이트 : " + boardrate_s + " 으(로) 연결합니다.")
        try:
            self.ser = serial.Serial(list[port - 1], boardrate)
        except PermissionError as e:
            print("포트를 열 수 없습니다!")
            return False
        return True

    def SetupWithoutSelect(self, serialport, boardrate):
        self.ser = serial.Serial(serialport, boardrate)

    def SendStr(self, str):
        if(self.ser is None):
            return False
        self.ser.write(str.encode())

    #def MoveWithDegree(self, degree):
        


def main():
    arduino = ArduinoSerial()
    arduino.Setup()
    #arduino.SetupWithoutSelect("COM1", 9600)
    while(True):
        key = msvcrt.getch()
        print(key)
        if(key == b'\r'):
            break
        if(key == b' '):
            arduino.SendStr("0.0.0.0.end")
        if(key == b'w'):
            arduino.SendStr("70.70.0.1.end")
        if(key == b'd'):
            arduino.SendStr("0.100.0.1.end")
        if(key == b'a'):
            arduino.SendStr("100.0.0.1.end")
        if(key == b's'):
            arduino.SendStr("70.70.1.0.end")

main()
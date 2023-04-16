import serial
from udp import Transmitter
import time
import threading

class Controller:

    ser = None
    transmitter = None
    active = False
    led_count = None

    def set_serial(self, COM):
        self.ser = serial.Serial(COM.split(" ")[0], 115200, timeout=1)

    def set_transmitter(self, UDP_port, IP):
        self.transmitter = Transmitter(UDP_port, IP)

    def set_led_count(self, count):
        self.led_count = int(count)

    # creates a package to send to wled. first byte is protocol, second byte is timeout duration
    # led data is read over serial com port
    def make_package(self):
        red = self.ser.readline()[:-1]
        return bytearray([2,255])+bytearray(red)
    
    def make_package_alt(self):
        package = bytearray([2, 255])
        end = False
        count = 0
        for i in range (0, self.led_count):
            red = self.ser.read(3)
            count+=1
            package+=red
        self.ser.read()
        #print("COUNT: ", count)
        return package

    def test_udp(self):
        thread = threading.Thread(target=self.transmitter.test_udp, args=(self.led_count,), daemon=True).start()

    def start(self):
        self.active = True
        thread = threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.active = False
        self.ser.close()

    def run(self):
        while(True):
            if not self.active:
                break
            packet = self.make_package_alt()
            self.transmitter.transmit(packet)
            time.sleep(.04)
        print("Quitting...")



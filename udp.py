import socket 
import time
class Transmitter:
    UDP_port = None
    IP = None
    socket = None

    # creates a new transmitter object
    def __init__(self, UDP_port, IP):
        self.UDP_port = int(UDP_port)
        self.IP = IP
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

    # creates a package to send to wled. first byte is protocol, second byte is timeout duration
    def transmit(self, package):
        #print("packet ist:")
        #print(package)
        print (''.join('{:02x}'.format(x) for x in package))
        self.socket.sendto(package, (self.IP, self.UDP_port))

    def test_udp(self):
            length = 56
            for i in range(0, length):
                package = bytearray([2, 2])
                for j in range(0, length):
                    for k in range(0, 3):
                        package.append(100 if i == j else 0)
                self.transmit(package)
                time.sleep(.1)
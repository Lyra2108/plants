from abc import ABC, abstractmethod
from serial import Serial


class Sensor(ABC):

    @abstractmethod
    def measure_raw_value(self):
        pass

    def measure(self):
        raw_value = self.measure_raw_value()
        return (1.0 - (raw_value / 1023.0)) * 100


class USBSensor(Sensor):

    def __init__(self, serial_port, device_port):
        self.serial_port = serial_port
        self.device_port = device_port

    def measure_raw_value(self):
        connection = Serial(self.serial_port, 9600)
        binary_string = str(self.device_port).strip(' ').encode()
        connection.write(binary_string)
        connection.flushOutput()
        return int(connection.readline())

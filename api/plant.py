from serial import Serial


def get_humidity(plant):
    connection = Serial('/dev/ttyUSB0', 9600)
    binary_string = plant.strip(' ').encode()
    connection.write(binary_string)
    connection.flushOutput()
    return (1.0 - (int(connection.readline()) / 1023.0)) * 100

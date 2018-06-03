import serial

connection = serial.Serial('/dev/ttyUSB0', 9600)
connection.write(b'10')
connection.flushOutput()
humidity = int(connection.readline())
print(humidity)

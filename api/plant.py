from serial import Serial


def get_humidity(plant):
    connection = Serial('/dev/ttyUSB0', 9600)
    binary_string = str(plant).strip(' ').encode()
    connection.write(binary_string)
    connection.flushOutput()
    return (1.0 - (int(connection.readline()) / 1023.0)) * 100


class Plant:

    def __init__(self, name, port):
        self.id = port
        self.name = name
        self.port = port

    def get_binary_port(self):
        return '{:d}'.format(self.port).encode()


class Plants:
    plants = [Plant(name='Forelle', port=10), Plant(name='Lilie', port=9)]

    @staticmethod
    def get_plants(query):
        query = query.strip(' ')
        if query.isdigit():
            return [plant for plant in Plants.plants if plant.port == int(query)]
        return [plant for plant in Plants.plants if plant.name.lower().find(query.lower()) > -1]

    @staticmethod
    def get_plant_by_id(plant_id):
        for plant in Plants.plants:
            if plant.id == int(plant_id):
                return plant

    @staticmethod
    def all():
        return Plants.plants

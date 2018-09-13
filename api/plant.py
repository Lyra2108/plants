from gettext import gettext as _

from api.sensor import USBSensor


class Plant:

    def __init__(self, plant_id, name, sensor):
        self.id = plant_id
        self.name = name
        self.sensor = sensor

    def get_humidity(self):
        return self.sensor.measure()

    def get_humidity_display_text(self):
        return _('{0} has a humidity of {1:.0f}%').format(self.name, self.get_humidity())


class Plants:
    plants = [
                 Plant(name='Forelle', plant_id=10, sensor=USBSensor(serial_port='/dev/ttyUSB0', device_port=10)),
                 Plant(name='Lilie', plant_id=9, sensor=USBSensor(serial_port='/dev/ttyUSB0', device_port=9))
             ]

    @staticmethod
    def get_plants(query):
        query = query.strip(' ')
        if query.isdigit():
            return [plant for plant in Plants.plants if plant.id == int(query)]
        return [plant for plant in Plants.plants if plant.name.lower().find(query.lower()) > -1]

    @staticmethod
    def get_plant_by_id(plant_id):
        for plant in Plants.plants:
            if plant.id == int(plant_id):
                return plant

    @staticmethod
    def all():
        return Plants.plants

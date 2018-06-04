from unittest import TestCase

from api.plant import Plant


class TestPlant(TestCase):

    def test_get_binary_port(self):
        plant = Plant(name='test', port=10)

        self.assertEqual(b'10', plant.get_binary_port())

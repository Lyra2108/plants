import pytest

from api.plant import Plants, Plant


@pytest.mark.parametrize("query,expected", [('Minze', ['Minze']),
                                            ('mInZe', ['Minze']),
                                            ('', ['Minze', 'Chili']),
                                            ('i', ['Minze', 'Chili']),
                                            ('chili', ['Chili']),
                                            ('9', ['Chili']),
                                            ('9 ', ['Chili'])])
def test_get_plants(monkeypatch, query, expected):
    monkeypatch.setattr(Plants, "plants", [Plant(name='Minze', port=10), Plant(name='Chili', port=9)])

    plants = Plants.get_plants(query)

    assert [plant.name for plant in plants] == expected


def test_get_all_plants(monkeypatch):
    plants = [Plant(name='test', port=42)]
    monkeypatch.setattr(Plants, "plants", plants)

    assert plants == Plants.all()

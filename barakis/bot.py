from random import randint
from ogame.constants import *


def expedition(empire):
    while len(empire.fleet()) < empire:
        for planet in empire.galaxy(coordinates(randint(1, 6), randint(1, 499))):
            if status.inactive in planet.status:
                for id in empire.get:
                    empire.send_fleet(mission=mission.attack,
                                      id=empire.id_by_planet_name(Hautplanet),
                                      where=planet.position,
                                      ships=[ships.large_transporter(int(24 / (i + 1)))])
                    fleet_send += 1


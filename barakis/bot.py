from random import randint
from ogame.constants import *
from time import sleep

try:
    from settings import *
except ImportError:
    from barakis.settings import *


def expedition(empire):
    for i in range(int(int(empire.research().astrophysics) / 5)):
        empire.send_fleet(
            mission=mission.expedition,
            id=empire.id_by_planet_name(bot_settings['main_planet']),
            where=coordinates(randint(1, 6), randint(1, 499), 16),
            ships=[ships.large_transporter(bot_settings['expedition_large_transporter'])],
            holdingtime=1)


def inactive(empire):
    for i in range(int(empire.research().computer)):
        galaxy = randint(1, 6)
        system = randint(1, 499)
        for planet in empire.galaxy(coordinates(galaxy, system)):
            if status.inactive in planet.status:
                if empire.send_fleet(
                        mission=mission.attack,
                        id=empire.id_by_planet_name(bot_settings['main_planet']),
                        where=planet.position,
                        ships=[ships.large_transporter(int(bot_settings['inactive_large_transporter']))]):
                    print('send Attack')
                else:
                    print('Failed', empire.id_by_planet_name(bot_settings['main_planet']))


def build_mines(empire):
    def compare_resources(planet_resources, cost):
        for a, b in zip(planet_resources, cost):
            if a < b:
                return False
        return True

    def missing_resources(planet_resources, cost):
        dif = []
        for a, b in zip(planet_resources, cost):
            if a - b < 0:
                dif.append(b - a)
            else:
                dif.append(0)
        return dif

    main_resources = empire.resources(empire.id_by_planet_name(bot_settings['main_planet'])).resources
    main_ships = empire.ships(empire.id_by_planet_name(bot_settings['main_planet']))
    ids = empire.planet_ids()

    for id in ids:
        supply = empire.supply(id)
        local_res = empire.resources(id)
        vessels = empire.ships(id)
        # send fleet for mines
        needed_resources = missing_resources(local_res.resources, supply.crystal_mine.cost)
        needed_large_transporter = ships.large_transporter(int(sum(needed_resources) / 46250) + 1)
        if compare_resources(main_resources, needed_resources) \
                and main_ships.large_transporter > ships.ship_amount(needed_large_transporter) + 1 \
                and not supply.crystal_mine.in_construction \
                and not supply.metal_mine.in_construction \
                and not supply.deuterium_mine.in_construction:
            if empire.send_fleet(
                    mission=mission.transport,
                    id=empire.id_by_planet_name(bot_settings['main_planet']),
                    where=empire.celestial_coordinates(id),
                    ships=[needed_large_transporter],
                    resources=needed_resources):
                main_resources = empire.resources(empire.id_by_planet_name(bot_settings['main_planet'])).resources
                main_ships = empire.ships(empire.id_by_planet_name(bot_settings['main_planet']))
            else:
                main_resources = empire.resources(empire.id_by_planet_name(bot_settings['main_planet'])).resources

        max_crawler = int((supply.metal_mine.level + supply.crystal_mine.level + supply.deuterium_mine.level) * 8)
        if supply.crystal_mine.is_possible:
            empire.build(buildings.crystal_mine, id)
        elif supply.metal_mine.is_possible:
            empire.build(buildings.metal_mine, id)
        elif local_res.energy < 0:
            empire.build(buildings.solar_satellite(20), id)
        elif local_res.energy > 0 and max_crawler > vessels.crawler:
            empire.build(buildings.crawler(5), id)
        elif supply.deuterium_mine.is_possible:
            empire.build(buildings.deuterium_mine, id)


def start_tasks(empire):
    if bot_settings['expedition'] == 'checked':
        expedition(empire)
    if bot_settings['build_mines'] == 'checked':
        build_mines(empire)
    if bot_settings['inactive'] == 'checked':
        inactive(empire)


def worker(empire):
    while True:
        if bot_settings['repeat'] == '0':
            continue
        start_tasks(empire)
        sleep(int(bot_settings['repeat']) * 60)

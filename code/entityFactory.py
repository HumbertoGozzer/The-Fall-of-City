#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.background import Background
from code.const import WIN_HEIGHT
from code.enemy import Enemy
from code.player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:

            case 'onda1' | 'onda2' | 'onda3' | 'bossfight':
                return [Background(f'Background/{entity_name}', position)]
            case 'Player':
                return [Player('Soldier/idle', position=(10, WIN_HEIGHT / 2 ))]
            case 'Enemy':
                return [Enemy('Zombie/Zb1Idle', position)]
            case _:
                return []

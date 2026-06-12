#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.background import Background

class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0,0)):
        match entity_name:
            case 'onda1':
                list_bg = [Background('onda1', position)]

                return list_bg

            case 'onda2':
                list_bg = [Background('onda2', position)]

                return list_bg

            case 'onda3':
                list_bg = [Background('onda3', position)]

                return list_bg

            case 'bossfight':
                list_bg  = [Background('bossfight', position)]

                return list_bg

            case _:
                
                return []

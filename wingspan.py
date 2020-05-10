#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:07:24 2020

@author: sgurvets
"""

#backend of the boardgame (wingspan) clone
#classes needed:
#players
#card
#board
#resources/birdfeeder
#deck of cards


import csv
import pandas as pd
import matplotlib.pyplot as plt

from enum import Enum, IntEnum
from random import randint


#resource attributes

class FoodEnum(Enum):
    WHEAT = 'wheat'
    BERRY = 'berry'
    WORM = 'worm'
    RAT = 'rat'
    FISH = 'fish'
    
#card attributes
class HabitatEnum(Enum):
    FOREST = 'forest'
    PLAINS = 'plains'
    WATER = 'water'
    
class NestEnum(Enum):
    BOWL = 'bowl'
    STICK = 'stick'
    PEBBLE = 'pebble'
    HOLE = 'hole'
    STAR = 'star'
    
class PowerEnum(Enum):
    BROWN = 'brown'
    PINK = 'pink'
    PLAYED = 'played'
    
class EggCapacityEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    
class PointValueEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    
class Card:    
    def __init__(self,card_name='Indigo Bunting',
                 habitat=HabitatEnum('forest'), 
                 cost_string = 'wo',
                 point_value = PointValueEnum(1),
                 nest=NestEnum('bowl'), 
                 egg_capacity=EggCapacityEnum(1), 
                 wingspan = 35,
                 power_type = PowerEnum('brown')
                 ):
        self.card_name = card_name
        self.habitat = habitat
        self.cost = cost_string
        self.point_value = point_value
        self.nest = nest
        self.egg_capacity = egg_capacity
        self.wingspan = wingspan
        self.power_type = power_type
        
    def display(self):
        print('Card Name = '+str(self.card_name))
        print('Habitat = '+str(self.habitat.name))
        
        
class DeckManager:
    def __init__(self, auto_deck = False):
        #auto deck makes cards combinatorially
        #import cards gets bird data from the BirdData class
        self.full_deck = []
        if auto_deck == True:
            self.full_deck = self.create_deck(deck=[])
        
    def import_card(self, card):
        self.full_deck.append(card)
        
    def import_deck(self, deck):
        self.full_deck = deck
        
    def create_deck(self,deck = []):
        for habitat in HabitatEnum:
            for nest in NestEnum:
                deck.append(Card(HabitatEnum(habitat),NestEnum(nest),1,1))
        return deck
    
    def draw_card(self):
        rand_card_num = randint(0, len(self.full_deck)-1)
        return self.full_deck.pop(rand_card_num)
            
#board attributes
class ColEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    
class RowEnum(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    
class BoardSquareState(Enum):
    EMPTY = 'empty'
    FILLED = 'filled'
    
class BoardManager:
    def __init__(self):
        self.board = self.create_board()
        
    def create_board(self, board={}):
        for row in RowEnum:
            for col in ColEnum:
                board[(row,col)] = BoardSquareState.EMPTY
        return board
    
#player attributes
        #dist representing the cards a player has  in hand
        #keys are the card name
        #value are the card object
class PlayerHandDict(dict):
    def remove_card_by_name(self,card_name):
        del self[card_name]
        
    def add_card_by_name(self, card_name, card):
        self[card_name] = card
        
#dict representing the food resources the player has gathered
#each resource is  a key and the amount is the value
class PlayerFoodDict(dict):
    def __init__(self):
        super().__init__()
        for food in FoodEnum:
            self[food]=0
            
    def add_food(self, food_enum):
        self[food_enum]+=1
        
    def remove_food(self, food_enum):
        self[food_enum] -= 1
        
class BirdData:
    def __init__(self, filename="/Users/sgurvets/Downloads/Birds.csv"):
        self.card_array = []
        self.df = pd.read_csv(filename)
        self.column_array = self.get_columns(df=self.df)
        

    def get_columns(self, df):
        return [i for i in df.keys()]
    
    def convert_df_to_cards(self, df):
        card_array = []
        for row_num in range(len(df.index)):
            row = df.iloc[row_num]
            card = self.convert_row_to_card(row)
            card_array.append(card)
        return card_array
            
    def convert_row_to_card(self,row):
        card_name = row.Name
        habitat_array = self.get_habitats(row['Habitat'])
        cost_string = self.get_cost(row['Cost'])
        point_value = row['Point Value']
        nest_array = self.get_nest_array(row['Nest Type'])
        nest_capacity = row['Nest Capacity']
        wingspan = row['Wingspan']
        power_type = self.get_power_array(row['Power Type'])
        
        card = Card(card_name=card_name,
                    habitat=habitat_array, 
                    cost_string=cost_string,
                    point_value=point_value, 
                    nest=nest_array, 
                    egg_capacity=nest_capacity, 
                    wingspan=wingspan,
                    power_type=power_type)
        return card
    
        
    def get_habitats(self, habitat_string):
        habitat_array = []
        for i in ['forest', 'water', 'plains']:
            if i in habitat_string:
                habitat_array.append(HabitatEnum(i))
        return habitat_array
    
    def get_nest_array(self, nest_string):
        nest_array = []
        for i in ['bowl','star','hole','pebble','stick']:
            if i in nest_string:
                nest_array.append(NestEnum(i))
        return nest_array
    
    def get_power_array(self, power_string):
        power_array = []
        for i in ['pink', 'brown', 'played']:
            if i in power_string:
                power_array.append(PowerEnum(i))
        return power_array
    
    def get_cost(self, cost_string):
        #TODO come up with something
#        cost_array = []
#        for i in []
        return cost_string
    
class GameManager:
    def __init__(self):
        
        self.bd = BirdData(filename="/Users/sgurvets/Downloads/Birds.csv")
        deck = self.bd.convert_df_to_cards(self.bd.df)
        self.dm = DeckManager(auto_deck = False)
        self.dm.import_deck(deck)
            
    def deal_open(self):
        phd = PlayerHandDict()
        for i in range(5):
            card = self.dm.draw_card()
            phd.add_card_by_name(card.card_name, card)
        return phd
        
            
        
        

        
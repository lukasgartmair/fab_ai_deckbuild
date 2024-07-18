#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:59:26 2023

@author: lukasgartmair
"""

import sqlite3

def initialize_db_connection():

    con = sqlite3.connect("database/cards.db")
    
    cur = con.cursor()

    return cur

def get_cards(cur):

    res = cur.execute("SELECT * FROM CARD")
    
    cards = res.fetchall()
    
    return cards

def parse_results(results):
    
    parsed_results = [c[0].split(",") for c in results]
    
    return parsed_results

def get_cards_from_database():
    
    cur = initialize_db_connection()
    
    cards = get_cards(cur)
    
    cards = parse_results(cards)
    
    return cards
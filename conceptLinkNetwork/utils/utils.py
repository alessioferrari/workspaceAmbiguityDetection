'''
Created on Oct 30, 2014

@author: alessioferrari
'''
import csv
import logging
import os

FLOAT = 'FLOAT'
INT = 'INT'
    
def store_dict_in_csv(dict, file_path):
    w = csv.writer(open(file_path, "w"))
    for key, val in dict.items():
        w.writerow([key, val])
            
def read_dict_from_csv(file_path, data_type):
    dict = {}
    if data_type == FLOAT:
        for key, val in csv.reader(open(file_path)):
            dict[key] = float(val)
    elif data_type == INT:
        for key, val in csv.reader(open(file_path)):
            dict[key] = int(val)
    else:
        for key, val in csv.reader(open(file_path)):
            dict[key] = val        
    return dict

def create_folder(input_path):
    if not os.path.exists(input_path):
        os.makedirs(input_path) 
        
        
def start_logger(name, file_path):
        logger = logging.getLogger(name) 
        hdlr = logging.FileHandler(file_path, mode="w")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(logging.INFO)
        return logger 
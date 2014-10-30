'''
Created on Oct 30, 2014

@author: alessioferrari
'''
import csv


    
def store_dict_in_csv(dict, file_path):
    w = csv.writer(open(file_path, "w"))
    for key, val in dict.items():
        w.writerow([key, val])
            
def read_dict_from_csv(file_path):
    dict = {}
    for key, val in csv.reader(open(file_path)):
        dict[key] = val
            
    return dict
import csv
import sys

#edit configuration in Configs.py
from Configs import *

#cardDB is the data base file containing cards details.
f = open(cardsDB, 'rt')

try:
    reader = csv.reader(f)
    for row in reader:
        print row
        #first line in the csv file should be skipped or deleted

        #acess each element in each row separetly in the csv file
        rowLength = len(row)
        print rowLength		
        for i in range(rowLength):
            print row[i]

        #sample call to the gimp script		

finally:
    f.close()

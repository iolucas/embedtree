import csv

import sys

from sklearn.cluster import KMeans

from myutils import *

article_title = sys.argv[1]
transversal_level = sys.argv[2]

filename = "results4/" + article_title + "-" + transversal_level + ".csv"

data = open_csv(filename)[2:]

for row in data:
    print row


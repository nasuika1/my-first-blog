import ChartMaker
import numpy as np
import csv
import Time_Sort
import Skill_Chart
with open('./データ/Chart/東京テディベア.csv') as f:
	reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
	l = [row for row in reader]
#num = int(l[-1][-2]//8)+1
#Skill_Chart.Make_Chart(l,num,'東京テディベア')
#ChartMaker.Make_Chart(l,num,'./データ/Chart/カレンデュラ')
W = Time_Sort.T_Sort(l)
with open('./データ/Chart/東京テディベア.csv','w') as f:
	writer = csv.writer(f)
	writer.writerows(W)
'''
with open('東京テディベア.csv') as f:
	reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
	l = [row for row in reader]
print(l)
'''

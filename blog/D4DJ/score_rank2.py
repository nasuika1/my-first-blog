import Skill_Chart
import csv
import Time_Sort
import Calc_Score
music = "medley2"

with open('./データ/Chart/'+str(music)+'.csv') as f:
	reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
	chart_info = [row for row in reader]
chart_info = Time_Sort.T_Sort(chart_info)
with open('./データ/Chart/'+str(music)+'_signature.csv') as f:
	reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
	sign_info = [row for row in reader]
	sign_info = sign_info[0]

skill_info = Skill_Chart.Make_Chart(chart_info,int(chart_info[-1][-2]//8+1),'./データ/Chart/'+music+'_skill',music = music,t_bool=False)

diff = 12

a_power = 155186
s1 = 30
s2 = 40
s3 = 40
s4 = 50
start =[0,0,0,0,0]
end = [0,0,0,0,0]
gre=[]
go=[]

print(Calc_Score.Calc_Score(skill_info,diff,a_power,s1,s2,s3,s4,start_add = start,end_add = end,Great=gre,Good=go))

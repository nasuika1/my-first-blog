import csv
import numpy as np
import ChartMaker
import Crip
import itertools
import Skill_Chart
import Calc_Score
import find_party
from PIL import Image, ImageDraw, ImageFont, ImageOps


def csv_mod_read_row(path,idx):
	with open(path) as f:
		reader = csv.reader(f)
		for row in reader:
			if reader.line_num - 1 == idx:
				return row
	return None

#カードクラス
class Card:
	def __init__(self,card_list,num):
		self.num  = num+1
		self.name = card_list[num][1]
		self.card = card_list[num][3]
		self.hart = int(card_list[num][5])
		self.tech = int(card_list[num][6])
		self.phis = int(card_list[num][7])
		self.power = self.hart+self.tech+self.phis
		self.typ  = card_list[num][4]
		self.skill= int(card_list[num][9])
		self.unit = card_list[num][2]

#曲クラス
class Music:
	def __init__(self,num):
		self.music_info = csv_mod_read_row('./データ/d4dj_music.csv',num)
		self.music_name = self.music_info[1]
		self.music_long = self.music_info[4]
		self.medley_loc = [[float(self.music_info[10]),float(self.music_info[11])],[float(self.music_info[12]),float(self.music_info[13])],[float(self.music_info[14]),float(self.music_info[15])]]
#譜面クラス
class Chart(Music):
	def __init__(self,num,dif):
		super().__init__(num)
		self.chart_info = None
		self.sign_info = None
		if(dif == 'ex'):
			self.diff = float(self.music_info[8])
			with open('./データ/Chart/'+str(self.music_info[1])+'.csv') as f:
				reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
				self.chart_info = [row for row in reader]
			with open('./データ/Chart/'+str(self.music_info[1])+'_signature.csv') as f:
				reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
				self.sign_info = [row for row in reader]
				self.sign_info = self.sign_info[0]
			try:
				with open('./データ/Chart/'+self.music_name+'_skill.csv') as f:
					reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
					self.skill_info = [row for row in reader]
			except:
				self.skill_info = Skill_Chart.Make_Chart(self.chart_info,int(self.chart_info[-1][-2]//8+1),'./データ/Chart/'+self.music_name+'_skill',music = self.music_name,t_bool=False)
		elif(dif == 'ha'):
			self.diff = float(self.music_info[7])
		elif(dif == 'no'):
			self.diff = float(self.music_info[6])
		elif(dif == 'ea'):
			self.diff = float(self.music_info[5])
		else:
			self.diff = None
	def Chart_show(self):
		try:
			im = Image.open('./データ/Chart/'+self.music_name+'.png')
			im.show()
		except:
			ChartMaker.Make_Chart(self.chart_info,int(self.chart_info[-1][-2]//8+1),'./データ/Chart/'+self.music_name,t_bool = True,sign=self.sign_info)

	def Skill_Chart_show(self):
		try:
			im = Image.open('./データ/Chart/'+self.music_name+'_skill.png')
			im.show()
		except:
			Skill_Chart.Make_Chart(self.chart_info,int(self.chart_info[-1][-2]//8+1),'./データ/Chart/'+self.music_name+'_skill',music = self.music_name,t_bool=True)
	def Score(self,a_power,s1,s2,s3,s4):
		return Calc_Score.Calc_Score(self.skill_info,self.diff,a_power,s1,s2,s3,s4)	
#メドレークラス
class Medley:
	def __init__(self,m1,m2,m3,m4,s_l = None):
		self.m1 = m1
		self.m2 = m2
		self.m3 = m3
		self.m4 = m4
		self.skill_loc = s_l
		self.chart_info = Medley_Chart([m1,m2,m3,m4],s_l = self.skill_loc)
		self.skill_info = Skill_Chart.Make_Chart(self.chart_info,int(self.chart_info[-1][-2]//8+1),'test')
		self.diff = None
	def Chart_show(self):
		self.chart_info = Medley_Chart([self.m1,self.m2,self.m3,self.m4],s_l = self.skill_loc)
		ChartMaker.Make_Chart(self.chart_info,int(self.chart_info[-1][-2]//8+1),'test',t_bool=True)
	def Skill_Chart_show(self):
		self.skill_info = Skill_Chart.Make_Chart(self.chart_info,int(self.chart_info[-1][-2]//8+1),'test',music_1=self.m1.music_name,music_2=self.m2.music_name,music_3=self.m3.music_name,music_4=self.m4.music_name,t_bool = True)
	def Score(self,a_power,s1,s2,s3,s4):
		return Calc_Score.Calc_Score(self.skill_info,self.diff,a_power,s1,s2,s3,s4)
#イベントクラス
class Event:
	def __init__(self,e_type = None,e_chara = [],A_s = 0):
		self.e_type = e_type
		self.e_chara = e_chara
		self.Assignment_song = Chart(A_s,'ex')
		self.party_list = "Not Calcurate"
		self.ideal_party = "Not Calcurate"

	def Calc(self):
		self.party_list= self.card_open(self.e_type,self.e_chara)
		self.ideal_party = self.party_list[0]

	def card_open(self,e_type,e_chara):
		with open('./データ/d4djcard.csv') as f:
			reader = csv.reader(f)
			card_list = [row for row in reader]
		self.All_card = []
		for i in range(len(card_list)):
			self.All_card += [Card(card_list,i)]
		del card_list
		return find_party.Find_party(self.All_card,self.e_type,self.e_chara,self.Assignment_song)
		
	def Party_Print(self,t = 1):
		self.party = self.party_list[t-1]
		if(self.ideal_party == "Not Calcurate"):
			return
		layout = ["モニター","DJブース","ディスクL","ディスクR","フロント","サイド","バック","フレーム","ライト","アクセサリ"]
		print("メイン編成")
		max_mem = ""
		max_power = 0
		for i in range(4):
			a = self.All_card[self.party[1][i]]
			print(a.name,a.card,a.typ,a.skill)
			if(max_power < a.power):
				max_power = a.power
				max_mem = a.name
		print("サポート編成")
		for j in range(4):
			a = self.All_card[self.party[1][j+4]]
			print(a.name,a.card,a.typ,a.skill)
		print("総合力")
		print(self.party[0])
		print("レイアウト")
		print("ユニット配置:"+self.party[2])
		print("ディスクスキン:"+max_mem)

def Skill_Relocate(c,skill_loc = None):
	skill_id   = []
	delete_id = []
	music_num = 1
	for i in range(len(c)):
		if(c[i][0] == 0):
			skill_id += [[i,music_num]]
		elif(c[i][0] == -1):
			delete_id += [i]
			music_num += 1
	if(len(skill_id) == 5):
		for i in range(len(delete_id)-1):
			del c[delete_id[len(delete_id)-i-2]]
		return c
	elif(len(skill_id) > 5):
		s_Conb = [1,2,3,4,5]
		if(skill_loc != None):
			s_Conb = skill_loc
		for i in range(len(skill_id)):
			print(c[skill_id[i][0]])
			if(not(i+1 in s_Conb)):
				delete_id += [skill_id[i][0]]
		delete_id.sort()
		for i in range(len(delete_id)-1):
			del c[delete_id[len(delete_id)-i-2]]
		return c
		
	else:
		#S3とS4のちょうど時間的真ん中
		s_time = (c[skill_id[3][0]][3]+c[skill_id[2][0]][3])/2
		for i in range(len(c)-1):
			if(c[i][3] <= s_time <= c[i+1][3]):
				s_bar = int(((s_time-c[i][3])/(c[i+1][3]-c[i][3])*(c[i+1][2]-c[i][2])+c[i][2])*256)/256
				c = c[:i+1]+[[0,0,s_bar,s_time]]+c[i+1:]
				break
		return c
def Medley_Chart(medley_chart,s_l = None):
	Medley_1 = Crip.Cripping(medley_chart[0].chart_info,medley_chart[0].medley_loc[0],[8,0])
	Medley_2 = Crip.Cripping(medley_chart[1].chart_info,medley_chart[1].medley_loc[1],Medley_1[-1][2:])
	Medley_3 = Crip.Cripping(medley_chart[2].chart_info,medley_chart[2].medley_loc[1],Medley_2[-1][2:])
	Medley_4 = Crip.Cripping(medley_chart[3].chart_info,medley_chart[3].medley_loc[2],Medley_3[-1][2:])
	Medley_chart = Medley_1[:-1]+Medley_2[:-1]+Medley_3[:-1]+Medley_4
	Medley_test = Medley_1+Medley_2+Medley_3+Medley_4
	Medley_chart = Skill_Relocate(Medley_test,skill_loc = s_l)
	#ChartMaker.Make_Chart(Medley_chart[:-1],int(Medley_chart[-1][2]//8),'test')
	#Skill_Chart.Make_Chart(Medley_chart[:-1],int(Medley_chart[-1][2]//8),'skill_test',music_1=medley_chart[0].music_name,music_2=medley_chart[1].music_name,music_3=medley_chart[2].music_name,music_4=medley_chart[3].music_name)
	return Medley_chart[:-1]
e = Event(e_type="パーティ",e_chara=["青柳椿","桜田美夢","三宅葵依","竹下みいこ"])
e.Calc()
for i in range(30):
	print(str(30-i)+"番目")
	e.Party_Print(t=30-i)


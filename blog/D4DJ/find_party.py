import itertools
import Calc_Score

def Party_Calc(p_l,s_l,chart):
	Score = []
	for i in itertools.combinations(p_l,4):
		member = []
		for j in range(4):
			if(not(i[j][-1] in member)):
				member += [i[j][-1]]
		if(len(member) != 4):
			continue
		support_count = 0
		while len(member) < 8 and support_count < len(s_l):
			if(not(s_l[support_count][-1] in member)):
				member += [s_l[support_count][-1]]
				i += tuple([s_l[support_count]])
			support_count += 1
		party_power = 0
		party_skill = []
		for j in range(4):
			party_power += i[j][2]+i[j][3]+i[j][4]+i[j+4][5]
			party_skill += [i[j][6]]
		Score +=[[Calc_Score.Calc_Score(chart.skill_info,chart.diff,party_power,party_skill[0],party_skill[1],party_skill[2],party_skill[3])[-1][1],list(i)]]
	Score = sorted(Score,reverse = True,key = lambda x:x[0])
	Score = Score[:30]
	
	return Score
def Output_power(All_Score,unit,e_type,e_chara,All_c,chart):
	po_pa_it = []
	for i in range(len(All_Score)):
		main_p = sorted(All_Score[i][1][:4],reverse=True,key = lambda x:x[2])
		main_p_num = [x[0] for x in main_p]
		support_p = All_Score[i][1][4:]
		support_p_num = [x[0] for x in support_p]
		po_pa_it += [[0,0,0]]
		skill = []
		for j in range(7):
			power = 0
			add_c = 1
			for k in main_p_num:
				add_e = 0
				add_a = (j//6)*0.16
				add_c *= 0.24
				if(All_c[k].name in e_chara):
					add_e += 0.2
				if(All_c[k].typ == e_type):
					add_e += 0.2
				if(All_c[k].unit == unit[j%6]):
					add_a += 0.24 - (j//6)*0.24
				elif(All_c[k].typ == e_type):
					if(j < 6):
						add_a += 0.03
					else:
						add_a += 0.01
				chara_b = int(All_c[k].hart*add_e)+int(All_c[k].tech*add_e)+int(All_c[k].phis*add_e)
				area_b = int(All_c[k].hart*(add_a+add_c))+int(All_c[k].tech*(add_a+add_c))+int(All_c[k].phis*(add_a+add_c))
				power += All_c[k].hart+All_c[k].tech+All_c[k].phis+chara_b+area_b
				skill += [All_c[k].skill]
				add_c *= 0
			for k in range(len(support_p)):
				power += support_p[k][5]
			if(po_pa_it[i][0] < power):
				po_pa_it[i][0] = power
				po_pa_it[i][1] = main_p_num+support_p_num
				if(j < 6):
					po_pa_it[i][2] = unit[j]
				else:
					po_pa_it[i][2] = "全て"
		po_pa_it[i] += [Calc_Score.Calc_Score(chart.skill_info,chart.diff,po_pa_it[i][0],skill[0],skill[1],skill[2],skill[3])[-1][1]]
	po_pa_it = sorted(po_pa_it,reverse= True, key=lambda x:x[3])
	ppi_list = [x[0:3] for x in po_pa_it]
	return ppi_list
			
			
def Find_party(All_c,e_type,e_chara,chart):
	unit = ["Happy Around","Peaky P-key","Photon Maiden","merm4id","燐舞曲","Lyrical Lily","すべて"]
	All_Score = []
	for i in range(7):
		Power_list = []
		for j in range(len(All_c)):
			chara_b = 0
			area_b = 0
			add_e = 0
			add_a = (i//6)*0.16
			if(All_c[j].name in e_chara):
				add_e += 0.2
			if(All_c[j].typ == e_type):
				add_e += 0.2
			if(All_c[j].unit == unit[i%6]):
				add_a += 0.24 - (i//6)*0.24
			elif(All_c[j].typ == e_type):
				if(i < 6):
					add_a += 0.03
				else:
					add_a += 0.01

			chara_b = int(All_c[j].hart*add_e)+int(All_c[j].tech*add_e)+int(All_c[j].phis*add_e)
			area_b = int(All_c[j].hart*add_a)+int(All_c[j].tech*add_a)+int(All_c[j].phis*add_a)
			support = All_c[j].hart//4+All_c[j].tech//4+All_c[j].phis//4
			Power_list += [[j,((1+All_c[j].skill/100)*9/120+1)*(All_c[j].power+chara_b+area_b),All_c[j].power,chara_b,area_b,support,All_c[j].skill,All_c[j].name]]

		Power_list = sorted(Power_list,reverse = True, key = lambda x:x[1])
		Support_list = sorted(Power_list,reverse = True, key = lambda x:x[2])
		pick = 20
		while True:
			score = Party_Calc(Power_list[:pick],Support_list,chart)
			pick += 5
			if(len(score) > 0):
				break
		All_Score += score
		All_Score = sorted(All_Score,reverse=True, key=lambda x:x[0])
		All_Score = All_Score[:30]
	return Output_power(All_Score,unit,e_type,e_chara,All_c,chart)


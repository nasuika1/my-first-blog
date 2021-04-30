import numpy as np
import itertools

def Calc_Score(c,diff,a_power,s1,s2,s3,s4,start_add = [0,0,0,0,0],end_add = [0,0,0,0,0],Great=[],Good=[],Auto = False):
	score_array = np.zeros(int(c[0][0]))
	base_score = a_power/len(score_array)*(1+(diff-5)/100)*3
	score_array += base_score
	combo_rate = np.array([1.0]*int(c[0][0]))
	skill_rate = np.array([1.0]*int(c[0][0]))
	judge_rate = np.array([1.0]*int(c[0][0]))
	s = np.array([s1,s2,s3,s4])
	s_max = np.max(s)
	if(Auto):
		combo_rate = 0.81
	else:
		for i in range(len(combo_rate)):
			if(i < 20):
				combo_rate[i] *= 1
			elif(i < 50):
				combo_rate[i] *= 1.01
			elif(i < 300):
				combo_rate[i] = 1 + (1+i//50)/100
			elif(i < 700):
				combo_rate[i] = 1 + (4+i//100)/100
			elif(700 <= i):
				combo_rate[i] = 1.11
	for i in range(len(Great)):
		judge_rate[Great[i]-1] = 0.9
	for i in range(len(Good)):
		judge_rate[Good[i]-1] = 0.8
	skill_score = []
	for i in itertools.permutations(s):
		skill_rate = skill_rate**0
		i += tuple([s_max])
		for j in range(5):
			skill_rate[int(c[1][j])-1-start_add[j]:int(c[2][j])+end_add[j]] = 1+i[j]/100
		skill_score += [[list(i),skill_rate]]
	for i in range(len(skill_score)):
		score = score_array*combo_rate*judge_rate*skill_score[i][1]
		skill_score[i][1] = np.sum(score.astype('int64'))
	skill_score = sorted(skill_score,reverse = False, key = lambda x:x[1])
	for i in range(23):
		if(skill_score[23-i] == skill_score[22-i]):
			del skill_score[23-i]
	return skill_score

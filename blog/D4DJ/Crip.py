import csv
import numpy as np

def Cripping(s,locate,offset):
	start = locate[0]*8
	cripping_time   = locate[1]*8-start
	cripped_chart = [[-1,0,0],[-1,0,cripping_time]]
	for i in range(len(s)):
		cripped_chart += [[s[i][0],s[i][1],s[i][2]-start]]
	del s
	cripped_chart = sorted(cripped_chart,reverse=False, key= lambda x:x[2])
	time = offset[1]
	BPM = 100
	if(cripped_chart[0][0] >= 10):
		BPM = cripped_chart[0][0]
	cripped_chart[0] += [0.0]
	start_id = -1
	end_id = -1
	for i in range(1,len(cripped_chart)):
		if(cripped_chart[i-1][2] >= 0):
			time += 30/BPM*(cripped_chart[i][2]-cripped_chart[i-1][2])
		if(cripped_chart[i][0] >= 10):
			BPM = cripped_chart[i][0]
		if(cripped_chart[i][0] == -1):
			if(start_id >= 0):
				end_id = i
			else:
				start_id = i
		cripped_chart[i] += [time]
	Re_cripped_chart = cripped_chart[start_id+1:end_id+1]
	LorH = []
	for i in range(start_id):
		if(cripped_chart[i][0] == 8 or cripped_chart[i][0] == 9):
			LorH += [cripped_chart[i]]
	exit_LH = []
	count = 0
	while len(LorH) != len(exit_LH) :
		before = LorH[count]
		t = True
		for i in range(count+1,len(LorH)):
			if(before[1] == LorH[i][1]):
				del LorH[i]
				del LorH[0]
				t = False
				break
		if(t):
			exit_LH += [LorH[count]]
			count += 1
	del LorH
	for i in range(len(exit_LH)):
		for j in range(len(Re_cripped_chart)):
			if(exit_LH[i][:2] == Re_cripped_chart[j][:2]):
				del Re_cripped_chart[j]
				break
	LorH = []
	for i in range(len(cripped_chart)):
		if(cripped_chart[len(cripped_chart)-i-1][0] == 8 or cripped_chart[len(cripped_chart)-i-1][0] == 9):
			LorH += [cripped_chart[len(cripped_chart)-i-1]]
		elif(cripped_chart[len(cripped_chart)-i-1][0] == -1):
			break
	exit_LH = []
	count = 0
	while len(LorH) != len(exit_LH) :
		before = LorH[count]
		t = True
		for i in range(count+1,len(LorH)):
			if(before[1] == LorH[i][1]):
				del LorH[i]
				del LorH[0]
				t = False
				break
		if(t):
			exit_LH += [LorH[count]]
			count += 1
	del LorH
	for i in range(len(exit_LH)):
		for j in range(len(Re_cripped_chart)):
			if(exit_LH[i][:2] == Re_cripped_chart[len(Re_cripped_chart)-j-1][:2]):
				del Re_cripped_chart[len(Re_cripped_chart)-j-1]
				break
	del exit_LH
	del cripped_chart
	for i in range(len(Re_cripped_chart)):
		if(4 <= Re_cripped_chart[i][0] <= 7):
			if(Re_cripped_chart[i][0] == 5):
				del Re_cripped_chart[i]
			break
	sly_id = []
	for i in range(len(Re_cripped_chart)):
		if(4 <= Re_cripped_chart[-1*(i+1)][0] <= 7):
			sly_id += [i]
		if(len(sly_id) >= 2):
			if(Re_cripped_chart[-1*(sly_id[0]+1)][0] == 4):
				if(Re_cripped_chart[-1*(sly_id[1]+1)][0] == 4):
					Re_cripped_chart[-1*(sly_id[0]+1)][0] = 5
				else:
					del Re_cripped_chart[-1*(sly_id[0]+1)]
			break
	if(len(sly_id) == 1):
		del Re_cripped_chart[-1*(sly_id[0]+1)]
	for i in range(len(Re_cripped_chart)):
		Re_cripped_chart[i][2] += offset[0]
	return Re_cripped_chart

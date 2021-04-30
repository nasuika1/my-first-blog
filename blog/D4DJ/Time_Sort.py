def T_Sort(s):
	W = []
	signature = 4
	try:
		for i in range(len(s)):
			for j in range(len(s[i])):
				W +=[[s[i][j][0],s[i][j][1],s[i][j][2]+8*i]]
	except:
		for i in range(len(s)):
			W += [[s[i][0],s[i][1],s[i][2]]]
	a = sorted(W, reverse=False, key=lambda x:x[2])
	time = 0
	BPM = 100
	if(a[0][0] >= 10):
		BPM = a[0][0]
	a[0] += [0.0]
	for i in range(1,len(a)):
		time += 30/BPM*(a[i][2]-a[i-1][2])
		if(a[i][0] >= 10):
			BPM = a[i][0]
		a[i] += [time]
	return a

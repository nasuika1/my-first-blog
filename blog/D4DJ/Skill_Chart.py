from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import csv

def Skill_Line(draw,time):
	off = time*100
	draw.line((20,10+off,160,10+off),fill=(200,0,0))

def Note_1(draw,time,y):
	off = time*100
	draw.rectangle((21+y*20,5+off,39+y*20,15+off),fill=(90,184,221))

def Note_2(draw,time,y):
	off = time*100
	draw.rectangle((21+y*20,5+off,39+y*20,15+off),fill=(47,105,214))

def Scrach(draw,time,y):
	off = time*100
	draw.ellipse((21+y*20,3+off,39+y*20,17+off),fill=(240,150,41))

def Long(draw,before,after):
	b_off = before[3]*100
	a_off = after[3]*100
	b_y  = before[1]
	a_y  = after[1]
	draw.rectangle((23+b_y*20,10+b_off,37+a_y*20,10+a_off),fill=(255,242,178))
	draw.rectangle((21+b_y*20,5+b_off,39+b_y*20,15+b_off),fill=(255,222,76))
	draw.rectangle((21+a_y*20,5+a_off,39+a_y*20,15+a_off),fill=(255,222,76))

def Hold(draw,before,after):
	b_off = before[3]*100
	a_off = after[3]*100
	b_y  = before[1]
	a_y  = after[1]
	draw.rectangle((23+b_y*20,10+b_off,37+a_y*20,10+a_off),fill=(255,135,112))
	draw.ellipse((21+b_y*20,3+b_off,39+b_y*20,17+b_off),fill=(255,75,35))
	draw.ellipse((21+a_y*20,3+a_off,39+a_y*20,17+a_off),fill=(255,75,35))

def Slider(draw,before,after):
	b_off = before[3]*100
	a_off = after[3]*100
	b_y  = before[1]
	a_y  = after[1]
	draw.line((30+b_y*20,10+b_off,30+a_y*20,10+a_off),fill=(255,175,243),width=3)
	draw.rectangle((27+b_y*20,1+b_off,33+b_y*20,19+b_off),fill=(255,112,233))
	draw.rectangle((27+a_y*20,1+a_off,33+a_y*20,19+a_off),fill=(255,112,233))
	if(after[0] == 6):
		draw.polygon(((35+a_y*20,1+a_off),(40+a_y*20,1+a_off),(43+a_y*20,10+a_off),(40+a_y*20,19+a_off),(35+a_y*20,19+a_off),(38+a_y*20,10+a_off)),fill=(255,112,233))
		draw.polygon(((44+a_y*20,1+a_off),(49+a_y*20,1+a_off),(52+a_y*20,10+a_off),(49+a_y*20,19+a_off),(44+a_y*20,19+a_off),(47+a_y*20,10+a_off)),fill=(255,112,233))

	if(after[0] == 7):
		draw.polygon(((25+a_y*20,1+a_off),(20+a_y*20,1+a_off),(17+a_y*20,10+a_off),(20+a_y*20,19+a_off),(25+a_y*20,19+a_off),(22+a_y*20,10+a_off)),fill=(255,112,233))
		draw.polygon(((16+a_y*20,1+a_off),(11+a_y*20,1+a_off),(8+a_y*20,10+a_off),(11+a_y*20,19+a_off),(16+a_y*20,19+a_off),(13+a_y*20,10+a_off)),fill=(255,112,233))

def Make_Chart(s,num,file_name,music_1=None,music_2=None,music_3=None,music_4=None,music=None,t_bool = False):
	Time = s[-1][-1]
	y_range = int(Time//10+1)*1000
	img = Image.new('RGBA',(180,y_range))
	im_text = Image.new('RGBA',(1080,200),"black")
	t_draw = ImageDraw.Draw(im_text)
	font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",20)
	t_draw.text((0,40),"被スキル範囲",font=font)
	t_draw.text((0,80),"被スキルノーツ数",font=font)
	t_draw.text((0,120),"直後ノーツの秒数",font=font)
	t_draw.text((0,160),"直前ノーツの秒数",font=font)
	draw = ImageDraw.Draw(img)
	'''
	draw.line((20,10,160,10),fill=(150,150,150))
	for i in range(int(Time)+1):
		draw.line((20,10+100*(i+1),160,10+100*(i+1)),fill=(150,150,150))
	for i in range(8):
		if(0 < i < 7):
			draw.line((20*(i+1),0,20*(i+1),y_range),fill=(150,150,150))
		else:
			draw.line((20*(i+1),0,20*(i+1),y_range),fill=(255,255,255))
	'''
	S_line = []
	BPM = []
	NorS = []
	Sly  = []
	Lon = []
	Hol = []
	Skill = [0,0,0,0,0]
	count = 0
	not_note = 0
	cover_start = [0,0,0,0,0]
	cover_end = [0,0,0,0,0]
	cover_num = [0,0,0,0,0]
	note_num = 0
	for i in range(len(s)):
		if(s[i][0] >= 1 and s[i][0] <= 3):
			NorS += [s[i]]
		elif(s[i][0] >= 4 and s[i][0] <= 7):
			Sly += [s[i]]
		elif(s[i][0] == 8):
			Lon += [s[i]]
		elif(s[i][0] == 9):
			Hol += [s[i]]
		elif(s[i][0] == 0):
			S_line += [s[i]]
			Skill[count] = int(s[i][-1]*100)
			not_note += 1
			s_time = s[i][3]
			end_note = 0			
			count += 1
			s_count = 0
			for j in range(i,len(s)):
				if(int((s[j][3]-s_time)*120)/120 > 9):
					t_draw.text((180*count,120),str(int((s[j][3]-s_time)*120)/120)[:8],font=font)
					end_note = j
					break
				end_note = j
			while True:
				if(int((s[i-s_count-1][3]-s_time)*120)/120 == 0):
					s_count += 1
				else:
					t_draw.text((180*count,160),str(int((s[i-s_count-1][3]-s_time)*120)/120)[:8],font=font)
					break
			if(s_count == 0):
				cover_start[count-1] = i+2-not_note
			else:
				cover_start[count-1] = i-s_count-not_note+2
			cover_end[count-1] = end_note-not_note
			cover_num[count-1] = cover_end[count-1]-cover_start[count-1]+1
		else:
			BPM += [s[i]]
			not_note += 1
	t_draw.text((0,0),str(len(s)-not_note)+"ノーツ",font=font)
	for i in range(5):
		t_draw.text((180*(i+1),0),"S"+str(i+1),font=font)
		t_draw.text((180*(i+1),40),str(cover_start[i])+"~"+str(cover_end[i]),font=font)
		t_draw.text((180*(i+1),80),str(cover_num[i])+"ノーツ",font=font)
	note_num = len(s)-not_note
	for i in range(len(S_line)):
		Skill_Line(draw,S_line[i][3])
	for i in range(len(NorS)):
		if(NorS[i][0] == 1):
			Note_1(draw,NorS[i][3],NorS[i][1])
		if(NorS[i][0] == 2):
			Note_2(draw,NorS[i][3],NorS[i][1])
		if(NorS[i][0] == 3):
			Scrach(draw,NorS[i][3],NorS[i][1])
	while len(Lon) > 1:
		before = Lon[0]
		del Lon[0]
		for i in range(len(Lon)):
			if(before[1] == Lon[i][1]):
				after = Lon[i]
				del Lon[i]
				break
		Long(draw,before,after)
	while len(Hol) > 1:
		before = Hol[0]
		del Hol[0]
		for i in range(len(Hol)):
			if(before[1] == Hol[i][1]):
				after = Hol[i]
				del Hol[i]
				break
		Hold(draw,before,after)
	while len(Sly) > 1:
		before = Sly[0]
		del Sly[0]
		if(before[0] >= 6):
			after = before
			Slider(draw,before,after)
		else:
			after = Sly[0]
			if(after[0] >= 5):
				del Sly[0]
			Slider(draw,before,after)
	if(len(Sly)==1):
		if(Sly[0][0] >= 6):
			after = before
			Slider(draw,before,after)
	a = 5
	im_flip = ImageOps.flip(img)
	im_Chart = Image.new('RGBA', (180*6,1220))
	im_Skill_Chart = Image.new('RGBA',(180*6,1220),(0x00,0x00,0x00))
	draw_bg = ImageDraw.Draw(im_Skill_Chart)
	for it in range(5):
		j = it+1
		for k in range(102):
				draw_bg.line((20+180*j,210+10*k,160+180*j,210+10*k),fill=(50,50,50))
		for i in range(9):
			draw_bg.line((20+180*j,260+100*i,160+180*j,260+100*i),fill=(150,150,150))
		for i in range(8):
			if(0 < i < 7):
				draw_bg.line((20*(i+1)+180*j,200,20*(i+1)+180*j,y_range+200),fill=(150,150,150))
			else:
				draw_bg.line((20*(i+1)+180*j,200,20*(i+1)+180*j,y_range+200),fill=(255,255,255))
	for i in range(a):
		im_flip.crop((0,y_range-(Skill[i]-50)-20,180,y_range-(Skill[i]+950)))
		im_Chart.paste(im_flip.crop((0,y_range-(Skill[i]+950)-20,180,y_range-(Skill[i]-50))),(180*(i+1),200))
	im_Chart.paste(im_text,(0,0))
	result = Image.alpha_composite(im_Skill_Chart,im_Chart)
	r_draw = ImageDraw.Draw(result)
	if(music_1 != None and music_2 != None and music_3 != None and music_4 != None):
		font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",32)
		try:
			im_samnail = Image.open('./データ/画像/'+music_1+'.png')
		except:
			im_samnail = Image.open('./データ/画像/Dig Delight!.png')
		result.paste(im_samnail.resize((180,180)),(0,250))
		try:
			im_samnail = Image.open('./データ/画像/'+music_2+'.png')
		except:
			im_samnail = Image.open('./データ/画像/Dig Delight!.png')
		result.paste(im_samnail.resize((180,180)),(0,480))
		try:
			im_samnail = Image.open('./データ/画像/'+music_3+'.png')
		except:
			im_samnail = Image.open('./データ/画像/Dig Delight!.png')
		result.paste(im_samnail.resize((180,180)),(0,710))
		try:
			im_samnail = Image.open('./データ/画像/'+music_4+'.png')
		except:
			im_samnail = Image.open('./データ/画像/Dig Delight!.png')
		result.paste(im_samnail.resize((180,180)),(0,940))
		for i in range(3):
			r_draw.text((75,430+230*i),"↓",font=font)
		result.save(file_name +'.png')
	elif(music != None):
		try:
			im_samnail = Image.open('./データ/画像/'+music+'.png')
		except:
			im_samnail = Image.open('./データ/画像/Dig Delight!.png')
		result.paste(im_samnail.resize((180,180)),(0,250))
		if(not(t_bool)):
			with open('./データ/Chart/'+music+'_skill.csv','w') as f:
				writer = csv.writer(f)
				writer.writerows([[note_num],cover_start,cover_end,cover_num])
		result.save(file_name +'.png')
	if(t_bool):
		result.show()
	return [[note_num],cover_start,cover_end,cover_num]

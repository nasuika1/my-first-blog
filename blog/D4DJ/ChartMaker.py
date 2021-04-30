from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np

def Skill_Line(draw,time):
	off = time*300//8
	draw.line((20,10+off,160,10+off),fill=(200,0,0),width = 3)

def Note_1(draw,time,y):
	off = time*300//8
	draw.rectangle((21+y*20,5+off,39+y*20,15+off),fill=(90,184,221))

def Note_2(draw,time,y):
	off = time*300//8
	draw.rectangle((21+y*20,5+off,39+y*20,15+off),fill=(47,105,214))

def Scrach(draw,time,y):
	off = time*300//8
	draw.ellipse((21+y*20,3+off,39+y*20,17+off),fill=(240,150,41))

def Long(draw,before,after):
	b_off = before[2]*300//8
	a_off = after[2]*300//8
	b_y  = before[1]
	a_y  = after[1]
	draw.rectangle((23+b_y*20,10+b_off,37+a_y*20,10+a_off),fill=(255,242,178))
	draw.rectangle((21+b_y*20,5+b_off,39+b_y*20,15+b_off),fill=(255,222,76))
	draw.rectangle((21+a_y*20,5+a_off,39+a_y*20,15+a_off),fill=(255,222,76))

def Hold(draw,before,after):
	b_off = before[2]*300//8
	a_off = after[2]*300//8
	b_y  = before[1]
	a_y  = after[1]
	draw.rectangle((23+b_y*20,10+b_off,37+a_y*20,10+a_off),fill=(255,135,112))
	draw.ellipse((21+b_y*20,3+b_off,39+b_y*20,17+b_off),fill=(255,75,35))
	draw.ellipse((21+a_y*20,3+a_off,39+a_y*20,17+a_off),fill=(255,75,35))

def Slider(draw,before,after):
	b_off = before[2]*300//8
	a_off = after[2]*300//8
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

def Write_Text(draw,time,text):
	x_off = (time//64)
	y_off = (time%64)*(300/8)
	font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",20)
	if(text == text*10//10):
		text = int(text)
	draw.text((160+x_off*220,2400-y_off-7),'◀'+str(text),fill=(102,187,221),font=font)

def Make_Chart(s,num,file_name,t_bool = False,sign = None):
	img = Image.new('RGBA',(220,2420+2400*((num-1)//8)),(0x00,0x00,0x00))
	draw = ImageDraw.Draw(img)
	draw.line((20,10,160,10),fill=(200,200,200))
	for i in range(num):
		draw.line((20,10+300*(i+1),160,10+300*(i+1)),fill=(200,200,200))
		if(sign != None):
			split = int(sign[i])
		else:
			split = 4
		for j in range(split-1):
				draw.line((20,10+300*(i+1)-300*(j+1)//split,160,10+300*(i+1)-300*(j+1)//split),fill=(70,70,70))
	for i in range(8):
		if(0 < i < 7):
			draw.line((20*(i+1),0,20*(i+1),320+300*(num-1)),fill=(150,150,150))
		else:
			draw.line((20*(i+1),0,20*(i+1),320+300*(num-1)),fill=(255,255,255))
	S_line = []
	BPM = []
	NorS = []
	Sly  = []
	Lon = []
	Hol = []
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
		else:
			BPM += [s[i]]
	for i in range(len(S_line)):
		Skill_Line(draw,S_line[i][2])
	for i in range(len(NorS)):
		if(NorS[i][0] == 1):
			Note_1(draw,NorS[i][2],NorS[i][1])
		if(NorS[i][0] == 2):
			Note_2(draw,NorS[i][2],NorS[i][1])
		if(NorS[i][0] == 3):
			Scrach(draw,NorS[i][2],NorS[i][1])
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
		before = Sly[0]
		if(Sly[0][0] >= 6):
			after = before
			Slider(draw,before,after)
	a = (num-1)//8
	im_flip = ImageOps.flip(img)
	im_Chart = Image.new('RGBA', (220*(a+1),2420))
	for i in range(a+1):
		im_Chart.paste(im_flip.crop((0,2400*(a-i),220,2420+2400*(a-i) )),(220*i,0))
	draw_im = ImageDraw.Draw(im_Chart)
	for i in range(len(BPM)):
		Write_Text(draw_im,BPM[i][2],BPM[i][0])
	im_Chart.save(file_name +'.png')
	if(t_bool):
		im_Chart.show()
#1:ノーツ1
#2:ノーツ2
#3:スクラッチ
#4:スライダー始点
#5:スライダー終点
#6:スライダーフリック右
#7:スライダーフリック左
#8:ロング
#9:ホールド
#0:スキル開始位置

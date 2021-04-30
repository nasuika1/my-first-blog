import cv2
import os
import numpy as np
import csv

class Note_Type:
    def __init__(self,color,region,n_name):
        self.color = color
        self.region = region
        self.n_name = n_name

class Note:
    def __init__(self,min_value,max_value,color,name):
        self.min_value = min_value
        self.max_value = max_value
        self.color = color
        self.name = name

class ChartInfo:
    def __init__(self):
        self.chartinfo = []
    
    def Add_Note(self,frame,note_type,note_place):
        self.chartinfo += [[frame,note_type,note_place]]
    
    def reset(self):
        self.chartinfo = []

    def Substi(self,s):
        self.chartinfo = s

class Chart:
    def __init__(self):
        self.chart = []
    
    def add_note(self,frame,note_type,note_place):
        self.chart += [[frame,note_place,note_type]]

def serch_region(hsv,min_value,max_value):
    color_min = np.array(min_value,np.uint8)
    color_max = np.array(max_value,np.uint8)
    color_region = cv2.inRange(hsv,color_min,color_max)
    return color_region

def padding_position(x,y,w,h,p):
    return x-p,y-p,w+p*2,h+p*2

class Analysis:
    def __init__(self,movie_name):
        self.movie_name = cv2.VideoCapture(movie_name)
        self.width = self.movie_name.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.movie_name.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = self.movie_name.get(cv2.CAP_PROP_FPS)
        self.fc = self.movie_name.get(cv2.CAP_PROP_FRAME_COUNT)
        self.ci = ChartInfo()
        self.note_count = [0,0,0,0,0,0,0]
        self.slider_count = 0
        self.hold_count = 0
        self.long_count = 0
        self.chart = Chart()
        self.count_1 = 0
        self.count_2 = 0

    def save_movie(self,file_name,frame_num = None):
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        video = cv2.VideoWriter(file_name,fourcc,self.fps,(int(self.width),int(self.height)))
        if(frame_num == None):
            frame_num = int(self.fc)
        i = 0
        while i < frame_num:
            print(i)
            self.ci.reset()
            self.count_1 = 0
            self.count_2 = 0
            img = self.save_frame(i)
            if(img.dtype!='uint8'):
                break
            video.write(img)
            i += 4-2*self.count_1 - self.count_2
        video.release()

    def analys(self,frame_num = None):
        if(frame_num == None):
            frame_num = int(self.fc)
        self.c_before = []
        self.c_after = []
        for i in range(7):
            self.c_before += [ChartInfo()]
            self.c_after += [ChartInfo()]
        i = 0
        while i < frame_num:
            print(i)
            self.count_1 = 0
            self.count_2 = 0
            b = self.analys_frame(i)
            if not(b):
                break
            i += 3-self.count_1 - self.count_2
        m = int(700-500/0.85)
        for i in range(len(self.chart.chart)):
            n = self.chart.chart[i][1]
            if(self.chart.chart[i][2] == 6):
                print(i,self.chart.chart[i])
            else:
                w = 960+(1115-m)/(n[1]+n[3]/2-m)*(n[0]+n[2]/2-960)
                print(i,self.chart.chart[i],int(w*7/1920))

    def analys_frame(self,frame_num):
        if not self.movie_name.isOpened():
            return False
        #該当フレームの読み込み
        #retは読み込めたがどうが(True,False),frameは画像データ
        self.movie_name.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.movie_name.read()
        if not(ret):
            return False
        #色抽出
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        #slider,[150~180,140~200,180~255]
        #note1,[90~100,170~220,200~255]
        #note2,[100~110,60~230,200~255]
        #long,[25~35,60~230,180~255]
        #scrach,[5~20,60~230,200~255]
        #hold,[170~180,60~230,200~255]
        pink_region = serch_region(hsv,[150,140,180],[170,200,255])
        sky_region = serch_region(hsv,[90,170,200],[100,220,255])
        blue_region = serch_region(hsv,[100,60,200],[110,230,255])
        yellow_region = serch_region(hsv,[25,60,180],[35,230,255])
        orange_region = serch_region(hsv,[5,180,200],[15,230,255])
        red_region = serch_region(hsv,[170,60,200],[180,230,255])
        red_line = serch_region(hsv,[170,200,100],[180,255,255])

        #それぞれのノーツの色の補色で領域を四角で囲む
        Slider = Note_Type([128,255,20],pink_region,'slider')
        Note1 = Note_Type([0,0,255],sky_region,'note1')
        Note2 = Note_Type([0,255,255],blue_region,'note2')
        Long = Note_Type([255,0,0],yellow_region,'longnote')
        Scrach = Note_Type([255,90,0],orange_region,'scrach')
        Red = Note_Type([255,0,0],red_region,'hold')
        Skill_Line = Note_Type([255,255,255],red_line,'skill_line')

        note_array = [Slider,Note1,Note2,Long,Scrach,Red,Skill_Line]

        #ノーツを検出し四角でマーク
        for i in range(len(note_array)):
            self.c_before[i].Substi(self.c_after[i].chartinfo)
            self.ci.reset()
            self.mark_region(frame,note_array[i],frame_num)
            for j in range(len(self.ci.chartinfo)):
                n = self.ci.chartinfo[j]
                print(n[2],n[1].n_name)
            m = int(700-500/0.85)
            self.c_after[i].Substi(self.ci.chartinfo)
            self.counting(self.c_before[i].chartinfo,self.c_after[i].chartinfo,i,frame_num)
            if(len(self.c_before[i].chartinfo) > 0 and len(self.c_after[i].chartinfo)):
                by = (1440-self.c_before[i].chartinfo[0][2][1])/(self.c_before[i].chartinfo[0][2][1]-m)*10
                ay = (1440-self.c_after[i].chartinfo[0][2][1])/(self.c_after[i].chartinfo[0][2][1]-m)*10
            #ay-by = -4.2
        print(self.note_count)
        print(len(self.chart.chart))
        return True
    
    def counting(self,sb,sa,c,f):
        if(c == 0):
            if(len(sb)>0):
                if(len(sa) == 0):
                    self.note_count[c] += 1
                    if(len(sb[self.slider_count]) == 4):
                        c = 7
                    self.chart.add_note(f,c,sb[self.slider_count][2])
                    self.slider_count = 0
                else:
                    if(self.slider_count == 0):
                        if(sb[0][2][1] > sa[0][2][1]+4):
                            self.note_count[c] += 1
                            if(len(sb[0]) == 4):
                                c = 7
                            self.chart.add_note(f,c,sb[0][2])
                        elif(sa[0][2][1] > 990):
                            self.slider_count = 1
                            self.note_count[c] += 1
                            if(len(sb[0]) == 4):
                                c = 7
                            self.chart.add_note(f,c,sb[0][2])
                    elif(self.slider_count == 1):
                        if(sa[0][2][1] < 990):
                            if(sa[0][2][1] < 800):
                                self.note_count[c] += 1
                                if(len(sb[1]) == 4):
                                    c = 7
                                self.chart.add_note(f,c,sb[1][2])
                            self.slider_count = 0
                        elif(len(sb) > 1 and len(sa) == 1):
                            self.note_count[c] += 1
                            if(len(sb[1]) == 4):
                                c = 7
                            self.chart.add_note(f,c,sb[1][2])
                        else:
                            for j in range(len(sb)-1):
                                if(sb[j+1][2][1] > sa[1][2][1]):
                                    self.note_count[c] += 1
                                    if(len(sb[j+1]) == 4):
                                        c = 7
                                    self.chart.add_note(f,c,sb[j+1][2])
                                    break
        elif(c == 3):
            if(len(sb)>0):
                if(len(sa) == 0):
                    self.note_count[c] += len(sb)-self.long_count
                    for i in range(len(sb)-self.long_count):
                        self.chart.add_note(f,c,sb[i+self.long_count][2])
                    self.long_count = 0
                else:
                    if(self.long_count == 0):
                        for j in range(len(sb)):
                            if(sb[j][2][1] > sa[0][2][1]+4):
                                self.note_count[c] += 1
                                self.chart.add_note(f,c,sb[j][2])
                            elif(sa[j][2][1] > 1050):
                                self.long_count += 1
                                self.note_count[c] += 1
                                self.chart.add_note(f,c,sb[j][2])
                            else:
                                break
                    elif(self.long_count == 1):  
                        if(sa[0][2][1] < 1050):
                            if(sa[0][2][1] < 900):
                                self.note_count[c] += 1
                                self.chart.add_note(f,c,sb[1][2])
                            self.long_count -= 1
                        elif(len(sb) > 1):
                            if(len(sa) > 1):
                                if(sa[1][2][1] > 1050):
                                    self.long_count += 1
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[1][2])
                            if not(sb[0][2][0] > sa[0][2][0] - 200 and sb[0][2][0] < sa[0][2][0] + 200):
                                self.note_count[c] += 2
                                self.chart.add_note(f,c,sb[1][2])
                                self.chart.add_note(f,c,sb[2][2])
                    
                    elif(self.long_count == 2):
                        if(len(sa) > 1):
                            if(sa[0][2][1] < 1050):
                                if(sa[0][2][1] < 900):
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[3][2])
                                self.long_count -= 1
                            if(sa[1][2][1] < 1050):
                                if(sa[1][2][1] < 900):
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[2][2])
                                self.long_count -= 1
                        else:
                            if(sa[0][2][1] < 1050):
                                if(sa[0][2][1] < 900):
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[1][2])
                                self.long_count -= 1         
        elif(c == 5):
            if(len(sb)>0):
                if(len(sa) == 0):
                    self.note_count[c] += len(sb)-self.hold_count
                    for i in range(len(sb)-self.hold_count):
                        self.chart.add_note(f,c,sb[i+self.hold_count][2])
                    self.hold_count = 0
                else:
                    if(self.hold_count == 0):
                        for j in range(len(sb)):
                            if(sb[j][2][1] > sa[0][2][1]+4):
                                self.note_count[c] += 1
                                self.chart.add_note(f,c,sb[j][2])
                            elif(sa[j][2][1] > 1000):
                                self.hold_count += 1
                                self.note_count[c] += 1
                                self.chart.add_note(f,c,sb[j][2])
                            else:
                                break
                    elif(self.hold_count == 1):  
                        if(sa[0][2][1] < 1000):
                            if(sa[0][2][1] < 800):
                                self.note_count[c] += 1
                                self.chart.add_note(f,c,sb[1][2])
                            self.hold_count -= 1
                        elif(len(sb) > 1):
                            if(len(sa) > 1):
                                if(sa[1][2][1] > 1000):
                                    self.hold_count += 1
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[1][2])
                            if not(sb[0][2][0] > sa[0][2][0] - 50 and sb[0][2][0] < sa[0][2][0] + 50):
                                self.note_count[c] += 2
                                self.chart.add_note(f,c,sb[1][2])
                                self.chart.add_note(f,c,sb[2][2])
                    
                    elif(self.hold_count == 2):
                        if(len(sa) > 1):
                            if(sa[0][2][1] < 1000):
                                if(sa[0][2][1] < 800):
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[3][2])
                                self.hold_count -= 1
                            if(sa[1][2][1] < 1000):
                                if(sa[1][2][1] < 800):
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[2][2])
                                self.hold_count -= 1
                        else:
                            if(sa[0][2][1] < 1000):
                                if(sa[0][2][1] < 800):
                                    self.note_count[c] += 1
                                    self.chart.add_note(f,c,sb[1][2])
                                self.hold_count -= 1
        else:
            if(len(sb) > 0 ):
                if(len(sa) == 0):
                    if(c == 6):
                        self.note_count[c] += 1
                        self.chart.add_note(f,c,sb[0][2])
                    else:
                        self.note_count[c] += len(sb)
                        for i in range(len(sb)):
                            self.chart.add_note(f,c,sb[i][2])
                else:
                    for j in range(len(sb)):
                        if(sb[j][2][1] > sa[0][2][1]+4):
                            self.note_count[c] += 1
                            self.chart.add_note(f,c,sb[j][2])
                        else:
                            break

    def save_frame(self,frame_num,result_path = None):
        if not self.movie_name.isOpened():
            return
        #該当フレームの読み込み
        #retは読み込めたがどうが(True,False),frameは画像データ
        self.movie_name.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.movie_name.read()
        if not(ret):
            return np.array(0,dtype=np.int64)
        #色抽出
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        a,b = 700,600 
        m = -0.61
        print(hsv[a:a+10,b:b+10])
        for i in range(1440):
                frame[i,int(m*(i-a))+b]=[0,0,255]
        for i in range(1440):
                frame[i,int(-m*(i-a))+1920-b]=[0,0,255]
        a,b = 700,460
        m = -0.85
        for i in range(1440):
            if(int(m*(i-a))+b>0):
                frame[i,int(m*(i-a))+b]=[0,0,255]
        for i in range(1440):
            if(int(-m*(i-a))+1920-b < 1920):
                frame[i,int(-m*(i-a))+1920-b]=[0,0,255]
        a = 1115
        b = 692
        c = 820
        for i in range(1920):
                frame[a,i]=[0,0,255]
                frame[b,i]=[0,0,255]
                frame[c,i]=[0,0,255]

        #slider,[150~180,140~200,180~255]
        #note1,[90~100,170~220,200~255]
        #note2,[100~110,60~230,200~255]
        #long,[25~35,60~230,180~255]
        #scrach,[5~20,60~230,200~255]
        #hold,[170~180,60~230,200~255]
        pink_region = serch_region(hsv,[150,140,180],[170,200,255])
        sky_region = serch_region(hsv,[90,170,200],[100,220,255])
        blue_region = serch_region(hsv,[100,60,200],[110,230,255])
        yellow_region = serch_region(hsv,[25,60,180],[35,230,255])
        orange_region = serch_region(hsv,[5,180,200],[15,230,255])
        red_region = serch_region(hsv,[170,60,200],[180,230,255])
        red_line = serch_region(hsv,[170,200,100],[180,255,255])

        #それぞれのノーツの色の補色で領域を四角で囲む
        Slider = Note_Type([128,255,20],pink_region,'slider')
        Note1 = Note_Type([0,0,255],sky_region,'note1')
        Note2 = Note_Type([0,255,255],blue_region,'note2')
        Long = Note_Type([255,0,0],yellow_region,'longnote')
        Scrach = Note_Type([255,90,0],orange_region,'scrach')
        Red = Note_Type([255,0,0],red_region,'hold')
        Skill_Line = Note_Type([255,255,255],red_line,'skill_line')

        note_array = [Slider,Note1,Note2,Long,Scrach,Red,Skill_Line]

        #ノーツを検出し四角でマーク
        for i in range(len(note_array)):
            self.ci.reset()
            frame = self.mark_region(frame,note_array[i],frame_num)
            for j in range(len(self.ci.chartinfo)):
                n = self.ci.chartinfo[j]
                print(n[2],n[1].n_name)
                cv2.rectangle(frame,(n[2][0],n[2][1]),(n[2][0]+n[2][2],n[2][1]+n[2][3]),n[1].color,3)
        if result_path !=None:
            os.makedirs(os.path.dirname(result_path),exist_ok=True)
            cv2.imwrite(result_path,frame)   

        return frame    

    def print_property(self):
        print(self.movie_name.isOpened())
        print(self.width)
        print(self.height)
        print(self.fps)
        print(self.fc)

    def mark_region(self,img,note,frame_num):
        contours, hieralky = cv2.findContours(note.region,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #輪郭表示
        if(note.color != [255,255,255]):
            #検出最小サイズ
            min_size = 2000
            for c in contours:
                if cv2.contourArea(c) < min_size:
                    continue
                x,y,w,h = cv2.boundingRect(c)
                x,y,w,h = padding_position(x,y,w,h,5)
                
                if(y > 200):
                    if(len(self.ci.chartinfo) > 0):
                        n = self.ci.chartinfo[-1]
                        if(n[1].n_name == 'slider' and y + h/2 > n[2][1] and y < n[2][1]+5):
                            self.ci.chartinfo[-1] = [frame_num,note,[x,y,w,h]]
                            if(x < n[2][0] or x > n[2][0] + n[2][2]):
                                self.ci.chartinfo[-1] += [1]
                            continue
                        if(n[1].n_name == 'longnote' and (y < n[2][1] + 10 and y > n[2][1] -10)):
                            if(n[2][0] - x < 400 and y > 950):
                                self.ci.chartinfo[-1] = [frame_num,note,[x,y,n[2][0]+n[2][3],h]]
                                continue
                    if(y < 995):
                        self.count_1 = 1
                        if(y > 550):
                            self.count_2 = 1
                    if note.n_name == 'slider' and ((y > 800 and w*h < 10000) or y > 1000):
                        continue
                    self.ci.Add_Note(frame_num,note,[x,y,w,h])

        else:
            min_size = 500
            for c in contours:
                if cv2.contourArea(c) < min_size:
                    continue
                x,y,w,h = cv2.boundingRect(c)
                x,y,w,h = padding_position(x,y,w,h,5)

                if h < 30 and y > 400:
                    self.ci.Add_Note(frame_num,note,[x,y,w,h])
                    if(y < 995):
                        self.count_1 = 1
                        if(y > 550):
                            self.count_2 = 1
        return img

    def F2S(self,file_name):
        m = int(700-500/0.85)
        before_time = 0
        s_c = []
        for i in range(len(self.chart.chart)):
            t = self.chart.chart[i][0]
            p = self.chart.chart[i][1]
            n = self.chart.chart[i][2]
            if(n == 1 or n == 2 or n == 3):
                b = (1440-p[1])/(p[1]-m)*10
                a = (1440-1057)/(1057-m)*10
                time = (t+(a-b)/4.2)/self.fps
            elif(n == 0 or n == 7):
                b = (1440-p[1])/(p[1]-m)*10
                a = (1440-995)/(995-m)*10
                time = (t+(a-b)/4.2)/self.fps
            elif(n == 4 or n == 5):
                b = (1440-p[1])/(p[1]-m)*10
                a = (1440-1005)/(1005-m)*10
                time = (t+(a-b)/4.2)/self.fps
            elif(n == 6):
                b = (1440-p[1])/(p[1]-m)*10
                a = (1440-1057)/(1057-m)*10
                time = (t+(a-b)/4.2)/self.fps
            if(n == 6):
                w = 7
            else:
                w = int((960+(1115-m)/(p[1]+p[3]/2-m)*(p[0]+p[2]/2-960))*7/1920)
            if(i > 0):
                if(time-s_c[-1][0] < 0.002 and s_c[-1][1] != 7 and w != 7):
                    time = (time+s_c[-1][0])/2
                    s_c[-1][0] = time
            s_c += [[time,w,n]]
            before_time = time
        for i in range(len(s_c)):
            print(s_c[i][0],s_c[i][1],s_c[i][2])
        with open(file_name,'w') as f:
            writer = csv.writer(f)
            writer.writerows(s_c)
            
    def release(self):
        self.movie_name.release()

a = Analysis('動画/ぐるぐるDJTURN.mov')
#a.save_frame(824,'動画/テスト.jpg')
a.print_property()
#a.save_movie('動画/テスト.mp4',frame_num = None)
a.analys(frame_num = None)
a.F2S('動画/ぐるぐるDJTURN.csv')
a.release()
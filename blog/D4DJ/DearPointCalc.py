import csv
import itertools
import sys
from mysite.settings import BASE_DIR


def Concider_accuracy(m_list,accuracy,Criteria,i_rate):
    max_point = 0
    for i in range(len(m_list)):
        m_list[i][4] = float(m_list[i][4])
        for j in range(4):
            m_list[i][5+j] = float(m_list[i][5+j])
            l_accuracy = (float(m_list[i][5+j]) - Criteria)*i_rate +accuracy
            if(l_accuracy < 0):
                l_accuracy = 0
            m_list[i] += [m_list[i][9+j]]
            m_list[i][9+j] = int(m_list[i][9+j]) - (int(m_list[i][9+j]) * l_accuracy) // 100
            if(m_list[i][9+j]//10 > max_point):
                max_point = m_list[i][9+j]//10
    return m_list,max_point

def Level_Divide(m_list,max_point):
    Level = ["Easy","Normal","Hard","Expert"]
    point_array = [[1000] for i in range(10,int(max_point)+1)]
    for i in range(len(m_list)):
        for j in range(4):
            get_p = int(m_list[i][9+j])//10-10
            if(get_p < 0):
                get_p = 0
            if(point_array[get_p][0] > float(m_list[i][4])):
                point_array[get_p] = [float(m_list[i][4]),m_list[i][1],Level[j],get_p+10,int(m_list[i][13+j])]
    
    return point_array

def SearchEfficient(point_list):
    max_efficient = 0
    efficient_m = 0
    for i in range(len(point_list)):
        if(len(point_list[i]) > 1):
            a = point_list[i][3]/point_list[i][0]
            if(a > max_efficient):
                max_efficient = a
                efficient_m = i
    return efficient_m
            
def CountGreat(pl,wp,vo):
    min_great = pl[4] - (wp+1)*10 + 1
    max_great = pl[4] - wp * 10
    if(min_great < 0):
        min_great = 0
    if(vo < 2):
        vo = 0
    if(wp == 10):
        return str(vo) + "ボルテージ消費、オート可"
    else:
        return str(vo) + "ボルテージ消費、Great以下を" + str(min_great) + "個以上" + str(max_great) + "個以下"

def Calc_Dear(music_list,want_point,voltage,accuracy = 0,Criteria = 14.0,increase_rate = 1):
    music_list,max_point = Concider_accuracy(music_list,accuracy,Criteria,increase_rate)
    point_list = Level_Divide(music_list,max_point)
    efficient_music = SearchEfficient(point_list)
    if(want_point < 10):
        print("欲しい親愛度は10以上")
        return 
    if(voltage < 1):
        voltage = 1
    efficient = point_list[efficient_music]
    Threshold = int((voltage + 0.5) * max_point)
    play_list = []
    play_list_2 = []
    while want_point > Threshold:
        want_point -= efficient[3]
        great_num = CountGreat(efficient,efficient[3],0)
        play_list += [efficient+[great_num]]
        play_list_2 += [efficient+[great_num]]

    #１曲の時
    v = 1
    for i in range(voltage-1):
        if(want_point%(voltage-i) == 0 and want_point/(voltage-i) <= max_point):
            v = voltage-i
            break
    if(want_point <= max_point*v):
        w_point = int(want_point//v)
        pl_10 = point_list[w_point-10]
        pl_9 = point_list[w_point-9]
        if(len(pl_10) <= 2):
            play_list += [pl_10]
        else:
            great_num = CountGreat(pl_10,w_point,v)
            play_list += [pl_10+[great_num]]
        if(len(point_list) >= w_point-10):
            if(pl_10[0] > pl_9[0]):
                great_num = CountGreat(pl_9,w_point,v)
                play_list_2 += [pl_9+[great_num]]
            else:
                if(len(pl_10) <= 2):
                    play_list_2 += [pl_10]
                else:
                    great_num = CountGreat(pl_10,w_point,v)
                    play_list_2 += [pl_10+[great_num]]
        if(len(play_list[-1]) <= 1):
            if(len(play_list_2[-1]) <= 1):
                del play_list[-1]
                del play_list_2[-1]
            else:
                play_list[-1] = play_list_2[-1]
                return play_list,play_list_2
        else:
            if(len(play_list_2[-1]) <= 1):
                play_list_2[-1] = "グレ１０個程度出してもいい譜面はない"
                return play_list,play_list
            return play_list,play_list_2
    #２曲以上の時
    sorted_list = sorted(point_list,reverse=False,key = lambda x:x[0])
    for i in range(len(sorted_list)):
        if(sorted_list[i][0] == 1000):
            sorted_list = sorted_list[:i]
            break
    Candicate_list = []
    Candicate_list_2 = []
    if(voltage < 2):
        voltage = 1
    for i,j in itertools.product(range(len(sorted_list)),range(len(sorted_list))):
        for v_i,v_j in itertools.product(range(6),range(6)):
            if(v_i + v_j > voltage):
                continue
            if(v_i == 0):
                v_i = 1
            if(v_j == 0):
                v_j = 1
            get_point = sorted_list[i][3] * v_i + sorted_list[j][3] * v_j
            get_point_2 = (sorted_list[i][3]-1) * v_i + sorted_list[j][3] * v_j
            get_point_3 = sorted_list[i][3] * v_i + (sorted_list[j][3]-1) * v_j
            get_point_4 = (sorted_list[i][3]-1) * v_i + (sorted_list[j][3]-1) * v_j
            if(v_i == 1):
                v_i = 0
            if(v_j == 1):
                v_j = 0
            if(want_point == get_point):
                Candicate_list += [[sorted_list[i],sorted_list[j],sorted_list[i][0]+sorted_list[j][0],sorted_list[i][3],sorted_list[j][3],v_i,v_j]]
                Candicate_list_2 += [[sorted_list[i],sorted_list[j],sorted_list[i][0]+sorted_list[j][0],sorted_list[i][3],sorted_list[j][3],v_i,v_j]]
            if(want_point == get_point_2):
                Candicate_list_2 += [[sorted_list[i],sorted_list[j],sorted_list[i][0]+sorted_list[j][0],sorted_list[i][3]-1,sorted_list[j][3],v_i,v_j]]
            if(want_point == get_point_3):
                Candicate_list_2 += [[sorted_list[i],sorted_list[j],sorted_list[i][0]+sorted_list[j][0],sorted_list[i][3],sorted_list[j][3]-1,v_i,v_j]]
            if(want_point == get_point_4):
                Candicate_list_2 += [[sorted_list[i],sorted_list[j],sorted_list[i][0]+sorted_list[j][0],sorted_list[i][3]-1,sorted_list[j][3]-1,v_i,v_j]]

    if(len(Candicate_list) > 0):
        Add_list = sorted(Candicate_list,reverse=False,key = lambda x:x[2])[0]
        Add_list_2 = sorted(Candicate_list_2,reverse=False,key = lambda x:x[2])[0]
        for i in range(2):
            great_num = CountGreat(Add_list[i],Add_list[3+i],Add_list[5+i])
            play_list += [Add_list[i]+[great_num]]
        for i in range(2):
            great_num = CountGreat(Add_list_2[i],Add_list_2[3+i],Add_list_2[5+i])
            play_list_2 += [Add_list_2[i]+[great_num]]
        return play_list,play_list_2
    else:
        print("未実装")
        return [],[]

class Music:
    def __init__(self,dear_point,voltage,accuracy = 0, criteria = 14.0, increase_rate = 1):
        self.dear_point = dear_point
        self.voltage = voltage
        self.accuracy = accuracy
        self.criteria = criteria
        self.increase_rate = increase_rate
        self.music_info = self.open_data()
        self.play_list = ''
        self.play_list_2 = ''

    def Main(self):
        if(int(self.voltage) > 10):
            print("消費ボルテージは10以下で設定")
            return
        if(int(self.dear_point) < 10):
            print("9以下の貢献度は得られません")
            return
        p1,p2 = Calc_Dear(self.music_info,self.dear_point,self.voltage,accuracy= self.accuracy,Criteria = self.criteria,increase_rate = self.increase_rate)

        self.play_list = p1
        self.play_list_2 = p2
    
    def open_data(self):
        with open(BASE_DIR+'/blog/D4DJ/データ/d4dj_music.csv') as f:
            reader = csv.reader(f)
            music_info = []
            for row in reader:
                music_info += [row]
        return music_info

#a = Music(200,3)
#a.Main()
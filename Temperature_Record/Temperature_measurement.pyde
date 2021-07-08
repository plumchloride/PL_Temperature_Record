import csv
import time
sc_mode = 1 #1=入力(初期画面)　2=一覧 3=編集（2のタブ内） 4=info 5=info(win) 6=info(kikkake) 7=info(config) 8=red reason 9=入力処理
page = 1
def setup():
    size(405,720) #16:9 *45
    background(253, 247, 234)
    with open("../data/config.csv","r",) as ta:
        config = list(csv.reader(ta))
    top2 = int(config[3][0])
    last1 = int(config[4][0])
    frameRate(int(config[0][0]))
    global config,top2,last1
    
def draw():
    global sc_mode
    import datetime
    dt_now = datetime.datetime.now() #時刻の取得
    frameRate(int(config[0][0]))
    background(253, 247, 234)
    tab() #タブ表示
    with open("../data/data.csv","r",) as ta:
        table = list(csv.reader(ta))
    amount = len(table)
    if sc_mode == 1 or sc_mode == 9: #入力画面
        #上部入力欄の表示
        stroke(50)
        strokeWeight(0.5)
        if amount == 0:
            fill(255)
        elif table[amount-1][0][:-6] != dt_now.strftime("20%y/%m/%d"):
            fill(247, 194, 182)
        else:
            fill(255)
        rect(20,20,205,100) 
        top2_rect(top2) #上2桁の表示
        last1_rect(last1) #下1桁の表示
        #体温表示
        fill(50)
        textAlign(LEFT, TOP)
        textSize(80)
        text(str(top2)+"."+str(last1),30,20)
        #決定ボタン
        if 225<=mouseX<=375 and 15<=mouseY<=125 and sc_mode == 1:
            fill(247, 194, 182)
        else:
            fill(255)            
        rect(235,20,135,100)
        #テキスト
        fill(50)
        textAlign(LEFT, TOP)
        textSize(39)
        text("Record",237,60)
        textSize(30)
        text("35.",42,146)
        text("36.",130,146)
        text("37.",240,146)
        text("38.",322,146)
        textSize(80)
        for i in range(9):
            text("{}".format(i+1),68+110*(i-((i)//3)*3),213 +110*((i)//3))
        textSize(70)
        text("0",183,534)
        #時刻表示
        textSize(10)
        text(dt_now.strftime("20%y/%m/%d %H:%M:%S"),247,22)
        
    if sc_mode == 2: #itiran
        amari = amount % 11
        amount_page = amount // 11
        global amount_page
        stroke(50)
        strokeWeight(0.5)
        for i in range(12):
            line(20, 20 + 50 * i, 385, 20 + 50 * i)
        if page == 1:
            pass
        elif 75<=mouseX<=160 and 570<=mouseY<=640: #left
            image(pic_icon[9],95,580)
        else:
            image(pic_icon[8],95,580)
        if amount_page+1 == page:
            pass
        elif 245<=mouseX<=320 and 570<=mouseY<=640: #right
            image(pic_icon[7],260,580)
        else:
            image(pic_icon[6],260,580)
        textSize(50)
        fill(50)
        text(page,187,575)
        for i in range(11):
            textSize(20)
            fill(50)
            if amount - i - 1 -((page-1)*11) < 0:
                text("None",30,35 + 50*i)
                continue
            text(table[amount - i - 1 -((page-1)*11)][0],30,35 + 50*i)
            textSize(30)
            if float(table[amount - i - 1 -((page-1)*11)][1]) >= float(config[1][0]):
                fill(247, 194, 182)
            elif float(table[amount - i - 1 -((page-1)*11)][1]) <= float(config[2][0]):
                fill(161,187,230)
            else:
                fill(50)
            text(table[amount - i - 1 -((page-1)*11)][1],280,30 + 50*i)
            
    #info
    for i in [4,5,6,7,8]:
        if sc_mode == i:
            image(pic_icon[i+6],0,0)
    #info rect
    if sc_mode == 4:
        noFill()
        stroke(161,187,230)
        strokeWeight(2)
        if 22<=mouseX<=360:
            if 30<=mouseY<=95:
                rect(22,30,338,65)
            if 95<mouseY<=170:
                rect(22,95,338,75)
            if 170<mouseY<=240:
                rect(22,170,338,70)
            if 240<mouseY<=310:
                rect(22,240,338,70)
        
        
    #データの処理
    if sc_mode == 9:
        frameRate(1)
        with open("../data/data.csv","a") as ta:
            writer = csv.writer(ta)
            writer.writerow([dt_now.strftime("20%y/%m/%d %H:%M"),top2+last1*0.1])
        textSize(50)
        stroke(50)
        strokeWeight(2)
        fill(255)
        with open("../data/data.csv","r",) as ta:
            table = list(csv.reader(ta))
        if dt_now.strftime("20%y/%m/%d %H:%M") == table[amount][0] and top2+last1*0.1 == float(table[amount][1]):
            rect(15,335,385,65)
            fill(50)
            text("Record success",20,340)
        else:
            raise Exception("The entered data and the recorded data are different")
        sc_mode = 1
        
def mousePressed():
    global sc_mode,top2,last1,page,amount_page
    #tab切り替え
    if 640<mouseY<720:
        if 0<=mouseX<130:
            sc_mode = 1
        elif 130<=mouseX<260:
            sc_mode = 2
        elif 260<=mouseX:
            sc_mode = 4
    #上2桁切り替え
    if sc_mode == 1 and 135<=mouseY<=195:
        if 35<=mouseX<=95:
            top2 = 35
        elif 95<mouseX<=205:
            top2 = 36
        elif 205<mouseX<=315:
            top2 = 37
        elif 315<mouseX<=365:
            top2 = 38
    #下1桁切り替え
    if sc_mode == 1:
        if  205<=mouseY<=315:
            if 40<=mouseX<=150:
                last1 = 1
            elif 150<mouseX<=260:
                last1 = 2
            elif 260<mouseX<=370:
                last1 = 3
        elif 315<mouseY<=425:
            if 40<=mouseX<=150:
                last1 = 4
            elif 150<mouseX<=260:
                last1 = 5
            elif 260<mouseX<=370:
                last1 = 6
        elif 425<mouseY<=535:
            if 40<=mouseX<=150:
                last1 = 7
            elif 150<mouseX<=260:
                last1 = 8
            elif 260<mouseX<=370:
                last1 = 9
        elif 535<mouseY<=615:
            if 40<=mouseX<=370:
                last1 = 0
    #入力ボタン
    if sc_mode == 1:
        if 225<=mouseX<=375 and 15<=mouseY<=125:
            sc_mode = 9
    #change table
    if sc_mode == 2:
        if 75<=mouseX<=160 and 570<=mouseY<=640 and page != 1:
            page -= 1
        if 245<=mouseX<=320 and 570<=mouseY<=640 and amount_page+1 != page:
            page += 1            
    #change mode info
    if sc_mode == 4:
        if 22<=mouseX<=360:
                if 30<=mouseY<=95:
                    sc_mode = 5
                if 95<mouseY<=170:
                    sc_mode = 6
                if 170<mouseY<=240:
                    sc_mode = 7
                if 240<mouseY<=310:
                    sc_mode = 8
    
def tab(): #画面下部タブの表示
    noStroke()
    fill(255)
    rect(0,643,405,80)
    stroke(50)
    strokeWeight(4)
    line(0,643,405,643)
    pic_icon = [None] * 15
    global pic_icon
    for i in range(15):
        pic_icon[i] = loadImage("../data/{}.png".format(i + 1))
    if 640<mouseY<720:
        if 0<=mouseX<130:
            image(pic_icon[3], 40, 650)
            i_pr(1,2)
        elif 130<=mouseX<260:
            image(pic_icon[4], 170, 650)
            i_pr(0,2)
        elif 260<=mouseX:
            image(pic_icon[5], 300, 650)
            i_pr(0,1)
    else:
        for i in range(3):
            image(pic_icon[i], 40 + i * 130, 650)

def i_pr(a,b):
    for i in [a,b]:
        image(pic_icon[i], 40 + i * 130, 650)
        
def top2_rect(a): #上2桁の選択ボタン表示
    fill(247, 194, 182)
    stroke(50)
    strokeWeight(0.5)
    if a == 35:
        rect(40,140,50,50)
        fill(255)
        rect(100,140,100,50) 
        rect(210,140,100,50) 
        rect(320,140,50,50)
    elif a == 36:
        rect(100,140,100,50) 
        fill(255)
        rect(40,140,50,50)
        rect(210,140,100,50) 
        rect(320,140,50,50)
    elif a == 37:
        rect(210,140,100,50)
        fill(255)
        rect(40,140,50,50)
        rect(100,140,100,50) 
        rect(320,140,50,50)
    elif a == 38:
        rect(320,140,50,50)
        fill(255)
        rect(40,140,50,50)
        rect(100,140,100,50)
        rect(210,140,100,50)   

def last1_rect(a):
    if a == 0:
        for i in range(9):
            rect(45+110*(i-((i)//3)*3),210 +110*((i)//3),100,100)
        fill(247, 194, 182)
        rect(45,540,320,70)
    else:
        last = [1,2,3,4,5,6,7,8,9]
        fill(255)
        stroke(50)
        strokeWeight(0.5)
        last.remove(a)
        for i in last:
            rect(45+110*(i-1-((i-1)//3)*3),210 +110*((i-1)//3),100,100)
        rect(45,540,320,70)
        fill(247, 194, 182)
        rect(45+110*(a-1-((a-1)//3)*3),210 +110*((a-1)//3),100,100)

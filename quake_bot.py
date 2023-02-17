# coding:utf-8
import RPi.GPIO as GPIO
import time
import math
import requests
import schedule
from datetime import datetime
import datetime as dt
from time import sleep



#Beepのセットアップ#########################################################################
pin = 17  # 任意のピン番号
a0 = 27.500  # 低いラの音

# n番目の音階の周波数を返す
def onkai(n):
    return a0*math.pow(math.pow(2, 1/12), n)

# それぞれの音の周波数を定義
SO = onkai(22)
SOS = onkai(23)
DO = onkai(27)
DOF = onkai(28)
MI = onkai(31)
FA = onkai(32)
SIF = onkai(37)
SI = onkai(38)
MIF = onkai(42)
MI2 = onkai(43)

# メロディとリズムを配列に
mery_merody = [SO, DO, MI, SIF, MIF, SOS, DOF, FA, SI, MI2]
mery_rhythm = [0.2, 0.2, 0.2, 0.2, 0.5, 0.2, 0.2, 0.2, 0.2, 1.0]

def play_beep():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    p = GPIO.PWM(pin, 1)
    p.start(50)

    p.ChangeFrequency(2)
    time.sleep(2)

    # 配列の通りに鳴らす
    for j in range(3):
        for i, oto in enumerate(mery_merody):
            p.start(50)
            p.ChangeFrequency(oto)
            time.sleep(mery_rhythm[i])
            p.stop()
            time.sleep(0.03)

    p.stop()
    GPIO.cleanup()
############################################################################################
def quake_main():
    dt_now = datetime.now()
    #リクエストするURLを指定(最新の地震情報のデータを取得することができるURL)
    p2pquake_url = 'https://api.p2pquake.net/v2/history?codes=551&limit=1'
    #リクエスト(データを取得する)
    p2pquake_json = requests.get(p2pquake_url).json()

    for i in range(len(p2pquake_json)):
        #地震時間
        quake_time = datetime.strptime(p2pquake_json[i]["time"], '%Y/%m/%d %H:%M:%S.%f')
        # 1分足す
        quake_time_plus_one = quake_time + dt.timedelta( seconds=15, minutes=1)

        #福井県坂井市があるのか検索とビープ音を鳴らす
        for locate in p2pquake_json[i]["points"]:
            #坂井市のみ
            if '坂井市' in locate["addr"]:
                if dt_now < quake_time_plus_one:
                    play_beep()            
                    break
            #全国のどこか
            # if dt_now < quake_time_plus_one:
            #     play_beep()
            #     print(dt_now)
            #     print(p2pquake_json[i]["earthquake"])      
            #     break

schedule.every(15).seconds.do(quake_main)

while True:
    schedule.run_pending()
    sleep(1)


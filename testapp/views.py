#文章生成の設定
from __future__ import print_function
from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.optimizers import RMSprop
from janome.tokenizer import Tokenizer  # 追加
import numpy as np
import random
import sys
import io
import re


#flaskの設定
from flask import render_template, request, redirect, url_for
from testapp import app
from random import randint


#flask-mailの設定
from flask import Flask 
from flask_mail import Mail
from flask_mail import Message


#現在の時間を取得
import datetime



#mailの設定
mail = Mail(app)
#SMTPサーバーアドレス
app.config['MAIL_SERVER']='smtp.gmail.com'
#PORT番号
app.config['MAIL_PORT'] = 465
#ユーザーID
app.config['MAIL_USERNAME'] = '2022.fit.team3@gmail.com'
#パスワード
app.config['MAIL_PASSWORD'] = '秘密'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)




#説明用
'''
@app.route('/test') #http://127.0.0.1:5000/ つまりルートにアクセスしたときに表示するページの処理と言うこと
def index(): #indexはHTMLでこのページに飛びたい時に指定される
    
    #HTMLに値を与えたい時はこのように与える
    my_dict = {
        'insert_something1': 'views.pyのinsert_something1部分です。',
        'insert_something2': 'views.pyのinsert_something2部分です。',
        'test_titles': ['title1', 'title2', 'title3']
    }

    return render_template('testapp/index.html', my_dict=my_dict)
    #どのHTMLに行くか指定
'''



#入力フォーム
@app.route('/')
def Top():
    return render_template('testapp/top.html')



#文章生成
@app.route('/create', methods=['POST'])
def Create():    

    #top.htmlから入力された値を受け取る
    Create1 = request.form['number']
    Create3 = request.form['destination']
    Create4 = request.form['classtime']
    Create5 = request.form['text']
    Create6 = request.form['name']
    Create7 = request.form['tel']
    Create8 = request.form['requirement']

    #未入力の場合の処理
    if Create1 == "":
        Create1 = "21A20XX"
    if Create6 == "":
        Create6 = "福工 太郎"
    if Create7 == "":
        Create7 = "012-3456-7890"
    if Create8 == "":
        Create8 = "1"
    if Create3 == "who":
        tname = "山田 太郎先生"
        tmail = "yamada"
    if Create4 == "when":
        classtime = "O曜X限"
    if Create5 == "":
        Create5 = "体調不良で入院のため"
    
    #電話番号に-を追加
    if len(Create7) == 11:
        Create7 = Create7[0:3]+"-"+Create7[3:7]+"-"+Create7[7:11]

    #要件からタイトルに入力
    if Create8 == "1":
        Create2 = "欠席の連絡"
    elif Create8 == "2":
        Create2 = "研究室訪問についての連絡"


    #現在の時間を取得に必要
    dt_now = datetime.datetime.now()


    #学籍番号にsがついていた場合消去する
    if Create1[0].upper() == "S":
        Create1 = Create1[1:]

    #学籍番号のAなどの英字を小文字にする
    Create1 = Create1[0:2] + Create1[2].lower() + Create1[3:]

    #現在の年-学籍番号
    year = int(str(dt_now.year)[2:]) - int(Create1[0:2])

    #現在の月を取得
    month = dt_now.month

    #学籍番号から何年生か調べる
    if year == 0:
        if month >= 4:
            grade = "1年"
        else:
            grade = "0年"
    elif year == 1:
        if month >= 4:
            grade = "2年"
        else:
            grade = "1年"
    elif year == 2:
        if month >= 4:
            grade = "3年"
        else:
            grade = "2年"
    elif year == 3:
        if month >= 4:
            grade = "4年"
        else:
            grade = "3年"
    #2100年になった時用
    elif year == -99:
        grade = "2年"
    elif year == -98:
        grade = "3年"
    elif year == -97:
        grade = "4年"


    #学籍番号の英字を大文字にして取得
    number = Create1[2].upper()

    #学籍番号から何学部か調べる
    if number == "A":
        course = "情報工学部 情報工学科"
    elif number == "B":
        course = "情報工学部 情報通信工学科"
    elif number == "C":
        course = "情報工学部 情報システム工学科"
    elif number == "M":
        course = "情報工学部 システムマネジメント学科"
    elif number == "F":
        course = "工学部 電子情報工学科"
    elif number == "G":
        course = "工学部 生命環境化学科"
    elif number == "E":
        course = "工学部 知能機械工学科"
    elif number == "5":
        course = "工学部 電気工学科"
    elif number == "K":
        course = "社会環境学部 社会環境学科"
    elif number == "X":
        course = "科目履修生"


    #教授の名前やメールアドレスを取得する
    if Create3 == "000":
        #tname = "先生の名前"
        tname = "石原 真紀夫先生"
        #tmail = "名字のローマ字"
        tmail = "isihara"
    elif Create3 == "001":
        tname = "種田 和正先生"
        tmail = "oida"

    elif Create3 == "002":
        tname = "柏 浩司先生"
        tmail = "kashiwa"

    elif Create3 == "003":
        tname = "正代 隆義先生"
        tmail = "shodai"

    elif Create3 == "004":
        tname = "馬場 謙介先生"
        tmail = "k-baba"

    elif Create3 == "005":
        tname = "福本 誠先生"
        tmail = "fukumoto"

    elif Create3 == "006":
        tname = "前田 道治先生"
        tmail = "maeda"

    elif Create3 == "007":
        tname = "山内 寛行先生"
        tmail = "yamauchi"

    elif Create3 == "008":
        tname = "山澤 一誠先生"
        tmail = "yamazawa"

    elif Create3 == "009":
        tname = "有吉 哲也先生"
        tmail = "ariyoshi"

    elif Create3 == "010":
        tname = "家永 貴史先生"
        tmail = "ienaga"

    elif Create3 == "011":
        tname = "佐竹 純二先生"
        tmail = "satake"

    elif Create3 == "012":
        tname = "柴田 望洋先生"
        tmail = "shibata"

    elif Create3 == "013":
        tname = "戸田 航史先生"
        tmail = "toda"

    elif Create3 == "014":
        tname = "中川 正基先生"
        tmail = "m-nakagawa"

    elif Create3 == "015":
        tname = "宮田 考史先生"
        tmail = "miyata"

    elif Create3 == "016":
        tname = "山盛 厚伺先生"
        tmail = "yamamori"

    elif Create3 == "017":
        tname = "相良 哲生先生"
        tmail = "sagara"

    elif Create3 == "018":
        tname = "兵頭 和幸先生"
        tmail = "hyodo"

    elif Create3 == "019":
        tname = "山口 裕先生"
        tmail = "y-yamaguchi"

    elif Create3 == "020":
        tname = "石田 智行先生"
        tmail = "t-ishida"

    elif Create3 == "021":
        tname = "糸川 銚先生"
        tmail = "itokawa"

    elif Create3 == "022":
        tname = "内田 法彦先生"
        tmail = "n-uchida"

    elif Create3 == "023":
        tname = "杉田 薫先生"
        tmail = "sugita"

    elif Create3 == "024":
        tname = "中嶋 徳正先生"
        tmail = "n-nakashima"

    elif Create3 == "025":
        tname = "中村 龍史先生"
        tmail = "t-nakamura"

    elif Create3 == "026":
        tname = "西田 茂人先生"
        tmail = "nishida"

    elif Create3 == "027":
        tname = "バロリ レオナルド先生"
        tmail = "baroli"

    elif Create3 == "028":
        tname = "藤崎 清孝先生"
        tmail = "fujisaki"

    elif Create3 == "029":
        tname = "前田 洋先生"
        tmail = "hiroshi"

    elif Create3 == "030":
        tname = "松尾 慶太先生"
        tmail = "kt-matsuo"

    elif Create3 == "031":
        tname = "山元 規靖先生"
        tmail = "nori@bene"

    elif Create3 == "032":
        tname = "渡辺 仰基先生"
        tmail = "koki"

    elif Create3 == "033":
        tname = "池田 誠先生"
        tmail = "m-ikeda"

    elif Create3 == "034":
        tname = "先生"
        tmail = ""

    elif Create3 == "035":
        tname = "先生"
        tmail = ""

    elif Create3 == "036":
        tname = "山口 明宏先生"
        tmail = "aki"

    elif Create3 == "037":
        tname = "木室 義彦先生"
        tmail = "kimuro"

    elif Create3 == "038":
        tname = "徳安 達士先生"
        tmail = "tokuyasu"

    elif Create3 == "039":
        tname = "利光 和彦先生"
        tmail = "toshimitsu"

    elif Create3 == "040":
        tname = "森園 哲也先生"
        tmail = "morizono"

    elif Create3 == "041":
        tname = "吉田 耕一先生"
        tmail = "k-yoshida"

    elif Create3 == "042":
        tname = "作田 誠先生"
        tmail = "sakuta"

    elif Create3 == "043":
        tname = "下戸 健先生"
        tmail = "simoto"

    elif Create3 == "044":
        tname = "丸山 勳先生"
        tmail = "i-maruyama"

    elif Create3 == "045":
        tname = "松原 裕之先生"
        tmail = "h-matsubara"

    elif Create3 == "046":
        tname = "山本 貴弘先生"
        tmail = "t_yama"

    elif Create3 == "047":
        tname = "菊田 俊幸先生"
        tmail = "kikuta"

    elif Create3 == "048":
        tname = "田村 かおり先生"
        tmail = "k-tamura"

    elif Create3 == "049":
        tname = "李 知炯先生"
        tmail = "j.lee"

    elif Create3 == "050":
        tname = "井口 修一先生"
        tmail = "inokuchi"

    elif Create3 == "051":
        tname = "宋 宇先生"
        tmail = "song"

    elif Create3 == "052":
        tname = "田嶋 拓也先生"
        tmail = "t-tajima"

    elif Create3 == "053":
        tname = "藤岡 寛之先生"
        tmail = "fujioka"

    elif Create3 == "054":
        tname = "前原 秀明先生"
        tmail = "h-maehara"

    elif Create3 == "055":
        tname = "クラ エリス先生"
        tmail = "kulla"

    elif Create3 == "056":
        tname = "小林 稔先生"
        tmail = "kobayashi"

    elif Create3 == "057":
        tname = "髙橋 啓先生"
        tmail = "takahashi"

    elif Create3 == "058":
        tname = "傅 靖先生"
        tmail = "j.fu"

    elif Create3 == "059":
        tname = "竹之内 宏先生"
        tmail = "h-takenouchi"

    elif Create3 == "100":
        tname = "江口 啓先生"
        tmail = "eguti"

    elif Create3 == "101":
        tname = "片山 龍一先生"
        tmail = "r-katayama"

    elif Create3 == "102":
        tname = "近木 祐一郎先生"
        tmail = "kogi"

    elif Create3 == "103":
        tname = "倪 宝栄先生"
        tmail = "nee"

    elif Create3 == "104":
        tname = "前田 文彦先生"
        tmail = "f-maeda"

    elif Create3 == "105":
        tname = "松井 義弘先生"
        tmail = "matsui"

    elif Create3 == "106":
        tname = "松木 裕二先生"
        tmail = "matsuki"

    elif Create3 == "107":
        tname = "盧 存偉先生"
        tmail = "lu"

    elif Create3 == "108":
        tname = "小野美 武先生"
        tmail = "onomi"

    elif Create3 == "109":
        tname = "田村 瞳先生"
        tmail = "h-tamura"

    elif Create3 == "110":
        tname = "中村 壮智先生"
        tmail = "tk-nakamura"

    elif Create3 == "111":
        tname = "巫 霄先生"
        tmail = "xiao"

    elif Create3 == "112":
        tname = "野瀬 敏洋先生"
        tmail = "nose"

    elif Create3 == "113":
        tname = "家形 諭先生"
        tmail = "yakata"

    elif Create3 == "114":
        tname = "赤木 紀之先生"
        tmail = "t-akaki"

    elif Create3 == "115":
        tname = "蒲池 高志先生"
        tmail = "kamachi"

    elif Create3 == "116":
        tname = "北山 幹人先生"
        tmail = "kitayama"

    elif Create3 == "117":
        tname = "桑原 順子先生"
        tmail = "j-kuwahara"

    elif Create3 == "118":
        tname = "呉 行正先生"
        tmail = "wu"

    elif Create3 == "119":
        tname = "永田 純一先生"
        tmail = "j-nagata"

    elif Create3 == "120":
        tname = "松山 清先生"
        tmail = "matsuyama"

    elif Create3 == "121":
        tname = "三田 肇先生"
        tmail = "mita"

    elif Create3 == "122":
        tname = "天田 啓先生"
        tmail = "amada"

    elif Create3 == "123":
        tname = "久保 裕也先生"
        tmail = "kubo"

    elif Create3 == "124":
        tname = "長谷(田丸) 靜香先生"
        tmail = "tamaru"

    elif Create3 == "125":
        tname = "宮元 展義先生"
        tmail = "miyamoto"

    elif Create3 == "126":
        tname = "福永 知則先生"
        tmail = "fukunaga"

    elif Create3 == "127":
        tname = "江頭 竜先生"
        tmail = "egashira"

    elif Create3 == "128":
        tname = "朱 世杰先生"
        tmail = "zhu"

    elif Create3 == "131":
        tname = "数仲 馬恋典先生"
        tmail = "suciu"

    elif Create3 == "132":
        tname = "仙波 卓弥先生"
        tmail = "senba"

    elif Create3 == "133":
        tname = "髙津 康幸先生"
        tmail = "takatsu"

    elif Create3 == "134":
        tname = "廣田 健治先生"
        tmail = "k-hirota"

    elif Create3 == "135":
        tname = "村山 理一先生"
        tmail = "murayama"

    elif Create3 == "136":
        tname = "山岸 里枝先生"
        tmail = "yamagishi"

    elif Create3 == "137":
        tname = "天本 祥文先生"
        tmail = "y-amamoto"

    elif Create3 == "138":
        tname = "加藤 友規先生"
        tmail = "t-kato"

    elif Create3 == "139":
        tname = "駒田 佳介先生"
        tmail = "komada"

    elif Create3 == "140":
        tname = "砂原 賢治先生"
        tmail = "sunahara"

    elif Create3 == "141":
        tname = "竹田 寛志先生"
        tmail = "h-takeda"

    elif Create3 == "142":
        tname = "槇田 諭先生"
        tmail = "makita"

    elif Create3 == "143":
        tname = "下川 倫子先生"
        tmail = "shimokawa"

    elif Create3 == "144":
        tname = "玉本 拓巳先生"
        tmail = "t-tamamoto"

    elif Create3 == "145":
        tname = "鞆田 顕章先生"
        tmail = "tomoda"

    elif Create3 == "146":
        tname = "井上 昌睦先生"
        tmail = "ms-inoue"

    elif Create3 == "147":
        tname = "大山 和宏先生"
        tmail = "ohyama"

    elif Create3 == "148":
        tname = "梶原寿了先生"
        tmail = "kajiwara"

    elif Create3 == "149":
        tname = "北川 二郎先生"
        tmail = "j-kitakawa"

    elif Create3 == "150":
        tname = "田島 大輔先生"
        tmail = "tashima"

    elif Create3 == "151":
        tname = "松尾 敬二先生"
        tmail = "k-matsuo"

    elif Create3 == "152":
        tname = "北﨑 訓先生"
        tmail = "kitazaki"

    elif Create3 == "153":
        tname = "鈴木 恭一先生"
        tmail = "k-suzuki"

    elif Create3 == "154":
        tname = "辻野 太郎先生"
        tmail = "tsujino"

    elif Create3 == "155":
        tname = "遠藤 文人先生"
        tmail = "endo"

    elif Create3 == "156":
        tname = "進藤 久和先生"
        tmail = "shindoh"

    elif Create3 == "157":
        tname = "中西 真大先生"
        tmail = "m-nakanishi"

    elif Create3 == "201":
        tname = "乾 隆帝先生"
        tmail = "inui"

    elif Create3 == "202":
        tname = "鄭 雨宗先生"
        tmail = "jung"

    elif Create3 == "203":
        tname = "中川 智治先生"
        tmail = "t-nakagawa"

    elif Create3 == "204":
        tname = "藤井 洋次先生"
        tmail = "y-fujii"

    elif Create3 == "205":
        tname = "松藤 賢二郎先生"
        tmail = "matsufuji"

    elif Create3 == "206":
        tname = "尹 諒重先生"
        tmail = "in"

    elif Create3 == "207":
        tname = "李 文忠先生"
        tmail = "ri"

    elif Create3 == "208":
        tname = "渡邉 智明先生"
        tmail = "t-watanabe"

    elif Create3 == "209":
        tname = "上杉 昌也先生"
        tmail = "uesugi"

    elif Create3 == "210":
        tname = "木下 健先生"
        tmail = "kinoshita"

    elif Create3 == "211":
        tname = "田中 久美子先生"
        tmail = "ku-tanaka"

    elif Create3 == "212":
        tname = "陳 艶艶先生"
        tmail = "chen"

    elif Create3 == "213":
        tname = "片岡 雅世先生"
        tmail = "kataoka"

    elif Create3 == "214":
        tname = "橘 雄介先生"
        tmail = "y-tachibana"

    elif Create3 == "215":
        tname = "森山 聡之先生"
        tmail = "t-moriyama"
    


    #授業の日時を取得する
    if Create4 == "m1":
        classtime = "月曜日1限"
    elif Create4 == "m2":
        classtime = "月曜日2限"
    elif Create4 == "m3":
        classtime = "月曜日3限"
    elif Create4 == "m4":
        classtime = "月曜日4限"
    elif Create4 == "m5":
        classtime = "月曜日5限"
    elif Create4 == "m6":
        classtime = "月曜日6限"
    elif Create4 == "t1":
        classtime = "火曜日1限"
    elif Create4 == "t2":
        classtime = "火曜日2限"
    elif Create4 == "t3":
        classtime = "火曜日3限"
    elif Create4 == "t4":
        classtime = "火曜日4限"
    elif Create4 == "t5":
        classtime = "火曜日5限"
    elif Create4 == "t6":
        classtime = "火曜日6限"
    elif Create4 == "w1":
        classtime = "水曜日1限"
    elif Create4 == "w2":
        classtime = "水曜日2限"
    elif Create4 == "w3":
        classtime = "水曜日3限"
    elif Create4 == "w4":
        classtime = "水曜日4限"
    elif Create4 == "w5":
        classtime = "水曜日5限"
    elif Create4 == "w6":
        classtime = "水曜日6限"
    elif Create4 == "th1":
        classtime = "木曜日1限"
    elif Create4 == "th2":
        classtime = "木曜日2限"
    elif Create4 == "th3":
        classtime = "木曜日3限"
    elif Create4 == "th4":
        classtime = "木曜日4限"
    elif Create4 == "th5":
        classtime = "木曜日5限"
    elif Create4 == "th6":
        classtime = "木曜日6限"
    elif Create4 == "f1":
        classtime = "金曜日1限"
    elif Create4 == "f2":
        classtime = "金曜日2限"
    elif Create4 == "f3":
        classtime = "金曜日3限"
    elif Create4 == "f4":
        classtime = "金曜日4限"
    elif Create4 == "f5":
        classtime = "金曜日5限"
    elif Create4 == "f6":
        classtime = "金曜日6限"

    #[]
    #https://programming.mmsankosho.com/archives/11772?_ga=2.162437812.905264649.1669099105-87430135.1669099104
    
    #データセットの選択
    if Create8 == "1":
        path = r"testapp\detaset\detaset1.txt"
    elif Create8 == "2":
        path = r"testapp\detaset\detaset2.txt"
 
    with io.open(path, encoding='utf-8') as f:
        text_original = f.read().lower()
    
    a = re.sub("《[^》]+》", "", text_original) # ルビの削除
    a = re.sub("［[^］]+］", "", a) # 読みの注意の削除
    a = re.sub("[｜ 　]", "", a) # | と全角半角スペースの削除
    print('corpus length:', len(a))

    t = Tokenizer()

    text =t.tokenize(a, wakati=True)  # 分かち書きする
    text_list = list(t.tokenize(a, wakati=True))
    chars = text_list
    count = 0
    char_indices = {}  # 辞書初期化
    indices_char = {}  # 逆引き辞書初期化


    for word in chars:
        if not word in char_indices:  # 未登録なら
            char_indices[word] = count  # 登録する      
            count +=1
            print(count,word)  # 登録した単語を表示
    # 逆引き辞書を辞書から作成する
    indices_char = dict([(value, key) for (key, value) in char_indices.items()])


    maxlen = 5
    step = 1
    sentences = []
    next_chars = []
    text_list = list(t.tokenize(a, wakati=True))
    for i in range (0, len(text_list) - maxlen, step):
        sentences.append(text_list[i: i + maxlen])
        next_chars.append(text_list[i + maxlen])
    print('nb sequences:', len(sentences))


    
    #変更
    #[]
    #x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    #y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    #for i, sentence in enumerate(sentences):
    #    for t, char in enumerate(sentence):
    #        x[i, t, char_indices[char]] = 1
    #    y[i, char_indices[next_chars[i]]] = 1
    # In[24]:
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=bool)
    y = np.zeros((len(sentences), len(chars)), dtype=bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1
    
    



    #[]
    # modelの読み込み
    from tensorflow import keras
    if Create8 == "1":
        model = keras.models.load_model(r"testapp\seiseimail1")
    elif Create8 == "2":
        model = keras.models.load_model(r"testapp\seiseimail2")


    #[]
    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)
    

    #シードを関数外から指定できるようにグローバル変数化
    global seed
    
    def on_epoch_end(epoch, _):
        # Function invoked at end of each epoch. Prints generated text.
        for diversity in [0.2]:  # diversity は 0.2のみ使用

            #文章生成結果がgenerated1に入っている
            #genrated1を関数外で使えるようにグローバル変数化
            global generated
            
            generated = ''
            s = Tokenizer()
        
            sentence1 = seed
            sentence2 =s.tokenize(sentence1, wakati=True)  # 分かち書きする
            sentence_list = list(s.tokenize(sentence1, wakati=True))
            sentence = sentence_list[0:maxlen]
            # sentence はリストなので文字列へ変換して使用
            generated += "".join(sentence)
            # sentence はリストなので文字列へ変換して使用
            
            for i in range(100):
                try:
                    x_pred = np.zeros((1, maxlen, len(chars)))
                    for t, char in enumerate(sentence):
                        x_pred[0, t, char_indices[char]] = 1.

                    preds = model.predict(x_pred, verbose=0)[0]
                    next_index = sample(preds, diversity)
                    next_char = indices_char[next_index]

                    if(next_char=="！"):
                        break
                    generated += next_char
                    sentence = sentence[1:]
                    # sentence はリストなので append で結合する
                    sentence.append(next_char)

                except KeyError:
                    #変更
                    generated = sentence1
                    if Create8 == "1":
                        next_char1 = "、欠席させていただきたいと思います。\n\nどうぞよろしくお願いいたします。"
                    elif Create8 == "2":
                        next_char1 = "ぜひ一度、お伺いできればと考えております。\nもしよろしければ以下の日程から都合の良いお時間を頂戴いただきたく存じます。"
                    generated += next_char1
                    break
            print(generated)
            print()

    print_callback = LambdaCallback(on_epoch_end=on_epoch_end)


    
    #[]
    seed=Create5

    #変更
    #mail_lstm = model.fit(x, y,callbacks=[print_callback],verbose=0)
    model.fit(x, y,callbacks=[print_callback],verbose=0)
    

    # In[30]:　追加？
    #model.save("mailseisei6")


    address = "s"+Create1+"@bene.fit.ac.jp"

    # 教授の名前
    #
    # （前文）
    # 学部学科 学年 組 名前
    #
    # 何曜日何限の授業の件で連絡させていただきました。
    # 生成結果
    # 
    # （後文）
    # --
    # ++福岡工業大学 学部学科 学年
    # ++名前
    # ++メールアドレス
    # ++電話番号
    
    front = tname+"\n\n"+course+" "+grade+Create1[3]+"組の"+Create6+"と申します。\n\n"+classtime+"の授業の件で連絡させていただきました。\n"
    
    if Create8 == "1":
        front = tname+"\n\nいつもご指導いただき、ありがとうございます。\n"+course+" "+grade+Create1[3]+"組の"+Create6+"と申します。\n\n"+classtime+"の授業の件について、"
    elif Create8 == "2":
        front = tname+"\n\nいつもご指導いただき、ありがとうございます。\n"+course+" "+grade+Create1[3]+"組の"+Create6+"と申します。\n\n"
    
    back = "\n\n-----\n"+"++ 福岡工業大学 "+course+" "+grade+"\n++ "+Create6+"\n++ "+address+"\n++ "+Create7+"\n-----"
    text = front+generated+back
  
    create = {
        'Create1': Create2,
        'Create2': tmail+"@fit.ac.jp",
        'Create3': address,
        'Create4': text,
        }
        
    return render_template('testapp/create.html', create=create)



#メール送信
@app.route('/mail', methods=['POST'])
def Mail():
        
    Mail1 = request.form['subject']
    Mail2 = request.form['destination']
    Mail3 = request.form['address']
    Mail4 = request.form['result']
        
    msg = Message(Mail1,
              sender="2022.fit.team3@gmail.com",
              recipients=[Mail3])
    msg.body = Mail4
        
    mail.send(msg)
    #メール送信コマンド
        
    result = {
        'Mail1': Mail1,
        'Mail3': Mail3,
        'Mail4': Mail4,
        }
    
    return render_template('testapp/mail.html', result=result)
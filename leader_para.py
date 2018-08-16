# -*- coding:utf-8 -*-

import tkinter as Tk
import sys,os

args = sys.argv
if len(args) == 1 :
	args = ["","P1","P2"]
tu_st = ["☆",""]
le_stas = []
units = []
start_now = False
battle_set = [0,0]
st_si = 40
st_si_h = 20


def callback(label, ch):
	def num_ch():
		label["text"] = str(int(label["text"])+ch)
	return num_ch
"""
ユニットパラメータに関するコールバック
num = ユニット通し番号0~5
ch = ユニットパラメータの変化方向 1 or -1
u_s_s_l = unit status s? label, ユニットのどのステータスを変化させるか
			0 HP, 1 MaxHP, 2 Atk, 3 Men
"""
def unitback(num,ch,u_s_s_l):
	def num_ch():
		u_ns = units[num][1]
		la_n = int(u_ns[u_s_s_l]["text"])+ch
		"""ゲームが始まっているなら気絶などになる"""
		if start_now:
			"""ユニットが気絶、死亡状態なら無視"""
			if la_n < 0 or units[num][2] != 0:
				pass
			elif u_s_s_l == 0:
				"""HPが0になったら気絶にしてMenを下げる"""
				if la_n == 0:
					u_ns[3]["text"] = str(int(u_ns[3]["text"])-1)
					units[num][0]["text"] = "^o^"
					if units[num][2] == 0:
						units[num][2] = 2
				"""HPはMaxHP以下なら変化する"""
				if la_n <= int(u_ns[1]["text"]):
					u_ns[0]["text"] = str(la_n)
			elif u_s_s_l == 3 and ch == -1:
				"""メンタルが直接減ったら気絶にする"""
				u_ns[u_s_s_l]["text"] = str(la_n)
				units[num][0]["text"] = "^o^"
				if units[num][2] == 0:
					units[num][2] = 2
			elif u_s_s_l == 1:
				"""MaxHPが変化したら同時にHPも変化する"""
				u_ns[u_s_s_l]["text"] = str(la_n)
				u_ns[0]["text"] = str(int(u_ns[0]["text"])+ch)
			else:
				u_ns[u_s_s_l]["text"] = str(la_n)
			"""Menが-1になったら死亡"""
			if u_ns[3]["text"] == "-1":
				units[num][0]["text"] = "むりぽ"
				units[num][2] = -1
		else:
			"""ゲーム開始前ならいじっても気絶とかにしない"""
			"""HPはMaxHP以下なら変化する"""
			if u_s_s_l == 0:
				if la_n <= int(u_ns[1]["text"]):
					u_ns[0]["text"] = str(la_n)
			elif u_s_s_l == 1:
				"""MaxHPが変化したらHPも変化する"""
				u_ns[u_s_s_l]["text"] = str(la_n)
				u_ns[0]["text"] = str(int(u_ns[0]["text"])+ch)
			else:
				u_ns[u_s_s_l]["text"] = str(la_n)
	return num_ch

"""
攻撃を行ったときの処理
code = True 自動で計算する処理, False 攻撃したという処理のみ
num = どちらの陣営のユニットが攻撃したか0 左側, 1 右側
"""
def attackback(code,num):
	"""計算もやる方"""
	def attacked():
		"""ユニットが気絶、死亡状態なら攻撃できない"""
		if units[battle_set[(num*-1)+1]][2] != 0:
			return None
		"""ユニットがすでに攻撃しているかを見る"""
		if battle_set[num] >= 0:
			unit = units[battle_set[num]]
			if unit[2] == 0 and unit[0]["text"][-1]=="゜":
				unit[0]["text"] =  unit[3]
				canatk = True
			else:
				canatk = False
		else:
			"""num=-1は顔"""
			canatk = True
		"""攻撃可能なら攻撃"""
		if canatk:
			"""カウンターがあるので、双方攻撃計算実行"""
			for p_num in range(2):
				u_num = battle_set[p_num]
				"""ユニットまたは顔のAtkを取得"""
				if u_num >= 0:
					atk_num = units[u_num][1][2]["text"]
				else:
					atk_num = le_stas[p_num][2]["text"]
				atk_num = int(atk_num)
				u_num = battle_set[p_num*-1+1]
				e_num = p_num*-1+1
				"""ユニットならユニットのHP減少させるメソッド呼び出し
					顔なら普通に殴られた後のHPに変更"""
				if u_num >= 0:
					for _ in range(atk_num):
						unitback(u_num,-1,0)()
				else:
					le_stas[e_num][1]["text"]=int(le_stas[e_num][1]["text"])-atk_num
	"""攻撃したとわからせるための方"""
	def attackch():
		if units[num][2] == 0:
			units[num][0]["text"] = units[num][3]
	if code:
		return attacked
	else:
		return attackch
"""
セクション変化
enterキーに反応させるためにeventを持ってるが使わん
"""
def ch_tu(event):
	t_s = int(t_s_n["text"])+1
	"""セクションが3超過ならターンを増加"""
	if t_s > 3:
		t_s_n["text"] = "1"
		t_t_n["text"] = str(int(t_t_n["text"])+1)
		"""ユニットが気絶から復帰するかチェック"""
		for unit in units:
			if unit[2] > 0:
				"""ユニットが気絶状態なら復帰までのターンを1減らし
					さらにそのターンが0なら復帰させる"""
				unit[2] -= 1
				if unit[2] == 0:
					unit[0]["text"] = "　"+unit[3]+"゜"
					unit[1][0]["text"] = unit[1][1]["text"]
			elif unit[0]["text"][-1]!="゜":
				"""ターン経過後ユニットが攻撃権を回復"""
				unit[0]["text"] = "　"+unit[3]+"゜"
		"""最大マナを1増加させマナ全回復"""
		for stas in le_stas:
			num = int(stas[4]["text"])
			if num < 10:
				stas[4]["text"] = str(num+1)
			stas[3]["text"] = stas[4]["text"]
	else:
		t_s_n["text"] = str(t_s)
	tu_st[0]["text"], tu_st[1]["text"] = tu_st[1]["text"], tu_st[0]["text"]
	# 3セクションで気絶から復帰の名残
	#for num in range(len(units)):
	#	if units[num][2] > 0:
	#		units[num][2] -= 1
	#		if units[num][2] == 0:
	#			u_n = num%3+1
	#			units[num][0]["text"] = "　"+units[num][3]+"゜"
	#			units[num][1][0]["text"] = units[num][1][1]["text"]
	t_n_t["text"] = "60.0"
"""
初期値の入力自動化
"""
def start_set():
	t_s_n["text"] = "1"
	t_t_n["text"] = "1"
	for stas in le_stas:
		stas[0]["text"] = "0"
		stas[1]["text"] = "25"
		stas[2]["text"] = "0"
		stas[3]["text"] = "3"
		stas[4]["text"] = "3"
	for u_n,unit in enumerate(units):
		for i in range(4):
			unit[1][i]["text"] = "0"
		unit[2] = 0
		unit[0]["text"] = "　"+str(unit[3])+"゜"
	t_n_t["text"] = "60.0"
"""
ゲーム開始および停止のボタン操作内容
"""
def gamestart():
	global start_now
	"""ゲーム中ならタイマー停止"""
	if start_now:
		start_now = False
		tu_t_b["text"] = "game start"
	else:
		"""停止中ならタイマー再始動"""
		start_now = True
		tu_t_b["text"] = "game stop"
		count()
"""
タイマーカウントを実行する
"""
def count():
	time = [int(i) for i in t_n_t["text"].split(".")]
	"""0.0秒になったら止める"""
	if time[0]+time[1] == 0:
		pass
	elif time[0] == 0 and time[1] == 1:
		"""時間切れならなんか音楽流すときの"""
		#os.system("afplay ./ちゃらちゃらちゃら.mp3 &")
		time[1] -= 1
	elif time[1]-1 == -1:
		time[0] -= 1
		time[1] = 9
	else:
		time[1] -= 1
	t_n_t["text"] = str(time[0]) + "." + str(time[1])
	"""ゲーム中ならタイマーカウントする"""
	if start_now:
		root.after(100,count)
"""
ユニットのID番号を入力するサブウインドウ
u_n = 対象となるユニットの通し番号0~5
"""
def u_n_s_back(u_n):
	def uni_name_set():
		"""ユニット番号入力の処理"""
		def sub_b_p(b_n):
			def b_p_b():
				"""数字キーなら入力"""
				if b_n >= 0:
					sub_w_n_l["text"] += str(b_n)
				else:
					"""デリートキーなら1文字削除"""
					sub_w_n_l["text"]=sub_w_n_l["text"][:-1]
			return b_p_b
		"""okボタンを押したらユニットの名前を変更し、
			このウインドウを削除する"""
		def ok_button():
			units[u_n][3] = sub_w_n_l["text"]
			units[u_n][0]["text"] = "　"+sub_w_n_l["text"]+"゜"
			sub_win.destroy()
		if start_now==False:
			sub_win = Tk.Toplevel()
			sub_win.title("unit name set")
			sub_w_l = Tk.Label(sub_win, text="write Unit number", font=("",st_si_h))
			sub_w_l.pack(side=Tk.TOP)
			sub_w_n_l = Tk.Label(sub_win,text="",font=("",st_si_h))
			sub_w_n_l.pack(side=Tk.TOP)
			sub_w_n_f = Tk.Frame(sub_win)
			for i,b_ns in enumerate([[7,8,9],[4,5,6],[1,2,3],[-2,0,-1]]):
				for j, b_n in enumerate(b_ns):
					if b_n >= 0:
						sub_w_nb = Tk.Button(sub_w_n_f,text=str(b_n),
							command=sub_b_p(b_n))
					elif b_n == -1:
						sub_w_nb = Tk.Button(sub_w_n_f,text="←",
							command=sub_b_p(b_n))
					else:
						sub_w_nb = Tk.Button(sub_w_n_f,text=" ",)
					sub_w_nb.grid(row=i,column=j)					
			sub_w_n_f.pack(side=Tk.TOP)
			sub_w_f = Tk.Frame(sub_win)
			sub_w_b = Tk.Button(sub_w_f,text="OK",font=("",st_si_h),
				command=ok_button)
			sub_w_b.pack(side=Tk.LEFT)
			sub_w_b = Tk.Button(sub_w_f,text="CANCEL",font=("",st_si_h),
				command=sub_win.destroy)
			sub_w_b.pack(side=Tk.LEFT)
			sub_w_f.pack(side=Tk.TOP)
	return uni_name_set
"""
攻撃被攻撃のユニット名もしくは顔の表示
"""
def battleback(u_num,pla_num,label):
	def batt_deci():
		battle_set[pla_num]=u_num
		if u_num < 0:
			label["text"] = "顔"
		else:
			label["text"] = units[u_num][3]
	return batt_deci

root = Tk.Tk()
root.title("leader parameter")
#root.geometry("800x800")

"""中央操作部"""
turnframe = Tk.Frame(root)
turnframe.grid(row=0,columnspan=3)
t_b_f = Tk.Frame(turnframe)
sta_b = Tk.Button(t_b_f, text="start set", command=lambda:start_set())
sta_b.pack(side=Tk.LEFT)
tu_b = Tk.Button(t_b_f, text="next turn", command=lambda:ch_tu(None))
tu_b.bind("<Return>",ch_tu)
tu_b.focus_set()
tu_b.pack(side=Tk.LEFT)
t_b_f.pack(side=Tk.TOP)
tu_t_b = Tk.Button(t_b_f, text="game start", command=lambda:gamestart())
tu_t_b.pack(side=Tk.LEFT)

"""ターン数など表示部"""
t_n_f = Tk.Frame(turnframe)
t_s_l = Tk.Label(t_n_f,text=" セクション ",font=("",st_si))
t_s_l.pack(side=Tk.LEFT)
t_s_n = Tk.Label(t_n_f,text="1",font=("",st_si))
t_s_n.pack(side=Tk.LEFT)
t_t_l = Tk.Label(t_n_f,text=" ターン ",font=("",st_si))
t_t_l.pack(side=Tk.LEFT)
t_t_n = Tk.Label(t_n_f,text="1",font=("",st_si))
t_t_n.pack(side=Tk.LEFT)

t_n_t = Tk.Label(t_n_f, text="00.0",font=("",st_si),padx=20)
t_n_t.pack(side=Tk.LEFT)

t_n_f.pack(side=Tk.TOP)

"""ステータスおよび攻撃操作盤表示フレーム作成"""

leftframe = Tk.Frame(root,relief="ridge",borderwidth=4)
leftframe.grid(row=1,column=0,padx=5)
centerframe = Tk.Frame(root)
centerframe.grid(row=1,column=1)
rightframe = Tk.Frame(root,relief="ridge",borderwidth=4)
rightframe.grid(row=1,column=2,padx=5)

"""ステータス表示部"""
for tu_n,(name, le_fr) in enumerate(zip(args[1:],[leftframe,rightframe])):
	tu_label = Tk.Label(le_fr, text=tu_st[tu_n], font=("",st_si))
	tu_st[tu_n] = tu_label
	tu_label.pack(side=Tk.TOP)
	l_A_label = Tk.Label(le_fr, text=name,font=("",st_si*2))
	l_A_label.pack(side=Tk.TOP)

	le_pa = Tk.Frame(le_fr,relief="groove",borderwidth=2,bg="gray")
	le_pa.pack(side=Tk.TOP)

	l_ns = ["VIT","HP","ATK","MN","MaxMN"]
	stas = []
	"""顔のステータス表示部"""
	for num, l_n in enumerate(l_ns):
		ln_f = Tk.Frame(le_pa,bg="gray")
		ln_f.pack(side=Tk.LEFT,padx=10,pady=5)
		ln = Tk.Label(ln_f, text=l_n, font=("",st_si),bg="gray")
		ln.pack()
		ln_n = Tk.Label(ln_f, text="0",font=("",st_si),bg="gray")
		ln_u_b = Tk.Button(ln_f, text="↑",
			command=callback(ln_n,1),font=("",st_si_h),bg="gray")
		ln_d_b = Tk.Button(ln_f, text="↓",
			command=callback(ln_n,-1),font=("",st_si_h),bg="gray")
		stas.append(ln_n)
		ln_u_b.pack()
		ln_n.pack()
		ln_d_b.pack()

	le_stas.append(stas)
	un_de = Tk.Frame(le_fr)
	un_de.pack(side=Tk.TOP)

	"""ユニット表示部"""
	for num in range(3):
		u_na = "　U"+str(num+1)+"゜"
		u_f = Tk.Frame(un_de)
		u_f.pack(side=Tk.LEFT,padx=10)
		u_l = Tk.Label(u_f, text=u_na,font=("",st_si),width=4)
		u_l.pack(side=Tk.TOP)
		u_n = tu_n*3 + num
		u_a_b = Tk.Button(u_f, text="Attack",font=("",st_si_h),
			command=attackback(False,u_n))
		u_a_b.pack(side=Tk.TOP)
		u_n_s = Tk.Button(u_f, text="set num", font=("",st_si_h),
			command=u_n_s_back(u_n))
		u_n_s.pack(side=Tk.TOP)
		#u_b = Tk.Button(u_f, text="m-1",command=unitback(u_l,u_n),font=("",20))
		#u_b.pack(side=Tk.TOP)
		#units.append([u_l,0])
		
		u_s = Tk.Frame(u_f)
		u_s_list = []
		"""ユニットのステータス表示部"""
		for u_s_num,u_s_s_l in enumerate(["H","MH","A","M"]):
			u_s_s = Tk.Frame(u_s)
			u_s_l = Tk.Label(u_s_s, text=u_s_s_l,font=("",st_si_h))
			u_s_l.pack(side=Tk.TOP)
			u_s_n = Tk.Label(u_s_s, text="0",font=("",st_si_h),width=2)
			u_s_list.append(u_s_n)
			u_s_u_b = Tk.Button(u_s_s, text="↑",
				command=unitback(u_n,1,u_s_num),font=("",st_si_h))
			u_s_d_b = Tk.Button(u_s_s, text="↓",
				command=unitback(u_n,-1,u_s_num),font=("",st_si_h))
			u_s_u_b.pack(side=Tk.TOP)
			u_s_n.pack(side=Tk.TOP)
			u_s_d_b.pack(side=Tk.TOP)
			u_s_s.pack(side=Tk.LEFT)
		u_s.pack(side=Tk.TOP)
		units.append([u_l,u_s_list,0,"U"+str(num+1)])

"""攻撃操作盤表示部"""
for b_n in range(2):
	b_b_f = Tk.Frame(centerframe)
	b_b_f.pack(side=Tk.LEFT)
	b_b_l = Tk.Label(b_b_f,text="",font=("",st_si_h))
	p_num = (b_n+1)*-1
	b_b_b_f = Tk.Button(b_b_f,text="顔",command=battleback(p_num,b_n,b_b_l))
	b_b_b_f.pack(side=Tk.TOP)
	for i in range(3):
		b_b_b_u = Tk.Button(b_b_f,text=units[b_n*3+i][3],
			command=battleback((b_n*3+i),b_n,b_b_l))
		b_b_b_u.pack(side=Tk.TOP)
	b_b_l.pack(side=Tk.TOP)
	b_b_ll = Tk.Label(b_b_f,text="が",font=("",st_si_h))
	b_b_ll.pack(side=Tk.TOP)
	b_b_b_a = Tk.Button(b_b_f, text="Attack",command=attackback(True,b_n))
	b_b_b_a.pack(side=Tk.TOP)

#l_B_label = Tk.Label(rightframe, text=args[2],font=("",40))
#l_B_label.pack(side=Tk.TOP)


root.mainloop()

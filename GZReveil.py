from guizero import App, PushButton, Slider, Text
from pygame import mixer
import sys
import signal
import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


app = App(title="Example", layout="grid")
#app.bg='black'

def main():
	app.tk.attributes("-fullscreen",True)
	app.tk.config(cursor='none')
	app.display()

def signal_handler(signal, frame):
	print('You pressed Ctrl+C!')
	print('Au revoir')
	sys.exit(0)

def set1():
	alarmset=1
	bouton_set1.toggle()
	heure_alarm1.value=''
	for v in boutons:
		v.toggle()
def playmusic():
	mixer.load('police.mp3')
	mixer.play(-1)

def num(args):
	global numchar,boutons
	temp=int(args)
	#print(args)
	#heure_alarm1.append(args)
	if numchar == 0:
		if temp > 2:
			numchar = 2
			heure_alarm1.append('0')
			heure_alarm1.append(args)
			heure_alarm1.append(':')
		else:
			numchar = 1
			heure_alarm1.append(args)
	elif numchar == 1:
		numchar = 2
		heure_alarm1.append(args)
		heure_alarm1.append(':')
	elif numchar == 2:
		if temp < 6:
			heure_alarm1.append(args)
			numchar=3
	elif numchar == 3:
		heure_alarm1.append(args)
		numchar=0
		for v in boutons:
			v.toggle()
		bouton_set1.toggle()
def quit():
	print('quit by HMI')
	sys.exit(0)
numchar = 0 #nombre de caracteres ajouté
mixer.init()
#fond = Text(app,text=' ',grid=[0,0,12,8])
#toto = Text(app,text='08:10',height=20,grid=[0,0])
bouton_quit = PushButton(app,text='X',command=quit,grid=[0,0])
heure_alarm1 = Text(app,text='08:20',grid=[0,1])
heure_alarm1.text_size = 50
#heure_alarm2 = Text(app,text='10:30',text_size=20,grid=[0,3])
bouton_set1 = PushButton(app,text=' Set Alarm 1 ',width='fill',grid=[0,2],command=set1)
bouton_set1.text_size=30

b1 = PushButton(app,text=' 1 ',grid=[1,1],command=num,args='1')
b2 = PushButton(app,text=' 2 ',grid=[2,1],command=num,args='2')
b3 = PushButton(app,text=' 3 ',grid=[3,1],command=num,args='3')
b4 = PushButton(app,text=' 4 ',grid=[1,2],command=num,args='4')
b5 = PushButton(app,text=' 5 ',grid=[2,2],command=num,args='5')
b6 = PushButton(app,text=' 6 ',grid=[3,2],command=num,args='6')
b7 = PushButton(app,text=' 7 ',grid=[1,3],command=num,args='7')
b8 = PushButton(app,text=' 8 ',grid=[2,3],command=num,args='8')
b9 = PushButton(app,text=' 9 ',grid=[3,3],command=num,args='9')
bv = PushButton(app,text='   ',grid=[1,4])
b0 = PushButton(app,text=' 0 ',grid=[2,4],command=num,args='0')
bV = PushButton(app,text='   ',grid=[3,4])
boutons=[b1,b2,b3,b4,b5,b6,b7,b8,b9,b0,bv,bV]
for v in boutons:
	#print(v)
	v.text_size = 50
	v.toggle()

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
	main()


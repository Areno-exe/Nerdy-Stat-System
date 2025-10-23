from ursina import *
# Idea is to make GUI elements that click and do stuff
app=Ursina('Stats!')

EXP=0
Level=0
EXPreq=10

EXP_Display=Text(text=f'EXP:{EXP}/{EXPreq}',color=color.green,x=-.75,scale=2)
Level_Display=Text(text=f'Level:{Level}',color=color.yellow,x=-.75,scale=2,y=-.1)
my_button = Button(text='Click Me!',color=color.azure,x=0,y=-0.1,scale=(0.3, 0.1)) #Creates Button

def update():
	global EXPreq
	global EXP
	if EXP>=EXPreq:
		Level_Up_Event()
		update()
def Level_Up_Event(): #Update Level, EXP, and EXP_Req
	global EXP,EXPreq,Level
	level_up_text=Text('LEVEL UP!', scale=3, color=color.yellow,x=.5,y=.5)
	Level+=1
	level_up_text.fade_out(duration=3)
	remainingEXP=EXP-EXPreq
	EXP=remainingEXP
	EXPreq=Level*2+10
	Level_Display.text=f'Level:{Level}'
	EXP_Display.text=f'EXP:{EXP}/{EXPreq}'

def on_button_click(): #Assigns Function to button
	global EXP
	my_text=Text(text='+1 EXP',scale=2,color=color.green,origin=(0, 0),y=0.4)
	my_text.fade_out(duration=0.75)
	EXP+=1
	EXP_Display.text=f'EXP:{EXP}/{EXPreq}'
my_button.on_click = on_button_click


app.run()
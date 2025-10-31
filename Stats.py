from ursina import * 
import math ; import random ; import pickle ; import os ; import collections.abc
app=Ursina('Game Stats')
window.fullscreen=True
game_state='menu'

# Reopening the menu doesn't hide the stuff behind it. You'll likely need to put all the ui in a master list and disable them all
# -- UI Elements -- Start Menu --

Start_Menu_Panel=Entity(parent=camera.ui,texture='black-white-box',model='quad',scale=(1*window.aspect_ratio,1),z=-20)
# -- Menu Buttons --
Start_Button=Button(parent=Start_Menu_Panel,texture='game-button',text='Start Game',color=color.orange,scale=(0.3,0.1),position=(0,.1,-1))
Quit_Button=Button(parent=Start_Menu_Panel,texture='game-button',text='Quit Game',color=color.orange,scale=(0.3,0.1),position=(0,-.1,-1))

# -- Logic -- Start Menu --

def Start_Game():
	global game_state
	game_state='game'
	Start_Menu_Panel.fade_out(duration=1)
	Start_Menu_Panel.enabled=False
	update_game_state()

def Quit_Game():
	application.quit()

Start_Button.on_click=Start_Game
Quit_Button.on_click=Quit_Game

# -- Variables & UI -- The Player --

Bar_Colors=[color.rgb(196/255, 14/255, 14/255),color.rgb(240/255, 137/255, 2/255),color.rgb(226/255, 237/255, 21/255), # Red, Orange, Yellow
	color.rgb(30/255, 181/255, 13/255),color.rgb(20/255, 227/255, 250/255), # Green, Turqoise
	color.rgb(14/255, 26/255, 196/255),color.rgb(106/255, 9/255, 217/255),color.rgb(242/255, 41/255, 112/255), # Blue, Purple, Pink-Red
	color.rgb(237/255, 83/255, 245/255),color.rgb(209/255, 207/255, 207/255)] # Bubblegum Pink, Dusty White

Player_Stats={
	"Name":'Zena',
	"Max_Health":493,"Current_Health":1,"EXP_Health":0,"Segment_Size":0,"Count_of_Health_Bars":0,"NEXT_LEVEL_Health":0, # Health Stats
	"Max_Defense":50,"Current_Defense":1,"EXP_Defense":0,"NEXT_LEVEL_Defense":0, # Defense Stats
	"Max_Strength":10,"Current_Strength":1,"EXP_Strength":0,"NEXT_LEVEL_Strength":0 # Strength Stats
	}
Player_UI={
	# -- Health UI --
	"Health_Bar_bg":Entity(parent=camera.ui,model='quad',color=color.black50,scale=(0.7, 0.06),origin=(-0.5, 0),position=(-0.5*window.aspect_ratio,0.48,1)),
	"Health_Text":0,"EXP_Health_Text":0,"Health_Bars":[],
	# -- Defense UI --
	"Defense_bg":Entity(parent=camera.ui,model='quad',color=color.rgba(12/255,14/255,54/255),scale=(0.7,0.06),origin=(-0.5,0),position=(-0.5*window.aspect_ratio,0.42,-0.25)),
	"Defense_Text":0,"Defense_fg":0,"EXP_Defense_Text":0,
	# -- Strength UI --
	"Strength_bg":Entity(parent=camera.ui,model='quad',color='#964a0c',scale=(0.7,0.06),origin=(-0.5,0),position=(-0.5*window.aspect_ratio,0.36,-0.25)),
	"Strength_Text":0,"Strength_fg":0,"EXP_Defense_Text":0
	}
Player_Stats["Segment_Size"]=10**math.floor(math.log10(Player_Stats["Max_Health"]))
Player_Stats["Count_of_Health_Bars"]=math.ceil(Player_Stats["Max_Health"]/Player_Stats["Segment_Size"])
Player_Stats["NEXT_LEVEL_Health"]=round(math.log(Player_Stats["Max_Health"]),3)+10
Player_Stats["NEXT_LEVEL_Defense"]=10+round(math.log(Player_Stats["Max_Defense"]),3)
Player_Stats["NEXT_LEVEL_Strength"]=10+round(math.log(Player_Stats["Max_Strength"]),3)
Player_UI["Health_Text"]=Text(parent=Player_UI["Health_Bar_bg"],text=f'HP:{Player_Stats["Current_Health"]:.1f}/{Player_Stats["Max_Health"]:.1f}',color=color.white,scale=(2,20),origin=(-0.5,0),z=-2)
Player_UI["EXP_Health_Text"]=Text(parent=Player_UI["Health_Bar_bg"],text=f'EXP: {Player_Stats["EXP_Health"]:.1f}/{Player_Stats["NEXT_LEVEL_Health"]:.1f}',origin=(-0.5,0),color=Bar_Colors[3],scale=(2,30),position=(1,-0.02))
Player_UI["Defense_Text"]=Text(parent=Player_UI["Defense_bg"],text=f'Defense: {round(Player_Stats["Current_Defense"])}',color=color.white,scale=(2,20),origin=(-0.5,0),z=-1)
Player_UI["Defense_fg"]=Entity(parent=Player_UI["Defense_bg"],model='quad',texture='health-bar-vector',color=color.rgb(40/255,47/255,247/255),scale=(1,1),origin=(-0.5,0),z=-0.26)
Player_UI["EXP_Defense_Text"]=Text(parent=Player_UI["Defense_bg"],text=f'EXP: {Player_Stats["EXP_Defense"]:.1f}/{Player_Stats["NEXT_LEVEL_Defense"]:.1f}',origin=(-0.5,0),color=Bar_Colors[5],scale=(2,30),position=(1,0))
Player_UI["Strength_Text"]=Text(parent=Player_UI["Strength_bg"],text=f'Strength: {round(Player_Stats["Current_Strength"])}',color=color.white,scale=(2,20),origin=(-0.5,0),z=-1)
Player_UI["Strength_fg"]=Entity(parent=Player_UI["Strength_bg"],model='quad',texture='health-bar-vector',color='#f7952d',z=-0.5,origin=(-0.5,0))
Player_UI["EXP_Strength_Text"]=Text(parent=Player_UI["Strength_bg"],color=color.hex('#f7952d'),text=f'EXP: {Player_Stats["EXP_Strength"]:.1f}/{Player_Stats["NEXT_LEVEL_Strength"]:.1f}',origin=(-0.5,0),scale=(2,30),position=(1,0))

# -- Variables -- Not Implemented -- Ideas for later; Order is roughly planned implementation route --

Level=0
EXP=0
Turn=0
Regeneration=0

# -- Buttons --

Lever_Button_Pannel=Button(parent=camera.ui,text='',texture='left-arrow-thumb-box',color=color.orange,origin=(0.5,0.5),position=(0.5*window.aspect_ratio,-0.4),scale=(0.05,0.05))
Lever_Button_Pannel_Out=Button(parent=camera.ui,text='',texture='left-arrow-thumb-box',color=color.orange,origin=(0.5,0.5),position=(0.5*window.aspect_ratio-0.4,-0.4),scale=(0.05,0.05))
Button_Pannel=Entity(parent=camera.ui,model='quad',color=color.black50,origin=(0.5,0),scale=(0.4,1),position=(0.5*window.aspect_ratio,0,-1))
Damage_Button=Button(parent=Button_Pannel,texture='game-button-2',text="You Masochist (;",color=color.red,origin=(0,0),position=(-0.5,-0.1,-1),scale=(0.9, 0.1))
Heal_Button=Button(parent=Button_Pannel,texture='game-button-2',text='How Boring ):',color=color.green,origin=(0,0),position=(-0.5,0.1,-1),scale=(0.9,0.1))
Corrosion_Button=Button(parent=Button_Pannel,texture='game-button-2',text='More Damage!',color=color.azure,origin=(0,0),position=(-0.5,0),scale=(0.9,0.1))
Weaken_Button=Button(parent=Button_Pannel,texture='game-button-2',text='Weaker Darling',color=color.orange,origin=(0,0),position=(-0.5,-0.2),scale=(0.9,0.1))
Save_Button=Button(parent=camera.ui,text='Save',color=color.black,scale=(0.2,0.1),position=(-0.105,-0.45))
Load_Button=Button(parent=camera.ui,text='Load',color=color.black,scale=(0.2,0.1),position=(0.105,-0.45))

# -- Logic -- Game Data ; Saving & Loading --

def Save_Data(*args,filename='save.dat'):
	'''
	Saves current game state to a file called "save.dat" in the "Saves" subfolder
	'''
	base_dir=os.path.dirname(__file__)
	save_dir=os.path.join(base_dir,'saves')
	os.makedirs(save_dir,exist_ok=True)
	path=os.path.join(save_dir, filename)
	with open(path,'wb') as f:
		pickle.dump(Player_Stats,f)
	save_text=Text(parent=camera.ui,text='Game Saved!',origin=(0,0),scale=2,position=(0,-0.375))
	destroy(save_text,delay=3)

def Load_Data(filename='save.dat'):
	'''
	Loads game data, this is stored in a file called "save.dat" in the "Saves" subfolder
	'''
	base_dir=os.path.dirname(__file__)
	save_dir=os.path.join(base_dir,'saves')
	path=os.path.join(save_dir, filename)
	try:
		with open(path,'rb') as f:
			loaded_data=pickle.load(f)
			load_text=Text(parent=camera.ui,text='Game loaded successfully!',origin=(0,0),scale=2,position=(0,-0.375))
			destroy(load_text,delay=3)
			Player_Stats=loaded_data
			Rebuild_Health_Bars(Player_Stats,Player_UI)
			Multi_Health_Update(Player_Stats["Current_Health"],Player_Stats,Player_UI)
			Defense_Update(Player_Stats["Current_Defense"],Player_Stats,Player_UI)
			Health_EXP_Update(0,Player_Stats,Player_UI)
			Defense_EXP_Update(0,Player_Stats,Player_UI)
			Strength_Update(Player_Stats["Current_Strength"],Player_Stats,Player_UI)
	except FileNotFoundError:
		load_text=Text(parent=camera.ui,text='Save file not found!',origin=(0,0),scale=2,position=(0,-0.375))
		destroy(load_text,delay=3)
		return None

Save_Button.on_click=Save_Data
Load_Button.on_click=Load_Data

# -- Logic -- Health --

def Multi_Health_Update(new_health,target_stats,target_ui):
	'''
	Updates the Multi-Health Bar System after recieving damage or healing
	'''
	target_stats["Current_Health"]=clamp(new_health,0,target_stats["Max_Health"])
	target_ui["Health_Text"].text=f'HP:{target_stats["Current_Health"]:.1f}/{target_stats["Max_Health"]:.1f}'
	for i,bar in enumerate(target_ui["Health_Bars"]):
		barmax=math.ceil(target_stats["Max_Health"]/target_stats["Segment_Size"])*target_stats["Segment_Size"]-i*target_stats["Segment_Size"]
		barmin=barmax-target_stats["Segment_Size"]
		if target_stats["Current_Health"]>=barmax:
			bar.scale_x=1
		elif target_stats["Current_Health"]<=barmin:
			bar.scale_x=0
		elif target_stats["Current_Health"]>barmin and target_stats["Current_Health"]<barmax:
			segment_health=target_stats["Current_Health"]-barmin
			bar.scale_x=segment_health/target_stats["Segment_Size"]
		else:
			bar.scale_x=0
		if target_stats["Current_Health"]<=0:
			Defeat_Text_bg=Entity(parent=camera.ui,model='quad',color=color.black,origin=(0,0),scale=(1,0.5),z=-5)
			Defeat_Text=Text(parent=camera.ui,text='You Died ):',color=color.red,scale=8,origin=(0,0),always_on_top=True)
			Defeat_Text.fade_out(duration=5) ; Defeat_Text_bg.fade_out(duration=5)
			destroy(Defeat_Text,delay=5) ; destroy(Defeat_Text_bg,delay=5)

def Health_EXP_Update(exp,target_stats,target_ui):
	'''
	Updates Health EXP indicator and the variable based on incoming damage
	'''
	exp=math.log(exp+1)
	target_stats["EXP_Health"]+=exp
	target_ui["EXP_Health_Text"].text=f'EXP: {target_stats["EXP_Health"]:.1f}/{target_stats["NEXT_LEVEL_Health"]:.1f}'
	while target_stats["EXP_Health"]>=target_stats["NEXT_LEVEL_Health"]:
		target_stats["EXP_Health"]-=target_stats["NEXT_LEVEL_Health"]
		target_stats["Max_Health"]+=1
		target_stats["NEXT_LEVEL_Health"]=10+math.log(target_stats["Max_Health"])
		target_ui["EXP_Health_Text"].text=f'EXP: {target_stats["EXP_Health"]:.1f}/{target_stats["NEXT_LEVEL_Health"]:.1f}'
		Rebuild_Health_Bars(target_stats,target_ui)
		Multi_Health_Update(target_stats["Current_Health"],target_stats,target_ui)

def Rebuild_Health_Bars(target_stats,target_ui):
	'''
	Recontructs Health Bars, use if Max Health gets modified at all
	'''
	for bar in target_ui["Health_Bars"]:
		destroy(bar)
	target_ui["Health_Bars"].clear()
	target_stats["Segment_Size"]=10**math.floor(math.log10(target_stats["Max_Health"]))
	target_stats["Count_of_Health_Bars"]=math.ceil(target_stats["Max_Health"]/target_stats["Segment_Size"])
	for i in range(target_stats["Count_of_Health_Bars"]): # Going to use idea that i=0 is top bar, descending. If Max_Health=400, i=0 is green
		base_index=(target_stats["Count_of_Health_Bars"]-1)-i
		Color_index=base_index % len(Bar_Colors)
		bar=Entity(parent=target_ui["Health_Bar_bg"],model='quad',texture='health-bar-vector',scale=(1,1),origin=(-0.5,0),position=(0,0,-1+0.05*i))
		bar.color=Bar_Colors[Color_index]
		target_ui["Health_Bars"].append(bar)

# -- Logic -- Defense --

def Damage_via_Defense(Damage,target_stats,target_ui):
	'''
	Calculates damage taken through defense value; damage dealt will be a fraction of total damage
	'''
	percent_reduction=1-(1/math.cosh(Damage/target_stats["Current_Defense"]))
	final_damage=Damage*(percent_reduction)
	final_damage1=clamp(round(final_damage,3),0,target_stats["Current_Health"])
	print(f'Blocked {Damage-final_damage1} Damage')
	Health_EXP_Update(final_damage1,target_stats,target_ui)
	Multi_Health_Update(target_stats["Current_Health"]-final_damage1,target_stats,target_ui)
	Defense_EXP_Update(clamp((Damage-final_damage1),0,target_stats["Current_Health"]),target_stats,target_ui)

def Defense_Update(new_defense,target_stats,target_ui):
	'''
	Updates defense value after recieving a change
	'''
	target_stats["Current_Defense"]=clamp(new_defense,0,target_stats["Max_Defense"])
	target_ui["Defense_Text"].text=f'Defense: {round(target_stats["Current_Defense"])}'
	target_ui["Defense_fg"].scale_x=target_stats["Current_Defense"]/target_stats["Max_Defense"]

def Defense_EXP_Update(exp,target_stats,target_ui):
	'''
	Updates defense experience and checks if it has leveled up or not ; this DOES NOT update the defense UI
	'''
	exp=math.log10(exp+1)
	target_stats["EXP_Defense"]+=exp
	target_ui["EXP_Defense_Text"].text=f'EXP: {target_stats["EXP_Defense"]:.1f}/{target_stats["NEXT_LEVEL_Defense"]:.1f}'
	while target_stats["EXP_Defense"]>=target_stats["NEXT_LEVEL_Defense"]:
		target_stats["EXP_Defense"]-=target_stats["NEXT_LEVEL_Defense"]
		target_stats["Max_Defense"]+=1
		target_stats["NEXT_LEVEL_Defense"]=10+round(math.log(target_stats["Max_Defense"]),3)
		target_ui["EXP_Defense_Text"].text=f'EXP: {target_stats["EXP_Defense"]:.1f}/{target_stats["NEXT_LEVEL_Defense"]:.1f}'
		Defense_Update(target_stats["Current_Defense"]+1,target_stats,target_ui)

# -- Logic -- Strength --

# def Dealt_via_Strength(enemy_defense):


def Strength_Update(new_strength,target_stats,target_ui):
	'''
	Updates strength value after recieving a change
	'''
	target_stats["Current_Strength"]=clamp(new_strength,0,target_stats["Max_Strength"])
	target_ui["Strength_Text"].text=f'Strength: {round(target_stats["Current_Strength"])}'
	target_ui["Strength_fg"].scale_x=target_stats["Current_Strength"]/target_stats["Max_Strength"]

def Strength_EXP_Update(exp,target_stats,target_ui):
	'''
	Updates strength experience and checks if it has leveled up or not ; this DOES NOT update the strength UI
	'''
	exp=math.log10(exp+1)
	target_stats["EXP_Strength"]+=exp
	target_ui["EXP_Strength_Text"].text=f'EXP: {target_stats["EXP_Strength"]:.1f}/{target_stats["NEXT_LEVEL_Strength"]:.1f}'
	while target_stats["EXP_Strength"]>=target_stats["NEXT_LEVEL_Strength"]:
		target_stats["EXP_Strength"]-=target_stats["NEXT_LEVEL_Strength"]
		target_stats["Max_Strength"]+=1
		target_stats["NEXT_LEVEL_Strength"]=10+round(math.log(target_stats["Max_Strength"]),3)
		target_ui["EXP_Strength_Text"].text=f'EXP: {target_stats["EXP_Strength"]:.1f}/{target_stats["NEXT_LEVEL_Strength"]:.1f}'
		Strength_Update(target_stats["Current_Strength"]+1,target_stats,target_ui)

# -- Logic -- Monsters -- 



# -- Logic -- Button Pannel --

def Open_Button_Pannel():
	Lever_Button_Pannel.enabled=False
	Button_Pannel.enabled=True
	Lever_Button_Pannel_Out.enabled=True

def Close_Button_Pannel():
	Lever_Button_Pannel.enabled=True
	Button_Pannel.enabled=False
	Lever_Button_Pannel_Out.enabled=False

Lever_Button_Pannel.on_click=Open_Button_Pannel
Lever_Button_Pannel_Out.on_click=Close_Button_Pannel

# -- Logic -- Damage Button --

def Damage_button_click():
	'''
	Randomly Damages Player 30-75 Damage
	'''
	Damage=random.randint(30,75)
	print(f"Took {Damage} Damage")
	Damage_via_Defense(Damage,Player_Stats,Player_UI)
Damage_Button.on_click=Damage_button_click

# -- Logic -- Health Button --

def Heal_Button_click():
	'''
	Randomly Heals Player 40-60 Health
	'''
	heal=random.randint(40,60)
	Multi_Health_Update(Player_Stats["Current_Health"]+heal,Player_Stats,Player_UI)
Heal_Button.on_click=Heal_Button_click

# -- Logic -- Corrosion Button --

def Corrosion_Button_click():
	'''
	Randomly Corrodes Player Defense 1-5 points
	'''
	corrosion=random.randint(1,5)
	Defense_Update(Player_Stats["Current_Defense"]-corrosion,Player_Stats,Player_UI)
Corrosion_Button.on_click=Corrosion_Button_click

# -- Logic -- Weaken Button --

def Weaken_Button_click():
	'''
	Randomly Weakens Player Strength 1-5 points
	'''
	weaken=random.randint(1,5)
	Strength_Update(Player_Stats["Current_Strength"]-weaken,Player_Stats,Player_UI)
Weaken_Button.on_click=Weaken_Button_click

# -- Logic -- Menu Open & Close --

Game_UI_Master_List=[Lever_Button_Pannel,*Player_UI.values()]
Menu_UI_Master_List=[Start_Menu_Panel,Save_Button,Load_Button]

def update_game_state():
	'''
	Prevents buttons from being assigned a function while in the start menu.
	'''
	for item in Game_UI_Master_List:
		if isinstance(item,collections.abc.Iterable):
			Game_UI_Master_List.remove(item)
	if game_state=='menu':
		Close_Button_Pannel()
		for i in Game_UI_Master_List:
			i.enabled=False
		for i in Menu_UI_Master_List:
			i.enabled=True
		pass
	else:
		for i in Game_UI_Master_List:
			i.enabled=True
		for i in Menu_UI_Master_List:
			i.enabled=False

def Open_Menu(key):
	global game_state
	if key=='escape':
		if game_state=='game':
			game_state='menu'
			update_game_state()
			Start_Button.text='Continue'
		else:
			game_state='game'
			update_game_state()
def input(key):
	Open_Menu(key)

# -- Starting Updates & Run --
Button_Pannel.enabled=False
Lever_Button_Pannel_Out.enabled=False
update_game_state()
Rebuild_Health_Bars(Player_Stats,Player_UI)
Multi_Health_Update(Player_Stats["Max_Health"],Player_Stats,Player_UI)
Defense_Update(Player_Stats["Max_Defense"],Player_Stats,Player_UI)
Strength_Update(Player_Stats["Max_Strength"],Player_Stats,Player_UI)
app.run()

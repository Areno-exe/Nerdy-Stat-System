from ursina import *
import math
import random
app=Ursina('Game Stats')

# Fix the Stacking Health Bars, it doesn't seem to line up properly
# -- Variables -- Implemented -- Health --

Max_Health=30
Current_Health=1
Segment_Size=10**math.floor(math.log10(Max_Health))
Count_of_Health_Bars=math.ceil(Max_Health/Segment_Size)
Segment_Scaling=1/Count_of_Health_Bars
Health_Bars=[]
EXP_Health=0
NEXT_LEVEL_Health=10+round(math.log(Max_Health),3)

# -- Variables -- Implemented -- Defense (Physical Damage Reduction) --

Max_Defense=150
Current_Defense=1

# -- Variables -- Not Implemented -- Strength (Physical Attack) --

Max_Strength=10
Strength=10

# -- Variables -- Not Implemented -- Ideas for later; Order is roughly planned implementation route --

Level=0
EXP=0
Turn=0
Regeneration=0

# -- UI Elements -- Health Bar --

Health_Bar_bg=Entity(parent=camera.ui,model='quad',color=color.black33,scale=(0.5, 0.04),origin=(-0.5, 0),position=(-0.75,0.48,-0.25))
Health_Text=Text(parent=Health_Bar_bg,text=f'HP:{Current_Health:.1f}/{Max_Health:.1f}',color=color.white,scale=(2,20),origin=(-0.5,0),always_on_top=True)
Bar_Colors=[color.rgb(196/255, 14/255, 14/255),color.rgb(240/255, 137/255, 2/255),color.rgb(226/255, 237/255, 21/255), # Red, Orange, Yellow
	color.rgb(30/255, 181/255, 13/255),color.rgb(20/255, 227/255, 250/255), # Green, Turqoise
	color.rgb(14/255, 26/255, 196/255),color.rgb(106/255, 9/255, 217/255),color.rgb(242/255, 41/255, 112/255), # Blue, Purple, Pink-Red
	color.rgb(237/255, 83/255, 245/255),color.rgb(209/255, 207/255, 207/255)] # Bubblegum Pink, Dusty White
EXP_Health_Text=Text(parent=camera.ui,text=f'EXP: {EXP_Health:.1f}/{NEXT_LEVEL_Health:.1f}',origin=(-0.5,0),color=Bar_Colors[3],scale=(1,1),position=(-0.25,0.48))

# -- UI Elements -- Defense --

Defense_bg=Entity(parent=camera.ui,model='quad',color=color.rgba(12/255,14/255,54/255,83/255),scale=(0.5,0.04),origin=(-0.5,0),position=(-0.75,0.44,-0.25))
Defense_Text=Text(parent=Defense_bg,text=f'Defense: {round(Current_Defense)}',color=color.white,scale=(2,20),origin=(-0.5,0),always_on_top=True)
Defense_fg=Entity(parent=Defense_bg,model='quad',color=color.rgb(40/255,47/255,247/255),scale=(1,1),origin=(-0.5,0))

# -- Buttons --

Damage_Button=Button(parent=camera.ui,text="You Masochist (;",color=color.red,x=0,y=-0.1,scale=(0.3, 0.1))
Heal_Button=Button(parent=camera.ui,text='How Boring ):',color=color.green,position=(0,0.1),scale=(0.3,0.1))
Corrosion_Button=Button(parent=camera.ui,text='More Damage!',color=color.azure,position=(0,0),scale=(0.3,0.1))

# -- Logic -- Health --

def Multi_Health_Update(new_health):
	'''
	Updates the Multi-Health Bar System after recieving damage or healing
	'''
	global Current_Health,Max_Health
	Current_Health=clamp(new_health,0,Max_Health)
	Health_Text.text=f'HP:{Current_Health:.1f}/{Max_Health:.1f}'
	for i,bar in enumerate(Health_Bars):
		barmax=math.ceil(Max_Health/Segment_Size)*Segment_Size-i*Segment_Size
		barmin=barmax-Segment_Size
		if Current_Health>=barmax:
			bar.scale_x=1
		elif Current_Health<=barmin:
			bar.scale_x=0
		elif Current_Health>barmin and Current_Health<barmax:
			segment_health=Current_Health-barmin
			bar.scale_x=segment_health/Segment_Size
		else:
			bar.scale_x=0
		if Current_Health<=0:
			Defeat_Text=Text(parent=camera.ui,text='You Died ):',color=color.red,scale=8,origin=(0,0))
			Defeat_Text.fade_out(duration=5)
			destroy(Defeat_Text,delay=5)

def Health_EXP_Update(exp):
	'''
	Updates Health EXP indicator and the variable based on incoming damage
	'''
	global EXP_Health,NEXT_LEVEL_Health,Max_Health
	EXP_Health+=exp
	EXP_Health_Text.text=f'EXP: {EXP_Health:.1f}/{NEXT_LEVEL_Health:.1f}'
	while EXP_Health>=NEXT_LEVEL_Health:
		EXP_Health-=NEXT_LEVEL_Health
		Max_Health+=1
		NEXT_LEVEL_Health=10+math.log(Max_Health)
		EXP_Health_Text.text=f'EXP: {EXP_Health:.1f}/{NEXT_LEVEL_Health:.1f}'
		Rebuild_Health_Bars()
		Multi_Health_Update(Current_Health)

def Rebuild_Health_Bars():
	'''
	Recontructs Health Bars, use if Max Health gets modified at all
	'''
	global Segment_Size, Count_of_Health_Bars, Segment_Scaling, Health_Bars
	for bar in Health_Bars:
		destroy(bar)
	Health_Bars.clear()
	Segment_Size=10**math.floor(math.log10(Max_Health))
	Count_of_Health_Bars=math.ceil(Max_Health/Segment_Size)
	Segment_Scaling=1/Count_of_Health_Bars	
	for i in range(Count_of_Health_Bars): # Going to use idea that i=0 is top bar, descending. If Max_Health=400, i=0 is green
		base_index=(Count_of_Health_Bars-1)-i
		Color_index=base_index % len(Bar_Colors)
		bar=Entity(parent=Health_Bar_bg,model='quad',scale=(1,Segment_Scaling),origin=(-0.5,-0.5),position=(0,Segment_Scaling*i-0.5,0.01*i),ignore_depth=True)
		bar.color=Bar_Colors[Color_index]
		Health_Bars.append(bar)

# -- Logic -- Defense --

def Damage_via_Defense(Damage):
	global Current_Defense,Current_Health
	percent_reduction=1-(1/math.cosh(Damage/Current_Defense))
	final_damage=Damage*(percent_reduction)
	final_damage1=clamp(round(final_damage,3),0,Current_Health)
	print(f'Blocked {Damage-final_damage1} Damage')
	Health_EXP_Update(final_damage1)
	Multi_Health_Update(Current_Health-final_damage1)

def Defense_Update(new_defense):
	global Current_Defense
	Current_Defense=clamp(new_defense,0,Max_Defense)
	Defense_Text.text=f'Defense: {round(Current_Defense)}'
	Defense_fg.scale_x=Current_Defense/Max_Defense

# -- Logic -- Damage Button --

def Damage_button_click():
	'''
	Randomly Damages Player 25-75 Damage
	'''
	global Current_Health
	Damage=random.randint(25,75)
	print(f"Took {Damage} Damage")
	Damage_via_Defense(Damage)

Damage_Button.on_click=Damage_button_click

# -- Logic -- Health Button --

def Heal_Button_click():
	'''
	Randomly Heals Player 40-60 Health
	'''
	global Current_Health
	heal=random.randint(40,60)
	Multi_Health_Update(Current_Health+heal)

Heal_Button.on_click=Heal_Button_click

# -- Logic -- Corrosion Button --

def Corrosion_Button_click():
	'''
	Randomly Corrodes Player Defense 1-10 points
	'''
	global Current_Defense
	corrosion=random.randint(1,10)
	Defense_Update(Current_Defense-corrosion)

Corrosion_Button.on_click=Corrosion_Button_click

# -- Starting Updates & Run --
Rebuild_Health_Bars()
Multi_Health_Update(Max_Health)
Defense_Update(Max_Defense)
app.run()

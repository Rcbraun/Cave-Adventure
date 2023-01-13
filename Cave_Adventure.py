#!/usr/bin/env python3

"""Cave Adventure Game | Richard Braun"""

import random ##imports a random number generator
import json
import urllib.request 
import pyinputplus as pinp
import os
from Cave_Adventure_Art import title, death, survive
import time
chkpt_ctr = 0
friends= 0 #counts how many friends you have 
def main():

    title()

    invent = []  #creates an empty list for the variable 'inventory'
    #invent = ['rocks','note','rope', 'flashlight', 'first aid kit'] #testing purposes
    checkpoint = [] #checkpoint creates a checkpoint system that updates along your journey
    # All the availible choices during the adventure
    options = ['Pick a direction and start walking', 'Search the immediate area', 'Pick up some rocks', 'Search the backpack', 'Check out the piece of paper', 'Look around the immediate area',
               'Walk in the only availible direction', 'Try and dig your way through the rock slide','Check your inventory', 'Try to lasso the stalagmite and swing across', 'Jump', #10
               'Stop to talk', "Use the First-Aid Kit to splint the person's ankle", 'Ignore them, and walk passed them without stopping', 'Throw some rocks down onto the wood']
                           # 0                                 # 1                       # 2                     # 3                     # 4                                    # 5     
    inv_opts = ['Do nothing'] 
    def slow(to_print):
        for char in to_print:
            print(char, end='')
            time.sleep(.01)

    def name(): ## The start of the epic adventure
        while True:
            slow('You come awake with a headache, confused as to where you are.\nIt is pitch dark, cool, and damp.\nIt is silent except for your panicked breathing.\nTaking stock of your situation you ask yourself, "Do you remember your name?" (y/n)\n')
            y_n = input().lower()
            
            if y_n == 'y' or y_n == 'yes':  #Allows the user to input a name
                slow('Your name is: ')
                your_name = input().title()  
                break
            elif y_n == 'n' or y_n == 'no': #Allows the user to have a randomly assigned name
                slow('Lets try an easier question.  Are you male or female?\n')
                gender = input().lower()
                if gender == 'male' or gender == 'm':  #Assigns the user a name based on a list of male names
                    male_lib = 'https://raw.githubusercontent.com/aruljohn/popular-baby-names/master/2000/boy_names_2000.json'
                    male_raw = urllib.request.urlopen(male_lib)
                    male = male_raw.read()
                    male_json = json.loads(male.decode("utf-8"))
                    your_name = random.choice(male_json.get('names'))
                    break
                    ##print(name)
                elif gender == 'female' or gender == 'f':  #Assigns the user a name based on a list of female names
                    female_lib = 'https://raw.githubusercontent.com/aruljohn/popular-baby-names/master/2000/girl_names_2000.json'
                    female_raw = urllib.request.urlopen(female_lib)
                    female = female_raw.read()
                    female_json = json.loads(female.decode("utf-8"))
                    your_name = random.choice(female_json.get('names'))
                    break
                    ##print(name)
                else:  #Assigns the user the name Hey
                    slow('Your head is pounding too badly to remember anything.')
                    your_name = ('Hey')
                    break
            else:  #Assigns the user the name Hey
                slow('Your head is pounding too badly to remember anything.')
                your_name = ('Hey')
                break
        return your_name

    user_name = name() 
    #user_name = "" #Testing purposes
    # Creates the variable paper that is used later as a hint
    paper = (f"""{user_name},\n  We were spelunking when a rockslide closed up the way out. You were knocked unconcious. You didn't wake up for 2 days.I was forced to venture further to try and find a way out and get a rescue party together.
If you wake up be careful, the way we came seems really unstable.\nIf you can you should follow me, otherwise I will try and send help.\n  Good Luck""")

    def clear():
        os.system('cls')

    def restart(): #allows a checkpoint restart if yyou die
        while True:
            slow('\nWould you like to retry from the closest checkpoint?(y/n)\n')
            chkpt = input().lower()
            if chkpt == 'y' or chkpt == 'yes':
                break
            else:
                exit()    

    def dark_walk(): #Gives you a 50/50 chance of dying and having to restart at a checkpoint or having to restart completely
        x = random.randint(1,2)
        if x == 1:
            slow("\nYou pick a random direction and start walking.\nYou only take a few steps until you walk head-first into a wall and fall unconcious.\nYou wake up a few moments later in the same situation.\n")
            
        elif x == 2:
            slow("\nYou pick a random direction and start walking.\nYou stumble your way about 20 yards.\n You go to take you next step and you've stepped into a chasm.\nYou spend the rest of your life in a free-fall.\n")
            death()
            restart()

    def wrong_input():  #function for any input other than an acceptable one
        slow("\nYou roll over and vomit.\nYou must still be concussed.\n")

    def rocks():  #happens when picking up rocks is chosen as an option
        if 'rocks' in invent:
            slow('\nYou already have some rocks.\n')
        else:
            invent.append('rocks')
            slow('\nGreat. Now you have some rocks.\n')

    def final_fall():
        slow("You figure you can just jump down and land on the wooded walk way.\nYou've grossly underestimated the drop.\nYou land heavily on the walkway, braking a leg.\nThe walkway gives out and you plummet into the water below.")
        slow('With a broken leg you are unable to swim out of the cave and...')
        death()
        restart()

    def step1():  #You may or may not have remembered your name, but need to get moving regardless
        clear()
        checkpoint.append(step1)
        
        while True:
            # allows the user to input an option for their first choice
            slow(f"""\n\nWhat is your next step?\n""") 
            slow(f'A: {options[0]}\nB: {options[1]}\n')                        
                                #Pick a direction and start walking, or search the immediate area 
            choice = input().upper()
            clear()
            #print(choice)
            if choice == 'A':
                dark_walk()
            elif choice == 'B': #continues the story
                invent.append('paper')
                slow('\nYou feel around your immediate area.')
                break
            else:
                wrong_input()

    def inventory():  # lists out everything in your inventory, updating the inv_opts and lead to inventory_menu()
        if invent == []:
            slow("\nYou currently have nothing in your inventory.")
            checkpoint[chkpt_ctr]()
        else:
            slow(f'\n{invent}\n')
            itemdict= {"rocks": 'Drop Rocks',
                        "paper": 'Read Note',
                        "rope": 'Inspect Rope',
                        "flashlight": 'Inspect Flashlight',
                        "first aid kit": "Inspect First-Aid Kit"}           
            for eachitem in invent:
                if itemdict[eachitem] not in inv_opts:
                    inv_opts.append(itemdict[eachitem])
        inventory_menu()

    def inventory_menu():  #allows the user to further explore their inventory
        while True:#allows the user to inspect items in the inventory, then release the user out to the closest checkpoint
            choice = pinp.inputMenu(inv_opts,'What would you like to do?\n', lettered = True)  
            if choice == 'Drop Rocks':
                invent.remove('rocks')
                inv_opts.remove('Drop Rocks')
                slow('\nYou drop your rocks')
            elif choice == 'Read Note':
                slow(paper)
            elif choice == 'Inspect Rope':
                slow('\nA sturdy length of rope.')
            elif choice == 'Inspect Flashlight':
                slow('\nFlashlight is on and seems to have fresh batteries')
            elif choice == 'Inspect First-Aid Kit':
                slow('\nFirst-Aid Kits is miraculously still full')
            else:
                slow('\nok')
            break

    def step2():  # Still might be blind, but atleast you can feel things
        checkpoint.append(step2)
        global chkpt_ctr
        chkpt_ctr = 1
        while True:
            slow(f"""\nYou feel some rocks, a backpack, and a piece of paper.\nWhat would you like to do?\n\n""")
            slow(f'A: {options[2]}\nB: {options[3]}\nC: {options[4]}\nD: {options[0]}\n')  #Pick up some rocks,Search the backpack, Check out the piece of paper, Pick a direction and start walking,
            choice = input().title()
            clear()
            if choice == 'A':
                rocks() 
            elif choice == 'B':
                invent.append('first aid kit') 
                invent.append('flashlight')
                slow('You find a first aid kit and a flashlight! You turn on the flashlight\n')
                slow('Thank God, some light!')
                break #Continues the story
            elif choice == 'C':
                slow("Believe it or not you can't see if anything is on the paper in the dark.\n")
            elif choice == 'D':
                dark_walk()
            else :
                wrong_input()

    def step3():  # Got a light now what?
        checkpoint.append(step3)
        global chkpt_ctr
        chkpt_ctr =2
        while True:
            slow(f"\nYou've finally got some light.\nNow what?\n")
            slow(f"A: {options[2]}\nB: {options[4]}\nC: {options[5]}\nD: {options[8]}\n")  #2,4,5,8
            choice = input().title()
            clear()
            if choice == 'A':
                rocks()
            elif choice == 'B':
                slow(paper)
            elif choice == 'C': #continues the story
                slow('\nYou look around the area.\n There seems to be some loose rubble in one direction, and the opposite direction continues into the darkness\n')
                break
            elif choice == 'D':
                inventory()
            else:
                wrong_input()

    def step4(): #got a light and you bearings
        checkpoint.append(step4)
        global chkpt_ctr
        chkpt_ctr = 3
        while True:
            slow(f"\nYou've checked your surroundings, and have a working flashlight. Aside from your splitting headache, and being lost underground things are looking great!\n")
            slow(f"A: {options[2]}\nB: {options[7]}\nC: {options[6]}\nD: {options[8]}\n")
            choice = input().title()
            clear()
            if choice == 'A':
                rocks()
            elif choice == 'B': #ends the story either in success or death
                x = random.randint(1,10)
                if x == 7:
                    slow("\n\nYou start to dig, and shift the rubble, you're making progress, but the way is closing up behind you...\nAfter what seems like forever you finally see light.")
                    slow("\nOne of your friends grabs you hand and pulls you the rest of the way free.\n  You've Survived!")
                    slow("\nYour friend asks what happened to your companion, You tell them that you have no idea...")
                    survive()
                    exit()
                else:
                    slow("\nYou start digging. Despite the rumbling and ominous shifting of rock, you continue digging.")
                    slow("\nLast thing you see is a basketball sized boulder coming straight for your head...")
                    death()
                    restart()
            elif choice == 'C': #continues the story
                slow ("""\nYou walk down the tunnel, around a bend, and come to a chasm. Your flashlight doesn't even reach the bottom.\nLooks like the tunnel continues on the otherside of the chasm and the gap is only 25'.
Luckily there is a rope on the ground that seems to be the perfect length.  Even more luckily there are stelagmites on the otherside you might be able to lasso,\nand they appear to barely be able to support your weight.""")
                invent.append('rope')
                break
            elif choice == 'D':
                inventory()
            else:
                wrong_input()
                
    def step5():#the great chasm crossing
        checkpoint.append(step5)
        global chkpt_ctr
        chkpt_ctr = 4
        while True:
            slow('\nHow do you proceed?')
            slow(f"\nA: {options[2]}\nB: {options[10]}\nC: {options[9]}\nD: {options[8]}\n")
            choice = input().title()
            clear()
            if choice == 'A':
                rocks()
            elif choice == 'B': #leads to a restart
                slow("\nDespite carrying a backpack full of gear you think you can make a borderline world record leap...\n\nYou can't.")
                slow('\nYou spent the rest of your short life regretting your over confidence.')
                death()
                restart()
            elif choice == 'C':# 50/50 that this will lead to the next step
                if 'rocks' in invent:
                    slow("\nYou make a miraculous toss. \nThe rope lassos the stelagmite perfectly.\nAs soon as you drop into the void to swing across, you hear a loud crack as the stelagmite snaps.")
                    slow("\nYou spend the fall thinking about the fact that the stelagmite would have held if you didn't have the extra weight of rocks in your backpack.")
                    restart()
                else:
                    x = random.randint(1,2)
                    if x == 1:
                        slow("\nYour lasso falls just short of the stelagmite.\nUnlucky, maybe you'll get it if you keep trying.")
                    else:
                        slow("\nYou make a miraculous toss. \nThe rope lassos the stelagmite perfectly.\nYou drop into the void to swing across, you hear a loud snap as the rope breaks...\n")
                        slow("\n\nYou're falling...\nBut only a foot as you land heavily on the other side.\nYou continue down the tunnel. You begin to hear some quiet sobbing.")
                        slow("\nYou come across a person whos ankle is at a weird angle.\n They call out for help.\n")
                        invent.remove('rope')
                        break
            elif choice == 'D':
                inventory()
            else:
                wrong_input()

    def step6():# you've crossed the chasm and are continueing down the path to a person
        checkpoint.append(step6)
        global chkpt_ctr
        chkpt_ctr = 5
        progress = ("""You round another bend, and come to a large hole.\nThis time you can see a pin prick of light shining up from below.
When you look down you can see what looks like an old wooden walkway.\nIt sounds like there is water below the too.""")
        while True:
            slow('\nNow what?\n')
            slow(f'A:{options[2]}\nB: {options[11]}\nC: {options[12]}\nD: {options[13]}\nE: {options[8]}\n')
            choice = input().title()
            clear()
            if choice == 'A':
                rocks()
            elif choice == 'B':
                slow(f'\nYou stop.\nBefore you can even say anything the person says,\n"{user_name}! Thank goodness you woke up.\nPlease help me! I tripped on a rock and broke my ankle."\n')
            elif choice == 'C':
                slow("\nYou pull out the First-Aid kit, and fashion a splint for this person's ankle.\nThey thank you profusely and they hobble along next to you down the tunnel.")
                slow(progress)
                global friends
                friends = 1
                break
            elif choice == 'D':
                slow(f'\nYou figure that this must be the person that abandoned you earlier, kharma finds a way.\nYou continue down the passage, all the while ignoring the persons pleading, "{user_name} come back!"')
                slow(progress)
                break
            elif choice == 'E':
                inventory()
            else:
                wrong_input()
    
    def step7(): #Almost there!!
        checkpoint.append(step7)
        global chkpt_ctr
        chkpt_ctr = 6
        global friends
        while True:
            if friends == 1:  #provides a hint if you saved the person
                slow("\nYour companion mentions that dropping some rocks down the hole could possible clear a path.\nHow do you proceed?")
            else:
                slow("\nHow do you proceed?")
            if 'rocks' in invent:
                slow(f"\nA: {options[2]}\nB: {options[14]}\nC: {options[10]}\nD: {options[8]}\n")
                choice = input().title()
                clear()
                if choice == 'A':
                    rocks()
                elif choice == 'B': #continues the story
                    slow("You drop some rocks onto the down the hole. \nAfter a loud crash the wood is cleared away and you see an ocean cave half filled with water with a way out!\n")
                    slow("The water seems deep enough to drop into.")
                    break
                elif choice == 'C':
                    final_fall()
                elif choice == 'D':
                    inventory()
                else:
                    wrong_input()
            else:
                slow(f"\nA: {options[2]}\nB: {options[10]}\nC: {options[8]}\n") #doesnt provide the option to continue the story unless there are rocks in your inventory
                choice = input().title()
                clear()
                if choice == 'A':
                    rocks()
                elif choice == 'B':
                    final_fall()
                elif choice == 'C':
                    inventory()
                else:
                    wrong_input()
    def step8(): #Ending!!
        global friends
        while True:
            if friends == 1:
                slow("\nBoth you and your companion leap for freedom at the same time.\n You manage to help each other to swim out of the cave and make to to a beach a short distance away.\n")
                slow("You are greeted by a rescue team.\nYou promptly throw up and are treated for your concussion.\n")
                survive()
                exit()
            else:
                slow("\nYou leap for freedom.\nYou somehow manage to swim out of the cave and make it to a beach a short distance away.\n")
                slow("You are greeted by a resuce team.\nYou promptly throw up and are treated for a concussion.\n")
                slow("One of members of the recue team ask you where your companion is.\n")
                choice = input("Do you lie or tell them where the person is?(Truth/Lie)\n")
                choice = choice.lower()
                clear()
                if choice == 'truth':
                    slow("\nYou tell them that you left them in the cave and explain how to reach them.\n")
                    slow("They are ultimately rescued but refuse to speak to you ever again because you ignored them when they needed you.\nBut...\n")
                    survive()
                    exit()
                elif choice == 'lie':
                    slow("\nYou tell the rescue team that you woke up alone and never saw them.\n You further explain that because of your concussion you can't remember how you made it to the beach.\n")
                    slow("Ultimately they never find your former friend.\nBut... Atleast\n")
                    survive()
                    exit()
                else:
                    wrong_input()
        
            




    step1()
    step2()
    step3()
    step4()
    step5()
    step6()
    step7()
    step8()


    #inventory()
            
#if __name__ == "main":
    #main()
main()



"""invent= ["rope","gun","compass", "rocks"]
ugh= {"Do Nothing": {"func": print,
                     "arg": invent},
      "Drop Rocks": {"func": invent.remove,
                     "arg": "rocks"},
      "Read Note":  {"func": print,
                     "arg": "I'm a note!"}
      }
choice= input(">").title()
ugh[choice]["func"](ugh[choice]["arg"])
print(invent)"""


"""invent= ["paper", "rope"]
inv_opts= []
itemdict= {"rocks": 'Drop Rocks',
           "paper": 'Read Note',
           "rope": 'Inspect Rope',
           "flashlight": 'Inspect Flashlight'}
                           
for eachitem in invent:
    if itemdict[eachitem] not in inv_opts:
        inv_opts.append(itemdict[eachitem])
        
print(inv_opts)"""
# -*- coding: utf-8 -*-

import pickle
import string
import time
import random
import re
import operator
import howlong
import marduino

# regexp's
one_dice_re = re.compile('!d\d{1,3}')
many_dice_re = re.compile('!\d{0,2}d\d{1,3}')
hero_dice_re = re.compile('!\d{1,6}h')
rick_dice_re = re.compile('!\drick')
birfday_re = re.compile('!birfday \d{1,3} \d{2}[.]\d{1}')
howlong_re = re.compile('!howlong \d{2}[/]\d{2}[/]\d{4}')

# Hellos
bonjour = ["O Hai ___.",
"Yay! It's ___. ^_^"
]
        
# marduino triggers
triggers = ["on", "off", "up", "down",
            "1", "2", "scroll", "clear", "light", "dark", "test", "conn"]

# Users to ignore (usually bots)
ignore_usr = []
ignore_chnl = []

# Highlight trigger words
hilights = ["your_nick"]

# Help dialogue
help_string = ["Commands accepted are:"]


def msgtype(user, channel, msg, arg):
    if arg == "c":
        #directed at channel
        print("Channel message is: %s\n" % msg)
        flag = "c"      # default flag
        if user in ignore_usr:          # Pay no attention to some nicks.
            return user, channel, None, flag
        if one_dice_re.match(msg):
            msg = diceroller(user, msg, 0)
            return user, channel, msg, flag
        elif many_dice_re.match(msg):
            msg = diceroller(user, msg, 1)
            return user, channel, msg, flag
        elif rick_dice_re.match(msg):
            msg = ["Never gonna give you up, never gonna let you down, never gonna turn around and desert you..."]
            return user, channel, msg, flag
        elif howlong_re.match(msg):
            msg = msg.split(" ", 1)[1]
            day,month,year = msg.split("/", 2)
            input_date = [day,month,year]
            msg = how_long(input_date)
            return user, channel, msg, flag
        else:
            print(msg)
            return user, channel, None, flag
        return user, channel, None, flag
    
    elif arg == "m":
        #Actions
        flag = "c"      # default flag
        print("Action message is: %s\n" % msg)
        if msg == "hello":
            msg = ["Hello, %s" % user]
            return user, channel, msg, flag
        elif msg == "help":
            flag = 'u'
            msg = help_string
            return user, channel, msg, flag
        else:
            return user, channel, None, flag
    
    elif arg == "p":
        #private message
        flag = "u"
        print("Private message is: %s\n" % msg)
        for trig in triggers:
            if re.match(trig, msg):
                print("arduino trigger matched.")
                msg = marduino.output(msg, user)
                #print(channel, user, msg)
                flag = "u"
                return user, channel, msg, flag
    else:
        return user, channel, None, flag


"""---------------------------
CHANNEL RELATED FUNCTIONS
---------------------------"""
def userjoin(user, channel):
    """Greet users logging in to the channel"""
    if channel in ignore_chnl:      # Don't message in some channels.
        return None
    chance = random.randint(0, 100)
    print("RANDOM INT: %d" % (chance))
    if chance < 90:
        return None
    else:
        msg = random.choice(bonjour).replace("___", user).replace("---", 
              channel)
        return msg

def diceroller(user, msg, dcount):
    if dcount == 0: # one dice
        d2 = msg.split('d', 1)[1]
        d2 = int(d2)
        if d2 > 0 and d2 < 101:
            an_nos = [8,11,18,80,81,82,83,84,85,86,87,88,89]
            chance = random.randint(1,d2)
            if chance in an_nos:
                a_an = "an"
            else:
                a_an = "a"
            msg =  [("%s rolls %s %d" % (user, a_an, chance))]
        else:
            msg = ["How big are the dice where you come from?! o_0"]
    
    else: # more than one dice
        d1, d2 = msg.split('d', 1)
        d1 = int(d1[1:len(d1)]) # ignore leading !
        d2 = int(d2)
        if (d1 > 0 and d1 < 101) and (d2 > 0 and d2 < 101):
            msg = ["more than one dice: %d - %d" % (d1, d2)]
            rolled_n = []
            rolled_s = []
            for ii in range(0,d1):
                chance = random.randint(1,d2)
                rolled_n.append(chance)
                rolled_s.append(str(chance))
            roll_tot = sum(rolled_n)
            out_str = ", ".join(rolled_s)
            msg = [user + " rolls: " + out_str + "  Total: " + str(roll_tot)]
        else:
            msg = ["How big are the dice where you come from?! o_0"]
        
    return msg

def how_long(input_date):
    weeks,days,hours,mins,secs,blah = howlong.howlong(input_date)
    out = ["There are only %d weeks, %d days, %d hours, %d minutes and %d %s" 
           % (weeks,days,hours,mins,secs,blah)]
    return out

"""---------------------------
PM RELATED FUNCTIONS
---------------------------"""

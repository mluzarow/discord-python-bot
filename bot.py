# Python 3.6

import discord
from discord.ext import commands
import asyncio
from urllib.request import urlopen
import urllib.parse
import http.client
import os
import logging

def loadConfig ():
    t = list ()

    with open ("config.cfg", 'r') as f:
        t = f.read ().split ("\n")
    f.closed
    
    return (t)
    
# ================================
# == Core super important stuff ==
# ================================
client = commands.Bot ('!', None)

@client.event
async def on_ready ():
    print ('Logged in as')
    print (client.user.name)
    print (client.user.id)
    print ('---------------')

@client.event
async def on_message (msg):
    await client.process_commands (msg)

    
# ================================
# ==         Commands           ==
# ================================
@client.command ()
async def test ():
    print ("Bot command triggered: !test\n-----------------------")
    
    await client.say ("I am listening.")

@client.command ()
async def commands ():
    print ("Bot command triggered: !commands\n-----------------------")
    HELP_TEXT = "```\n" \
                "** Keybot Commands **\n" \
                "-----------------------\n" \
                "* !commands         : Shows this help message.\n" \
                "* !test             : Prints a test message.\n" \
                "* !wolfram [query]  : Returns a gif solution from Wolfram Alpha using [query] as the query.\n" \
                "* !google [query]   : Returns the first link from Google using [query] as the query.\n" \
                "* !roll [rollable]  : Returns the result of the rolled rollable.\n" \
                "    * die   : Rolls a single six-sided die.\n" \
                "    * ndm   : Rolls an m-sided die n times with n > 0 and m > 0.\n" \
                "    * n-m   : Rolls for a value between n and m with n > 0, m > 0, and m >= n.\n" \
                "* !choose [list]    : Chooses a phrase from a comma (,) separated list, [list].\n" \
                "* !animequote       : Displays a random anime quote.\n" \
                "```"

    await client.say (HELP_TEXT)

@client.command ()
async def animequote ():
    print ("Bot command triggered: !animequote\n-----------------------")
    import animequotes
    from random import randint

    quote_dict = animequotes.makeQuotes ()
    
    q = quote_dict [randint (0, len (quote_dict) - 1)]

    s = "%s\n%s %s" % (q ['quotesentence'], q ['quotecharacter'], q ['quoteanime'])
    
    await client.say (s)

@client.command (pass_context=True)
async def choose (msg):
    from random import choice

    msg = msg.message
    s = msg.content

    print ("Bot command triggered: %s\n-----------------------" % s)
    
    s = s [7::].split (',')
    
    await client.say ("I've chosen: %s" % choice (s).strip ())

@client.command (pass_context=True)
async def roll (msg):
    from random import randint

    msg = msg.message
    s = msg.content

    print ("Bot command triggered: %s\n-----------------------" % s)

    s = s.split ()
    if (len (s [1::]) < 1):
        return

    if (s [1] == "die"):
        await client.say ("The die landed on: %d" % randint (1, 6))
    else:
        n = s [1].split ('-')

        try:
            # Must be roll range
            if (len (n) == 2):
                await client.say ("You have rolled a: %d" % randint (int (n [0]), int (n[1])))
            # Must be ndm
            else:
                n = s [1].split ('d')
                rolls = list ()
                
                for i in range (int (n [0])):
                    rolls.append (randint (1, int (n [1])))
                
                await client.say ("You have rolled the following: %s\nYour total is: %d" % (" ".join ([str(r) for r in rolls]), sum (rolls)))
                    
        except:
            return

@client.command (pass_context=True)
async def google (msg):
    from google import search

    msg = msg.message
    s = msg.content

    await client.send_typing (msg.channel)
    
    print ("Bot command triggered: %s\n-----------------------" % s)
    
    s = s.split ()
    s = " ".join (s [1::])

    # I don't understand why search () is ignoring all the arguments
    t = '' 
    for url in search (s, start=0, stop=1):
        t = url
        break

    await client.say (t)

@client.command (pass_context=True)
async def wolfram (msg):
    msg = msg.message
    s = msg.content

    await client.send_typing (msg.channel)

    print ("Bot command triggered: %s\n-----------------------" % s)
    
    s = s.split ()
    s = " ".join (s [1::])

    URLencodeRule = {'i' : s}
    URLencodeStr = urllib.parse.urlencode (URLencodeRule)
    
    path = "https://api.wolframalpha.com/v1/simple?%s&appid=%s" % (URLencodeStr, WOLFRAM_ID)

    try:
        # Follow URL
        response = urlopen(path)
        # Get data
        j = response.read()
        # Save as gif
        with open ('file.gif', 'wb') as f:
            f.write (j)
            # Keep this print line in here; it delays the script enough to
            # fully write the image before upload
            print ("File written to disc.")
        f.closed

        await client.send_file (msg.channel, 'file.gif')
    except Exception:
        from traceback import format_exec
        logging.warning ('Generic exception: ' + format_exc ())

# Bot initialize
if (__name__ == "__main__"):
    print ('Bot script is running.')
    print ('----------------------')
    
    t = loadConfig ()
    
    EMAIL = t [0]
    PASSWORD = t [1]
    BOT_ID = t [2]
    OWNER_ID = t [3]
    GOOGLE_API_KEY = t [4]
    SOUNDCLOUD_ID = t [5]
    WOLFRAM_ID = t [6]

    client.run (EMAIL, PASSWORD)

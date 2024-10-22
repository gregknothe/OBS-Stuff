import obspython as obs
import os
from twitchio.ext import commands, eventsub
from twitchio.client import Client
import pandas as pd
import random as rand
import sys
import time 
import threading
import datetime

#----------------------Useful Documentation----------------------#
#OBS doc: https://docs.obsproject.com/
#OBS Cheatsheet: https://github.com/upgradeQ/OBS-Studio-Python-Scripting-Cheatsheet-obspython-Examples-of-API/blob/master/README.md
#Twitchio doc: https://twitchio.dev/en/stable/
#Twitchio Youtube Tutorial: https://www.youtube.com/watch?v=w8HRE-NNfnk


#----------------------------"Settings"------------------------#
#Durration: # of sec the visual stays on screen, Cooldown: # of sec the cooldown of !hey is set to (must be greater than durration)
#ModList: list of people who can use the !hr command (and other commands down the line)
durration = 5   
cooldown = 6    
currCooldown = 0
modList = ["lastclaire", "greedx___", "asome26", "nastyplot", "botthewoz", "frendweeb", "gdom", "redditto", "sajam", "wooper_enthusiast",
           "joshgrilli", "sindercenpai", "hotashi", "linkl0nk", "chris_re5", "voidashe", "the_doc_", "abusywitch", "lament_03", "kyluneena",
           "jackpotfm", "nastyplot", "nbnhmr", "ailubee", "meowzykat", "squirrel147"]    

#Just some global variables used throughout the program.
heyList = []
hotkey_id = obs.OBS_INVALID_HOTKEY_ID
gameList = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/rankFinalGameList.csv", sep="|")
ranceGameList = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/ranceGameList.csv", sep = "|")
monuGameList = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/monuminGames.csv", sep="|") # Altered Lines: 33, 48, 53-54, 112-116###########################

silverFile = "C:/Users/codyb/OneDrive/Documents/pythonScripts/gachaClaire/silverClaireAnimated.gif"
goldFile = "C:/Users/codyb/OneDrive/Documents/pythonScripts/gachaClaire/goldClaireAnimated.gif"
rainbowFile = "C:/Users/codyb/OneDrive/Documents/pythonScripts/gachaClaire/rainbowClaireAnimated.gif"
ranceFile = "C:/Users/codyb/OneDrive/Documents/pythonScripts/gachaClaire/ranceClaireAnimated.gif"


#Supresses error outputs (happens when someone types something other than !hey, so they kinda needa go tbh)
class DevNull:
    def write(self, msg):
        pass
sys.stderr = DevNull()

#----------------------Python Code Section---------------------#
#Just taking the game data from the dataframe and formatting it into something usable. 
def hey(rance=False, monu=False):
    global gameList
    global ranceGameList
    if rance == True:
        localGameList = ranceGameList
    elif monu == True:
        localGameList = monuGameList
    else:
        localGameList = gameList
    x = rand.randint(0,len(localGameList["name"]))
    gameTitle, gameYear, gamePlat, gameImg, gameRarity= localGameList["name"][x], localGameList["year2"][x], localGameList["platform"][x], localGameList["img"][x], localGameList["rarity"][x]
    if len(gamePlat) > 25:
        gamePlat = gamePlat[:25] + "..." 
    if gameYear == "None":
        gameYear = "NA"

    gameRare = ""
    if gameRarity == "silver":
        gameRare = "R"
    elif gameRarity == "gold":
        gameRare = "SR"
    elif gameRarity == "rainbow":
        gameRare = "UR" 
    else: 
        gameRare = "RANCE"

    gameInfo = "([" + gameRare + "] " + gamePlat + " " + str(int(gameYear)) + ")"
    return gameTitle, gameInfo, gameImg, gameRarity

def heyString(userName, gameTitle, gameInfo, rance=False):
    if rance == True:
        return "Hey alright, it's my favorite " + gameTitle + " " + gameInfo + " streamer. @" + userName
    return "Oh hey, it's my favorite " + gameTitle + " " + gameInfo + " streamer. @" + userName

def cooldownReset():
    global currCooldown 
    currCooldown = 0
    print(f"curr Cooldown: " + str(currCooldown))
    return

def cooldownStart():
    global currCooldown
    currCooldown = 1
    return
#---------------------Twitch Chat Bot Section---------------------#
#Sets up the bot with all the info it needs
bot = commands.Bot(
    token='oauth:0nyov8e54o2d1ezitbcnvcbznrafcy',
    client_id=['hq2jby4wfk8p1rd2igt88y0wm0160i'],
    nick=['botthewoz'],
    prefix=['!'],
    initial_channels=["lastclaire"]
)

#Setup for the chat command cooldown, prevents visual overlap and potential bugs.
@commands.cooldown(rate=1, per=cooldown, bucket=commands.Bucket.channel)

#Bot commands, pretty shrimple.
@bot.command(name="hey")
async def ohHey(ctx):
    print(f"Hey was activated.")
    global currCooldown
    if ctx.author.name not in heyList and currCooldown == 0:
        print(f"Valid Hey was triggered")
        cooldownStart()
        if ctx.author.name == "life_jam":
            game = hey(rance=True)
            await ctx.send(heyString(ctx.author.name, game[0], game[1], True))
            heyList.append(ctx.author.name)
            display_game(game[0], game[2], ctx.author.name, game[3])
        elif ctx.author.name == "monuminn":
            game = hey(monu=True)
            await ctx.send(heyString(ctx.author.name, game[0], game[1], True))
            heyList.append(ctx.author.name)
            display_game(game[0], game[2], ctx.author.name, game[3])
        else:
            game = hey()
            await ctx.send(heyString(ctx.author.name, game[0], game[1]))
            heyList.append(ctx.author.name)
            display_game(game[0], game[2], ctx.author.name, game[3])
            print(f"Valid Hey was displayed for" + ctx.author.name + " " + str(datetime.datetime.now()))
        print(f"curr cooldown: " + str(currCooldown))
        threading.Timer(cooldown, cooldownReset).start()
        sys.sleep(6)
    elif ctx.author.name in heyList:
        await ctx.send("You already used your daily !hey. @" + str(ctx.author.name))
    else:
        await ctx.send("!hey is currently on cooldown. @" + str(ctx.author.name))
        print(f"curr cooldown: " + str(currCooldown))
    return

#Removes the requested twitch chatter from the heyList, allowing them to "go again".
@bot.command(name="hr")
async def heyListRemove(ctx, *, text):
    print(f"!hr was activated")
    if ctx.author.name in modList:
        try:
            heyList.remove(text.lower())    
            await ctx.send("You has been given another daily !hey. @" + str(text.lower()))
        except:
            await ctx.send("Something went wrong, you probably misspelt their name.")

#Turns off the bot, but it kinda doesnt really tho, not sure how OBS and the bot interact in this case.
@bot.command(name="goodbye")
async def test(ctx):
    if ctx.author.name in modList:
        await ctx.send("Goodbye :)")
        sys.exit()

@bot.command(name="reset")
async def reset(ctx):
    if ctx.author.name not in heyList:
        global currCooldown
        currCooldown = 0
    return

@bot.event()
async def event_eventsub_notification_channel_reward_redeem(payload: eventsub.CustomRewardRedemptionAddUpdateData) -> None:
    channel = bot.get_channel('channel')
    await channel.send("woah, thats crazy.")
    print(f"user: " + payload.data.user.name)
    print(f"redeemID: " + payload.data.reward.id)
    return

#Bot Startup.
if __name__ == "__main__":
    bot.run()


#------------------------OBS Script Section-------------------------#
#The obs script part that does the thing.
def display_game(gameTitle, gameImg, userName, gameRarity):

    #Fetching game info from hey().
    settings = obs.obs_data_create()
    scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())

    #Updating the gacha.
    raritySource = obs.obs_get_source_by_name("gachaRarity")
    if gameRarity == "silver":
        obs.obs_data_set_string(settings, "file", silverFile)
    elif gameRarity == "gold":
        obs.obs_data_set_string(settings, "file", goldFile)
    elif gameRarity == "rainbow":
        obs.obs_data_set_string(settings, "file", rainbowFile)
    else:
        obs.obs_data_set_string(settings, "file", ranceFile)
    
    obs.obs_source_update(raritySource, settings)
    
    #Updating the Title.
    titleSource = obs.obs_get_source_by_name("titleText")
    obs.obs_data_set_string(settings, "text", gameTitle)
    obs.obs_source_update(titleSource, settings)

    #Updating the Game Image.
    imgSource = obs.obs_get_source_by_name("gameImage")
    obs.obs_data_set_string(settings, "url", gameImg)
    obs.obs_source_update(imgSource, settings)

    #Updating the User Name.
    userSource = obs.obs_get_source_by_name("usernameText")
    obs.obs_data_set_string(settings, "text", userName)
    obs.obs_source_update(userSource, settings)
    
    #Hopefully plays the shenmue sound
    pullSource = obs.obs_get_source_by_name("pullSound")
    obs.obs_source_media_play_pause(pullSource, True)
    
    #Toggling the visibility of the group with a wait statement inbetween.
    groupSource = obs.obs_get_source_by_name("ohHeyGroup")
    group = obs.obs_scene_sceneitem_from_source(scene, groupSource)
    obs.obs_sceneitem_set_visible(group, True)
    
    def hide_group():
        obs.obs_sceneitem_set_visible(group, False)

        #Releasing the sources.
        obs.obs_data_release(settings)
        obs.obs_source_release(raritySource)
        obs.obs_source_release(titleSource)
        obs.obs_source_release(imgSource)
        obs.obs_source_release(userSource)
        obs.obs_source_release(groupSource)
        obs.obs_source_release(pullSource)
        obs.obs_scene_release(scene)

    threading.Timer(durration, hide_group).start()

#Description of the script in the script menu, crazy.
def script_description():
    return "Active the bot via the 'Twitch Chat Bot Start' hotkey. \n \nUse chat command !goodbye to turn off the bot before exiting OBS (closing it by closing OBS should be fine, but better safe than sorry tbh)"

#Saves the hotkey since OBS is lame and doesnt do that by default for some reason.
def script_save(settings):
    global hotkey_id
    hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
    obs.obs_data_set_array(settings, "Twitch Chat Bot Start", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

#More hotkey stuff, automatically runs when the script is started.
def script_load(settings):
    global hotkey_id
    def callback(pressed):
        if pressed:
            return bot.run()
    hotkey_id = obs.obs_hotkey_register_frontend("htk_hotkey2", "Twitch Chat Bot Start", callback)
    hotkey_save_array = obs.obs_data_get_array(settings, "Twitch Chat Bot Start")
    obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

#Some stuff that might or might not be needed, but I'm to lazy to find out, thus it is left here in a neutered state.
def script_update(settings):
    dog = "dog"
    return

def script_properties():
    cat = "cat"
    return


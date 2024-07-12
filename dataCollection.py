import pandas as pd
import random as rand
import os
import time

#New idea for formating: 
#Since this site seemingly assigns each game a unique id, the random num gen can just be set to a range within set years instead of pulling from an actual dataframe
    #ex. RanNum(1000-80000) -> x, add x to a list, so when it is generated down the line it will skip it 
#To do: 
    #Find unique id numbering method. If its just by date of release that would be fucking amazing, but its probably not. 
        #It does not work by release date, unlucky. Still try to figure it out at some point.
    #Try to compile a list of games for each platform, prob using the "games" call.
    #Have a list of games (or id range) and a efficent function to pull the picture URL for the next step (the hardest step prob)
    #Figure out how to run python on OBS and how to intigrate that into twitch chat so it all works through OBS or Nightbot in particular? 

key = "xxxxxx"
alan = "84428"
gameID = "23412"

def gameLookup(gameID):
    #Takes the game id and returns: "game title", "release year", "platforms", and "boxart url"
    df = pd.read_json("https://www.giantbomb.com/api/game/3030-" + str(gameID) + "/?api_key=" + key + "&format=json&field_list=name,image,platforms,original_release_date")
    #print(df.loc["image","results"])
    gameTitle = df.loc["name","results"]
    imgURL = df.loc["image","results"].get("original_url")
    releaseYear = str(df.loc["original_release_date","results"]).split("-")[0]
    #print(df.loc["platforms","results"])
    platformList = []
    for x in range(len(df.loc["platforms","results"])):
        platformList.append(df.loc["platforms", "results"][x].get("abbreviation"))
    return gameTitle, releaseYear, ", ".join(platformList), imgURL

#gameLookup(gameID)

gamecube = "23"

def consoleGames(consoleID, offset=0):
    json = pd.read_json("https://www.giantbomb.com/api/games/?api_key=" + key + "&format=json&field_list=name,id,image,platforms,expected_release_year,original_release_date&filter=platforms:" + str(consoleID) + "&offset=" + str(offset))
    data = json["results"]
    nameList, idList, imageList, yearList, yearList2, platformList = [], [], [], [], [], []
    for x in range(len(data)):
        nameList.append(data[x].get("name"))
        idList.append(data[x].get("id"))
        yearList.append(data[x].get("expected_release_year"))
        yearList2.append(str(data[x].get("original_release_date")).split("-")[0])
        imageList.append(data[x].get("image").get("original_url"))
        allPlatforms = []
        for y in range(len(data[x].get("platforms"))):
            allPlatforms.append(data[x].get("platforms")[y].get("abbreviation"))
        platformList.append(", ".join(allPlatforms))
    df = pd.DataFrame({"name": nameList, "id": idList, "year": yearList, "year2": yearList2, "platform": platformList, "img": imageList})
    return df

def consoleGamesFullList(consoleID):
    offset = 100
    loopCount = 2
    df = consoleGames(consoleID, 0)
    print("Page #1 done.")
    currDF = consoleGames(consoleID, offset)
    print("Page #2 done.")
    while len(currDF["name"]) == 100:
        df = pd.concat([df, currDF])
        offset = offset + 100
        currDF = consoleGames(consoleID, offset)
        print("Page #" + str((offset+100)/100) + " done.")
        loopCount += 1
        if loopCount == 25:
            time.sleep(60)
            loopCount = 0
    df = pd.concat([df, currDF])
    df.reset_index(drop=True).to_csv("gameList/" + str(consoleID) + ".csv")
    return

def updateAllList():
    consoleIDList = [202, 144, 36, 35, 20, 82, 176, 179, 157, 159, 156, 155, 145, 146, 154, 139, 129, 117, 185, 192, 18, 52, 89, 34, 32, 134, 84,
                    72, 23, 4, 54, 19, 186, 81, 65, 37, 57, 80, 43, 79, 31, 22, 42, 59, 28, 29, 142, 158, 9, 5, 25, 7, 3, 6, 70, 8, 91, 21, 51,
                    70, 50, 87, 101, 104, 78, 77, 102, 171, 98, 103, 127, 118, 26, 39, 27, 119, 108, 148, 1, 201, 76, 67, 14, 40]
    for x in consoleIDList:
        consoleGamesFullList(x)
        print("-----------------ConsoleID: " + str(x) + " complete.")
    return

def finalList():
    listList = os.listdir("gameList")
    df = pd.read_csv("gameList/"+listList[0])
    listList.pop(0)
    print("added " + listList[0])
    for x in listList:
        df2 = pd.read_csv("gameList/"+x)
        df = pd.concat([df, df2])
        print("added " + x)
    df = df.drop_duplicates("id", keep="first")
    df.reset_index(drop=True).drop(["Unnamed: 0"], axis=1).to_csv("finalGameList.csv", sep = "|")
    return 

def ranceList():
    ranceIDList = [67729, 78766, 48464, 78765, 78764, 35053, 78763, 39173, 10034, 714, 7404, 41482, 78767]
    gameInfo = gameLookup(ranceIDList[0])
    nameList, imageList, yearList, platformList = [gameInfo[0]], [gameInfo[3]], [gameInfo[1]], [gameInfo[2]]
    ranceIDList.pop(0)
    for x in ranceIDList:
        newGame = gameLookup(x)
        nameList.append(newGame[0])
        imageList.append(newGame[3])
        yearList.append(newGame[1])
        platformList.append(newGame[2])
    df = pd.DataFrame({"name": nameList, "year2": yearList, "platform": platformList, "img": imageList})
    df.reset_index(drop=True).to_csv("ranceGameList.csv", sep = "|")
    return

#ranceList()
#finalList()

#df = pd.read_csv("testGameList.csv")
#print(df["name"][0])

#gameList = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/finalGameList.csv", sep="|")

#print(gameList[gameList["name"]=="Rance 4.2: Angel Army"])


def consoleInfo():
    #consoleIDList = [202, 144, 36, 35, 20]
    consoleIDList = [202, 144, 36, 35, 20, 82, 176, 179, 157, 159, 156, 155, 145, 146, 154, 139, 129, 117, 185, 192, 18, 52, 89, 34, 32, 134, 84,
                    72, 23, 4, 54, 19, 186, 81, 65, 37, 57, 80, 43, 79, 31, 22, 42, 59, 28, 29, 142, 158, 9, 5, 25, 7, 3, 6, 70, 8, 91, 21, 51,
                    70, 87, 101, 104, 78, 77, 102, 171, 98, 103, 127, 118, 26, 39, 27, 119, 108, 148, 1, 201, 76, 67, 14, 40]
    abrList = []
    consolePageList = []
    for x in consoleIDList:
        json = pd.read_json("https://www.giantbomb.com/api/platform/3045-"+ str(x) +"/?api_key="+ str(key) + "&format=json&field_list=abbreviation,deck")
        abrList.append(json["results"].get("abbreviation"))
        consolePageList.append("https://www.giantbomb.com/playdate/3045-"+str(x)+"/")
    df = pd.DataFrame({"abbreviation": abrList, "consoleID": consoleIDList, "consoleURL": consolePageList})
    df.to_csv("consoleInfo.csv")
    return

def applyRarity():
    df = pd.read_csv("finalGameList.csv", sep="|")
    consoleInfo = pd.read_csv("consoleListFinal.csv")
    gameCount = []
    for x in range(len(df["name"])):
        consoleString = df["platform"][x]
        consoleList = consoleString.split(", ")
        consoleValues = []
        for y in consoleList:
            #consoleValues.append(consoleInfo["gameCount"][consoleInfo["abbreviation"]==y])
            try:
                consoleValues.append(consoleInfo.loc[consoleInfo["abbreviation"]==y, "gameCount"].iloc[0])
            except: 
                consoleValues.append(1000)
        gameCount.append(max(consoleValues))
    df["gameCount"] = gameCount
    df.to_csv("realFinalGameList.csv", sep="|")
    return 

#print(applyRarity())

#consoleInfo = pd.read_csv("consoleListFinal.csv")

#print(consoleInfo["gameCount"][consoleInfo["abbreviation"]=="PS5"].index)
#print(consoleInfo.loc[consoleInfo["abbreviation"]=="PS5", "gameCount"].iloc[0])

def countDisplay():
    df = pd.read_csv("rankFinalGameList.csv", sep="|")
    df["rarity"].value_counts().to_csv("countDisplay.csv")
    return



def addCount():
    df = pd.read_csv("realFinalGameList.csv", sep="|")
    rankList = []
    for x in range(len(df["name"])):
        if df["gameCount"][x] >= 1000:
            rankList.append("silver")
        elif df["gameCount"][x] <= 1000 and df["gameCount"][x] > 100:
            rankList.append("gold")     
        else:
            rankList.append("rainbow") 
    df["rarity"] = rankList
    df.to_csv("rankFinalGameList.csv", sep="|")
    return

#countDisplay()
#addCount()

def monuminTable():
    df = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/rankFinalGameList.csv", sep="|").reset_index(drop=True)
    #print(df)
    titleList = ["Blue's Clues", "Rugrats", "Dora the Explorer", "Teletubbies", "My Little Pony", 
                 "Go Diego Go", "CoComelon", "Little Einsteins", "Backyardigans", "Paw Patrol", "Bob the Builder",
                 "PJ Masks", "Marvel vs. Capcom 3", "Street Fighter III: 3rd Strike"]
    
    gameDF = df.loc[df["name"].str.contains("Sesame Street")].reset_index(drop=True)
    for title in titleList:
        games = df.loc[df["name"].str.contains(title)].reset_index(drop=True)
        #print(games)
        gameDF = pd.concat([gameDF, games]).reset_index(drop=True)
    #print(gameDF.reset_index(drop=True))    
    gameDF.reset_index(drop=True).to_csv("monuminGames.csv", sep="|")
    return

monuminTable()


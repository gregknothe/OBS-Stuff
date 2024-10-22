import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import json
import urllib
import requests
import os

#possible useful links
#rarity json file: https://api.ccgtrader.co.uk/_/items/rarities
#card?field
#
#
#

#gameList = ["https://www.ccgtrader.net/games/pokemon-tcg", "https://www.ccgtrader.net/games/magic-the-gathering-ccg", "https://www.ccgtrader.net/games/yu-gi-oh-tcg"]
gameList = ["https://www.ccgtrader.net/games/yu-gi-oh-tcg",
            "https://www.ccgtrader.net/games/pokemon-tcg",
            "https://www.ccgtrader.net/games/magic-the-gathering-ccg",
            "https://www.ccgtrader.net/games/cardcaptors-tcg",
            "https://www.ccgtrader.net/games/hack-g-u",
            "https://www.ccgtrader.net/games/digi-battle-ccg",
            "https://www.ccgtrader.net/games/death-note-tcg",
            "https://www.ccgtrader.net/games/duel-masters-tcg",
            "https://www.ccgtrader.net/games/kingdom-hearts-tcg",
            "https://www.ccgtrader.net/games/one-piece-collectible-card-game",
            "https://www.ccgtrader.net/games/club-penguin-tcg",
            "https://www.ccgtrader.net/games/fire-emblem-cipher-tcg",
            "https://www.ccgtrader.net/games/lego-bionicle-bohrok-swarm-tcg",
            "https://www.ccgtrader.net/games/megaman-nt-warrior-tcg"
            ]

gameList2 = ["https://www.ccgtrader.net/games/sailor-moon-ccg",
             "https://www.ccgtrader.net/games/sonic-x-tcg",
             "https://www.ccgtrader.net/games/naruto-ccg",
             "https://www.ccgtrader.net/games/initial-d-ccg",
             "https://www.ccgtrader.net/games/neopets-tcg",
             "https://www.ccgtrader.net/games/beyblade-ccg",
             "https://www.ccgtrader.net/games/digimon-d-tector-ccg",
             "https://www.ccgtrader.net/games/dragon-ball-super-card-game",
             "https://www.ccgtrader.net/games/final-fantasy-tcg-opus"
             ]

gameList3 = ["https://www.ccgtrader.net/games/hackenemy-ccg",
             "https://www.ccgtrader.net/games/chaotic-tcg",
             "https://www.ccgtrader.net/games/buffy-the-vampire-slayer-ccg",
             "https://www.ccgtrader.net/games/dice-masters",
             "https://www.ccgtrader.net/games/mlb-showdown-ccg",
             "https://www.ccgtrader.net/games/zatch-bell-the-card-battle",
             "https://www.ccgtrader.net/games/jackie-chan-adventures",
             "https://www.ccgtrader.net/games/gundam-ms-war-tcg",
             "https://www.ccgtrader.net/games/fullmetal-alchemist-tcg",
             "https://www.ccgtrader.net/games/dragon-booster-tcg"
            ]

gameList4 = ["https://www.ccgtrader.net/games/anachronism",
             "https://www.ccgtrader.net/games/ani-mayhem-ccg",
             "https://www.ccgtrader.net/games/24-tcg",
             "https://www.ccgtrader.net/games/inuyasha-tcg",
             "https://www.ccgtrader.net/games/the-x-files-ccg",
             "https://www.ccgtrader.net/games/shaman-king-tcg",
             "https://www.ccgtrader.net/games/xiaolin-showdown-tcg",
             "https://www.ccgtrader.net/games/my-hero-academia-ccg",
             "https://www.ccgtrader.net/games/monster-rancher-ccg",
             "https://www.ccgtrader.net/games/monster-hunter-hunting-card-tcg",
             "https://www.ccgtrader.net/games/dreadnought-tcg",
             "https://www.ccgtrader.net/games/blue-dragon-rpcg",
             "https://www.ccgtrader.net/games/bleach-tcg",
             "https://www.ccgtrader.net/games/world-of-warcraft-tcg",
             "https://www.ccgtrader.net/games/ben-10-ccg",
             "https://www.ccgtrader.net/games/anachronism",
             "https://www.ccgtrader.net/games/dragoborne-rise-to-supremacy",
             "https://www.ccgtrader.net/games/wwe-raw-deal",
             "https://www.ccgtrader.net/games/torchwood-tcg",
             "https://www.ccgtrader.net/games/transformers-tcg",
             "https://www.ccgtrader.net/games/redemption-ccg",
             "https://www.ccgtrader.net/games/knights-of-the-zodiac-ccg",
             "https://www.ccgtrader.net/games/dragon-quest-tcg",
             "https://www.ccgtrader.net/games/caster-chronicles-tcg",
             "https://www.ccgtrader.net/games/angry-birds",
             "https://www.ccgtrader.net/games/future-card-buddyfight",
             "https://www.ccgtrader.net/games/the-simpsons-tcg",
             "https://www.ccgtrader.net/games/star-trek-the-card-game-ccg",
             "https://www.ccgtrader.net/games/maplestory-itcg"
            ]


gameList5 = ["https://www.ccgtrader.net/games/dune-ccg"]

def jsonViewer(url):
    resp = requests.get(url)
    data = resp.json()
    with open('subject.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    return

#jsonViewer("https://api.ccgtrader.co.uk/_/items/card?fields%5B0%5D=id&fields%5B1%5D=name&fields%5B2%5D=number&fields%5B3%5D=subtitle&fields%5B4%5D=rarity.id&fields%5B5%5D=image_url&fields%5B6%5D=image.data.asset_url&fields%5B7%5D=number&fields%5B8%5D=reference&fields%5B9%5D=type&fields%5B10%5D=url_title&filter%5Bset%5D%5Beq%5D=1786&sort=number%2Ctype%2Cname&limit=4999")

#jsonViewer("https://api.ccgtrader.co.uk/_/items/card?fields%5B0%5D=id&fields%5B1%5D=name&fields%5B2%5D=number&fields%5B3%5D=subtitle&fields%5B4%5D=rarity.id&fields%5B5%5D=image_url&fields%5B6%5D=image.data.asset_url&fields%5B7%5D=number&fields%5B8%5D=reference&fields%5B9%5D=type&fields%5B10%5D=url_title&filter%5Bset%5D%5Beq%5D=5397&sort=number%2Ctype%2Cname&limit=4999")

def getCards(gameURL):
    req = Request(gameURL, headers={'User-Agent': 'XYZ/3.0'})
    webpage = urlopen(req, timeout=10).read()
    html = bs(webpage, features="lxml")
    return html
    #cardURLs = html.find(class_="MuiImageListItem-root")
    #return cardURLs

def getGameSets(gameURL):
    gameURL = "https://www.ccgtrader.net/page-data/games/" + gameURL.replace("https://www.ccgtrader.net/games/","") + "/page-data.json"
    resp = requests.get(gameURL)
    data = resp.json()
    setList, yearList, idList = [], [], []
    for year in range(len(data["result"]["data"]["directusGame"]["series"])):
        yearData = data["result"]["data"]["directusGame"]["series"][year]
        for set in range(len(data["result"]["data"]["directusGame"]["series"][year]["sets"])):
            setList.append(yearData["sets"][set]["name"])
            yearList.append(yearData["sets"][set]["release_date"])
            idList.append(yearData["sets"][set]["directusId"])
    df = pd.DataFrame({"set": setList, "date": yearList, "setID": idList})
    return df

def getAllGameSets(gameList):
    for game in gameList:
        print(game.replace("https://www.ccgtrader.net/games/",""))
        getGameSets(game).to_csv("cardGamble/gameSets/"+ game.replace("https://www.ccgtrader.net/games/","")+".csv", sep="|", index=False)
    return

#getAllGameSets(gameList4)

def getCards(setID):
    setAPICall = "https://api.ccgtrader.co.uk/_/items/card?fields%5B0%5D=id&fields%5B1%5D=name&fields%5B2%5D=number&fields%5B3%5D=subtitle&fields%5B4%5D=rarity.id&fields%5B5%5D=image_url&fields%5B6%5D=image.data.asset_url&fields%5B7%5D=number&fields%5B8%5D=reference&fields%5B9%5D=type&fields%5B10%5D=url_title&filter%5Bset%5D%5Beq%5D=" + str(setID) + "&sort=number%2Ctype%2Cname&limit=4999"
    resp = requests.get(setAPICall)
    data = resp.json()
    data = data["data"]
    nameList, urlList, rarityList, idList = [], [], [], []
    for card in range(len(data)):
        cardData = data[card]
        nameList.append(cardData["name"])
        try:
            urlList.append(cardData["image"]["data"]["full_url"])
        except:
            urlList.append(cardData["image_url"])
        try:
            rarityList.append(cardData["rarity"]["id"])
        except:
            rarityList.append(0)
        idList.append(cardData["id"])
    df = pd.DataFrame({"name": nameList, "id": idList, "rarity": rarityList, "imgURL": urlList})
    return df

def createGameDataframe():
    #games = os.listdir("E:\Various Programs\Coding Projects\OBS STUFF\cardGamble\gameSets")
    games = [game.replace("https://www.ccgtrader.net/games/","") + ".csv" for game in gameList4]
    for game in games:
        print(">>> " + game.replace(".csv","") + " <<<")
        gameDF = pd.read_csv("cardGamble/gameSets/"+game, delimiter="|")
        idList = gameDF["setID"]
        print("0 : " + str(idList[0]))
        fullDF = getCards(idList[0])
        fullDF["setID"] = idList[0]
        idList.pop(0)
        w = 0
        for setID in idList:
            w += 1
            print(str(w) + " : " + str(setID))
            setDF = getCards(setID)
            setDF["game"] = game
            setDF["setID"] = setID
            fullDF = pd.concat([fullDF, setDF])
        fullDF["game"] = game.replace(".csv","")
        gameDF = pd.read_csv("cardGamble/gameSets/"+game, delimiter="|")
        fullDF = fullDF.merge(gameDF, on="setID", how="left")
        fullDF.to_csv("cardGamble/gameDataframes/"+game, sep="|", index=False)
    return

#createGameDataframe()

def magicUnique():
    df = pd.read_csv("cardGamble/gameDataframes/magic-the-gathering-ccg.csv", delimiter="|").fillna("")
    df = df.sort_values("date", ascending=True).drop_duplicates(subset='name').reset_index(drop=True)
    df.to_csv("cardGamble/gameDataframes/magic-the-gathering-ccg.csv", sep="|")
    return

#magicUnique()

def gameStats():
    games = os.listdir("E:\Various Programs\Coding Projects\OBS STUFF\cardGamble\gameDataframes")
    gameList, rawList, uniqueList = [], [], []
    for game in games:
        df = pd.read_csv("cardGamble/gameDataframes/"+game, delimiter="|").fillna("")
        df = df[df["imgURL"]!=""]
        gameList.append(game.replace(".csv",""))
        rawList.append(len(df.index))
        uniqueList.append(len(df["name"].unique()))
    df = pd.DataFrame({"name": gameList, "raw": rawList, "unique": uniqueList})
    df["raw%"] = df["raw"] / sum(df["raw"].to_list())
    df["raw%"] = df["raw%"].apply(lambda x: f"{x:.3%}")
    df["unique%"] = df["unique"] / sum(df["unique"].to_list())
    df["unique%"] = df["unique%"].apply(lambda x: f"{x:.3%}")
    return df.sort_values('raw', ascending=False)

#print(gameStats().to_string())

def createFinalFile():
    games = os.listdir("E:\Various Programs\Coding Projects\OBS STUFF\cardGamble\gameDataframes")
    finalDF = pd.DataFrame()
    for game in games:
        df = pd.read_csv("cardGamble/gameDataframes/"+game, delimiter="|").fillna("")
        finalDF = pd.concat([finalDF, df])
    finalDF = finalDF.reset_index(drop=True).drop(["Unnamed: 0"], axis=1)
    finalDF = finalDF[finalDF["imgURL"]!=""]
    finalDF.to_csv("cardGamble/finalFile.csv", sep="|", index=False)
    return finalDF

#print(createFinalFile())


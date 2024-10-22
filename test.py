import pandas as pd

gl = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/rankFinalGameList.csv", sep="|").fillna("")
rgl = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/ranceGameList.csv", sep = "|").fillna("")
mgl = pd.read_csv("https://raw.githubusercontent.com/GGSTFrameTrap/gameList/main/monuminGames.csv", sep="|").fillna("")


print("gl")
print(len(gl.index))
print(len(gl[gl["year2"]!=""].index))

print("rgl")
print(len(rgl.index))
print(len(rgl[rgl["year2"]!=""].index))

print("mgl")
print(len(mgl.index))
print(len(mgl[mgl["year2"]!=""].index))


gl = gl[gl["year2"]!=""]
rgl = rgl[rgl["year2"]!=""]
mgl = mgl[mgl["year2"]!=""]

gl.to_csv("finalGameList.csv", sep="|", index=False)
rgl.to_csv("ranceGameList.csv", sep="|", index=False)
mgl.to_csv("monuGameList.csv", sep="|", index=False)

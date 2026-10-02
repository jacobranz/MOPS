from api.clashApi import Clan
from api.clashApi import Player
from data.buildData import War
from data.buildData import CapitalRaid
from data.dbConnect import dbHelper
import json

#API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImNjNmRlMjUzLWE2ZGUtNDg0Ni1iM2U1LWY1ZjUyMjY5ZWQzMyIsImlhdCI6MTc4ODQ5NTAzNywic3ViIjoiZGV2ZWxvcGVyL2ZlMzA3MDZmLWJkNjgtNGFjOC04ZGQ1LTFkMDVjZTBhNTFmMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjc2LjgzLjExMC4yMzQiXSwidHlwZSI6ImNsaWVudCJ9XX0.N3tQyGxUCACOYHzGmd12Af6kmVSfcuY3ssjLLfUSFUdK_rEnbQSsT0yqRHNSxIgIlwrfOdAbjT4WT9OnJJvAEA"
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjcyYTI2NmE2LTg1MDctNGQ3OS05NjVkLTM5MzA4OWU4Mzc4OCIsImlhdCI6MTc4NTEwODE1Mywic3ViIjoiZGV2ZWxvcGVyL2ZlMzA3MDZmLWJkNjgtNGFjOC04ZGQ1LTFkMDVjZTBhNTFmMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjQ3LjE1MC4xNzEuMjIyIl0sInR5cGUiOiJjbGllbnQifV19.GFtnAg3097GwaHZSzNFJrgzNjdfKgzyRfYVWUsg-ZSiD_ykf1-oMrjkMNZIvgyHA3rOBA1p9wzLWHyPP4DpUyw"
getWar = 0
#"#2PUGJQ82G"

playerTags = [
]
clanTags = [
    "#2Q2YL8VGO"
]

def getWarLog():
    for tag in clanTags:
        clan = Clan(API_TOKEN, tag)
        return clan.getWarLog()

def getCurrentWar():
    for tag in clanTags:
        clan = Clan(API_TOKEN, tag)
        return clan.getCurrentWar()

def getCurrentWarMembers():
    for tag in clanTags:
        clan = Clan(API_TOKEN, tag)
        war = clan.getCurrentWar()
        return {
            "clan": war["clan"]["members"], 
            "opponent": war["opponent"]["members"]
        }

def getCapitalRaids():
    for tag in clanTags:
        clan = Clan(API_TOKEN, tag)
        return clan.getCapitalRaidSeason()["items"]

def main():
    ## Connect to database
    db = dbHelper()

    #with open("data.json", "w") as f:
    #    json.dump(getCapitalRaids(), f)

    #for warData in getWarLog()['items']:
    #    war = War(warData)
    #    result = war.parseWar()
    #    db.addWar(result)

    if getWar == 1:
        war = War(getCurrentWar())
        result = war.parseCurrentWar()
        warId = db.addCurrentWar(result)

        members = getCurrentWarMembers()
        for member in members["clan"]:
            warMember = War(member)
            memberResult = warMember.parseWarMembers()
            warMemberId = db.addWarMembers(memberResult, warId)
            for attack in member.get("attacks", []):
                warAttack = War(attack)
                attackResult = warAttack.parseWarAttacks()
                db.addWarAttacks(attackResult, warMemberId)
        for opponent in members["opponent"]:
            opponentMember = War(opponent)
            opponentResult = opponentMember.parseWarMembers()
            warOpponentId = db.addWarMembers(opponentResult, warId)
            for attack in opponent.get("attacks", []):
                warAttack = War(attack)
                attackResult = warAttack.parseWarAttacks()
                db.addWarAttacks(attackResult, warOpponentId)
    else:
        print("War data not running.")

    for raidData in getCapitalRaids():
        raid = CapitalRaid(raidData)
        result = raid.parseRaids()
        raidID = db.addRaidSeasons(result)

        members = raid.parseRaidMembers()
        for member in members:
            raidMemberId = db.addRaidMembers(member, raidID)

    return 0

if __name__ == "__main__":
    exit(main())
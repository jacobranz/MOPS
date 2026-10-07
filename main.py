from api.clashApi import Clan
from api.clashApi import Player
from data.buildData import War
from data.buildData import CapitalRaid
from data.dbConnect import dbHelper
import os
from dotenv import load_dotenv

getWar = 0
getRaid = 0
#"#2PUGJQ82G"
#"#2Q2YL8VGO"

playerTags = [
]
clanTags = [
    "#2PUGJQ82G"
]

## Load env vars
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

## Connect to database
db = dbHelper()

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


if getRaid == 1:
    for raidData in getCapitalRaids():
        raid = CapitalRaid(raidData)
        result = raid.parseRaids()
        raidID = db.addRaidSeasons(result)

        members = raid.parseRaidMembers()
        for member in members:
            raidMemberId = db.addRaidMembers(member, raidID)

        logs = raid.parseRaidLogs()
        for log in logs:
            raidLogId = db.addRaidLogs(log, raidID)

            districts = raid.parseRaidDistricts()
            for district in districts:
                if district["logIndex"] != log["logIndex"]:
                    continue

                raidDistrictId = db.addRaidDistricts(district, raidLogId)

                attacks = raid.parseRaidAttacks()
                for attack in attacks:
                    if attack["logIndex"] != log["logIndex"]:
                        continue

                    db.addRaidAttacks(attack, raidDistrictId)
else:
    print("Raid data not running.")

## Testing data plotting
playerData = db.getPlayerStars()
w = War()
w.plotStarPerPlayer(playerData)
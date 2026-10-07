import matplotlib.pyplot as plt
import numpy as np
import json

class playerData():
    # Graph player data
    def graphPlayer(data):
        player = np.array(data)
        return player

class War():
    def __init__(self, data=None):
        self.data = data

    def parseWar(self):
        try:
            return {
                "result": self.data["result"],
                "endTime": self.data["endTime"],
                "teamSize": self.data["teamSize"],
                "clanTag": self.data["clan"]["tag"],
                "clanName": self.data["clan"]["name"],
                "clanLevel": self.data["clan"]["clanLevel"],
                "clanAttacks": self.data["clan"]["attacks"],
                "clanStars": self.data["clan"]["stars"],
                "clanDestrPer": self.data["clan"]["destructionPercentage"],
                "clanExpEarn": self.data["clan"]["expEarned"],
                "opponentTag": self.data["opponent"]["tag"],
                "opponentName": self.data["opponent"]["name"],
                "opponentLevel": self.data["opponent"]["clanLevel"],
                "opponentStars": self.data["opponent"]["stars"],
                "opponentDestrPer": self.data["opponent"]["destructionPercentage"]
            }
        except KeyError:
            print("Failed to parse json and get all values")
            return None

    def parseCurrentWar(self):
         if self.data["state"] == "notInWar":
            return "notInWar"
         else:
            return {
                "teamSize": self.data["teamSize"],
                "battleMod": self.data["battleModifier"],
                "prepStart": self.data["preparationStartTime"],
                "warStart": self.data["startTime"],
                "warEnd": self.data["endTime"],
                "clanTag": self.data["clan"]["tag"],
                "clanName": self.data["clan"]["name"],
                "clanLevel": self.data["clan"]["clanLevel"],
                "clanAttacks": self.data["clan"]["attacks"],
                "clanStars": self.data["clan"]["stars"],
                "clanDestrPer": self.data["clan"]["destructionPercentage"],
                "opponentTag": self.data["opponent"]["tag"],
                "opponentName": self.data["opponent"]["name"],
                "opponentLevel": self.data["opponent"]["clanLevel"],
                "opponentAttacks": self.data["opponent"]["attacks"],
                "opponentStars": self.data["opponent"]["stars"],
                "opponentDestrPer": self.data["opponent"]["destructionPercentage"]
            }

    def parseWarMembers(self):
        return {
            "playerTag": self.data["tag"],
            "playerName": self.data["name"],
            "playerThLevel": self.data["townhallLevel"],
            "playerMapPos": self.data["mapPosition"]
        }

    def parseWarAttacks(self):
        return {
            "attackerTag": self.data["attackerTag"],
            "defenderTag": self.data["defenderTag"],
            "attackStars": self.data["stars"],
            "attackDestrPer": self.data["destructionPercentage"],
            "attackOrder": self.data["order"],
            "attackDuration": self.data["duration"]
        }

    def getMembers(self):
        pass

    def getAttacks(self):
        pass

    def plotWarHist(self, warData):
        self.dates = []
        self.destrPercent = []

        for war in warData:
            self.dates.append(war[0])
            self.destrPercent.append(war[7])


        plt.scatter(self.dates, self.destrPercent)

        plt.xlabel("War Date")
        plt.ylabel("Destruction %")
        plt.title("Clan Destruction % Over Time")

        plt.ylim(0, 100)

        plt.show()

    def plotPlayerConsistency(self, playerData):
        self.players = {}

        for player, destruction in playerData:

            if player not in self.players:
                self.players[player] = []

            self.players[player].append(destruction)

        playerNames = list(self.players.keys())
        destructionData = list(self.players.values())

        height = max(8, len(playerNames) * 0.35)

        plt.figure(figsize=(10, height))

        plt.boxplot(
            destructionData,
            vert=False
        )

        plt.yticks(
            range(1, len(playerNames) + 1),
            playerNames,
            fontsize=8
        )

        plt.xlabel("Player")
        plt.ylabel("Destruction %")
        plt.title("Player Destruction Consistency")

        plt.xlim(0, 100)

        plt.xticks(range(0, 101, 10))

        plt.subplots_adjust(
            left=0.25,
            right=0.95,
            top=0.95,
            bottom=0.10
        )   
        plt.show()

    def plotStarPerPlayer(self, playerData):
        self.players = {}

        for player, stars in playerData:
            if player not in self.players:
                self.players[player] = []

            self.players[player].append(stars)

        playerNames = list(self.players.keys())

        starCounts = []

        for player in playerNames:
            zeroStars = self.players[player].count(0)
            oneStar = self.players[player].count(1)
            twoStars = self.players[player].count(2)
            threeStars = self.players[player].count(3)

            starCounts.append([
                zeroStars,
                oneStar,
                twoStars,
                threeStars
            ])

        starCounts = list(zip(*starCounts))

        plt.figure(figsize=(12, max(8, len(playerNames) * 0.35)))

        plt.barh(
            playerNames,
            starCounts[0],
            label="0 Stars"
        )

        plt.barh(
            playerNames,
            starCounts[1],
            label="1 Stars"
        )

        plt.barh(
            playerNames,
            starCounts[2],
            left=[
                starCounts[0][i] + starCounts[1][i]
                for i in range(len(playerNames))
            ],
            label="2 Stars"
        )

        plt.barh(
            playerNames,
            starCounts[3],
            left=[
                starCounts[0][i] +
                starCounts[1][i] +
                starCounts[2][i]
                for i in range(len(playerNames))
            ],
            label="3 Stars"
        )

        plt.xlabel("Number of Attacks")
        plt.ylabel("Player")
        plt.title("Player Star Distribution")

        plt.legend()

        plt.show()

    def plotWarParticipation(self, playerData):

        self.players = {}

        for player, warID in playerData:
            if player not in self.players:
                self.players[player] = set()

            self.players[player].add(warID)

        playerNames = list(self.players.keys())

        warIDs = sorted(
            set(warID for player, warID in playerData)
        )

        participationData = []

        for player in playerNames:
            row = []
            for warID in warIDs:
                if warID in self.players[player]:
                    row.append(1)
                else:
                    row.append(0)

            participationData.append(row)

        plt.figure(
            figsize=(
                max(10, len(warIDs) * 0.7),
                max(8, len(playerNames) * 0.5)
            )
        )

        plt.imshow(participationData, aspect="auto")

        plt.xticks(
            range(len(warIDs)),
            warIDs,
            rotation=90,
            fontsize=8
        )

        plt.yticks(
            range(len(playerNames)),
            playerNames,
            fontsize=8
        )

        plt.xlabel("War ID")
        plt.ylabel("Player")
        plt.title("Player War Participation")

        plt.colorbar(
            label="Participation"
        )

        plt.subplots_adjust(
            left=0.25,
            right=0.95,
            top=0.95,
            bottom=0.25
        )

        plt.show()

class CapitalRaid():
    def __init__(self, data):
        self.data = data

    def parseRaids(self):
        return {
            "state": self.data["state"],
            "raidStart": self.data["startTime"],
            "raidEnd": self.data["endTime"],
            "totalLoot": self.data["capitalTotalLoot"],
            "raidCount": self.data["raidsCompleted"],
            "attackCount": self.data["totalAttacks"],
            "destrDistrictCount": self.data["enemyDistrictsDestroyed"],
            "offenseReward": self.data["offensiveReward"],
            "defenseReward": self.data["defensiveReward"],
        }

    def parseRaidMembers(self):
        self.members = []

        for member in self.data.get("members", []):
            self.members.append({
                "tag": member["tag"],
                "name": member["name"],
                "attacks": member["attacks"],
                "attackLimit": member["attackLimit"],
                "bonusAttackLimit": member["bonusAttackLimit"],
                "resourcesLooted": member["capitalResourcesLooted"]
            })

        return self.members

    def parseRaidLogs(self):
        self.logs = []

        for logIndex, log in enumerate(self.data["attackLog"], start=1):
            self.logs.append({
                "logIndex": logIndex,
                "logType": "attack",
                "clanTag": log["defender"]["tag"],
                "clanName": log["defender"]["name"],
                "clanLevel": log["defender"]["level"],
                "attackCount": log["attackCount"],
                "districtCount": log["districtCount"],
                "districtsDestroyed": log["districtsDestroyed"]
            })

        for logIndex, log in enumerate(self.data["defenseLog"], start=len(self.logs) + 1):
            self.logs.append({
                "logIndex": logIndex,
                "logType": "defense",
                "clanTag": log["attacker"]["tag"],
                "clanName": log["attacker"]["name"],
                "clanLevel": log["attacker"]["level"],
                "attackCount": log["attackCount"],
                "districtCount": log["districtCount"],
                "districtsDestroyed": log["districtsDestroyed"]
            })

        return self.logs

    def parseRaidDistricts(self):
        self.districts = []

        for logIndex, log in enumerate(self.data["attackLog"], start=1):
            for district in log["districts"]:
                self.districts.append({
                    "logIndex": logIndex,
                    "districtID": district["id"],
                    "districtName": district["name"],
                    "stars": district["stars"],
                    "districtHallLevel": district["districtHallLevel"],
                    "destructionPercentage": district["destructionPercent"],
                    "attackCount": district["attackCount"],
                    "totalLooted": district["totalLooted"]
                })

        for logIndex, log in enumerate(self.data["defenseLog"], start=len(self.logs) + 1):
            for district in log["districts"]:
                self.districts.append({
                    "logIndex": logIndex,
                    "districtID": district["id"],
                    "districtName": district["name"],
                    "districtHallLevel": district["districtHallLevel"],
                    "stars": district["stars"],
                    "destructionPercentage": district["destructionPercent"],
                    "attackCount": district["attackCount"],
                    "totalLooted": district["totalLooted"]
                })

        return self.districts

    def parseRaidAttacks(self):
        self.attacks = []

        for logIndex, log in enumerate(self.data["attackLog"], start=1):
            for district in log["districts"]:
                for attacker in district.get("attacks", []):
                    self.attacks.append({
                        "logIndex": logIndex,
                        "districtId": district["id"],
                        "tag": attacker["attacker"]["tag"],
                        "name": attacker["attacker"]["name"],
                        "destrPercent": attacker["destructionPercent"],
                        "stars": attacker["stars"]
                    })

        for logIndex, log in enumerate(self.data["defenseLog"], start=len(self.attacks) + 1):
            for district in log["districts"]:
                for attacker in district.get("attacks", []):
                    self.attacks.append({
                        "logIndex": logIndex,
                        "districtId": district["id"],
                        "tag": attacker["attacker"]["tag"],
                        "name": attacker["attacker"]["name"],
                        "destrPercent": attacker["destructionPercent"],
                        "stars": attacker["stars"]
                    })

        return self.attacks
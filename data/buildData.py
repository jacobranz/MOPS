import matplotlib as plt
import numpy as np
import json

class playerData():
    # Graph player data
    def graphPlayer(data):
        player = np.array(data)
        return player

class War():
    def __init__(self, data):
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

class CapitalRaid():
    def __init__(self, data):
        self.data = data

    def parseRaids(self):
        return {
            "state": self.data["state"],
            "raidStart": self.data["startTime"],
            "raidEnd": self.data["endTime"],
            "totalLoot": self.data["totalLoot"],
            "raidCount": self.data["completedRaidCount"],
            "attackCount": self.data["attackCount"],
            "destrDistrictCount": self.data["destroyedDistrictCount"],
            "offenseReward": self.data["offensiveReward"],
            "defenseReward": self.data["defensiveReward"],
            "defenseLoot": self.data["totalDefensiveLoot"],
            "defenseAttacks": self.data["defenseAttackCount"],
            "defenseDestrDistrictCount": self.data["defensiveDestroyedDistrictCount"]
        }

    def parseRaidMembers(self):
        self.members = []

        for member in self.data["members"]:
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

        for log in self.data["attackLog"]:
            self.logs.append({
                "logType": "attack",
                "clanTag": log["defender"]["tag"],
                "clanName": log["defender"]["name"],
                "clanLevel": log["defender"]["clanLevel"],
                "attackCount": log["attackCount"],
                "districtCount": log["districtCount"],
                "districtsDestroyed": log["districtsDestroyed"]
            })

        for log in self.data["defenseLog"]:
            self.logs.append({
                "logType": "defense",
                "clanTag": log["attacker"]["tag"],
                "clanName": log["attacker"]["name"],
                "clanLevel": log["attacker"]["clanLevel"],
                "attackCount": log["attackCount"],
                "districtCount": log["districtCount"],
                "districtsDestroyed": log["districtsDestroyed"]
            })

        return self.logs

    def parseRaidDistricts(self):
        self.districts = []

        for log in self.data["attackLog"]:
            for district in log["districts"]:
                self.districts.append({
                    "districtID": district["id"],
                    "districtName": district["name"],
                    "stars": district["stars"],
                    "districtHallLevel": district["districtHallLevel"],
                    "destructionPercentage": district["destructionPercent"],
                    "attackCount": district["attackCount"],
                    "totalLoot": district["totalLooted"]
                })

        for log in self.data["defenseLog"]:
            for district in log["districts"]:
                self.districts.append({
                    "districtID": district["id"],
                    "districtName": district["name"],
                    "districtHallLevel": district["districtHallLevel"],
                    "stars": district["stars"],
                    "destructionPercentage": district["destructionPercent"],
                    "attackCount": district["attackCount"],
                    "totalLoot": district["totalLooted"]
                })

        return self.districts

    def parseRaidAttacks(self):
        self.attacks = []

        for log in self.data["attackLog"]:
            for district in log["districts"]:
                for attacker in district["attacks"]:
                    self.attacks.append({
                        "tag": attacker["attacker"]["tag"],
                        "name": attacker["attacker"]["name"],
                        "destrPercent": attacker["destructionPercent"],
                        "stars": attacker["stars"]
                    })

        for log in self.data["defenseLog"]:
            for district in log["districts"]:
                for attacker in district["attacks"]:
                    self.attacks.append({
                        "tag": attacker["attacker"]["tag"],
                        "name": attacker["attacker"]["name"],
                        "destrPercent": attacker["destructionPercent"],
                        "stars": attacker["stars"]
                    })

        return self.attacks
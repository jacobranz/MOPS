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
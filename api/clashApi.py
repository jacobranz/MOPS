import requests
import json
import csv

class Player():
    def __init__(self, token, tag):
        self.apiToken = token
        self.playerTag = tag

    def get_info(self):
        encoded_tag = self.playerTag.replace("#", "%23")
        url = f"https://api.clashofclans.com/v1/players/{encoded_tag}"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def queryPlayer(self, fields):
        self.playerInfo = self.get_info()

        return {
            field: self.playerInfo[field]
            for field in fields
            if field in self.playerInfo
        }

class Clan():
    def __init__(self, token, tag):
        self.apiToken = token
        self.clanTag = tag

    def getWarLog(self):
        encoded_tag = self.clanTag.replace("#", "%23")
        url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/warlog"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def getCurrentWar(self):
        encoded_tag = self.clanTag.replace("#", "%23")
        url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/currentwar"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        }

        response = requests.get(url, headers=headers, timeout=30)

        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()

        return response.json()

    def getCurrentWarMembers(self):
        encoded_tag = self.clanTag.replace("#", "%23")
        url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/currentwar"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()
    
    def queryClan(self, fields):
        self.clanInfo = self.get_info()

        return {
            field: self.clanInfo[field]
            for field in fields
            if field in self.clanInfo
        }

    def createMemberList(self):
        self.memberList = []
        print(self.queryClan('memberList'))
        self.members = self.queryClan(['memberList'])

        for member in self.members:
            self.memberList.append(member['tag'])

        return self.memberList

    def getCapitalRaidSeason(self):
        encoded_tag = self.clanTag.replace("#", "%23")

        url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/capitalraidseasons"

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.apiToken}"
        }

        response = requests.get(url, headers=headers, timeout=30)

        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()

        return response.json()

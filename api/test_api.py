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

        response = requests.get(url, headers=headers)
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

# Instantiate class
#API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjhjMzFhYTEwLTRkYTYtNGJmMi05NjkyLTViODM4ODg3YmNhYyIsImlhdCI6MTc4NjQxODIyMiwic3ViIjoiZGV2ZWxvcGVyL2ZlMzA3MDZmLWJkNjgtNGFjOC04ZGQ1LTFkMDVjZTBhNTFmMyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE4Ny4xMy4xNDMuMjA0Il0sInR5cGUiOiJjbGllbnQifV19._tOYShTW-u0DO58wfHpqPFKMjzqV6xkwZ1mwse4lfd2qmH8LOKLKZb21Q78xOuMTZ0CiVX6iPi3x0xeph1vOdQ"
'''
with open("coc_clan_data.csv", "a", newline="") as clanscv:
    writer = csv.DictWriter(clanscv, fieldnames=clanFields)
    writer.writeheader()

    for tag in clanTags:
        clan = Clan(API_TOKEN, tag)

        data = clan.queryClan(clanFields)

        writer.writerow(data)
'''

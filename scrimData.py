import json
import pprint
import time
from datetime import datetime
from urllib.request import urlopen
from riotwatcher import LolWatcher
import champList
import jsonReader

# global variables
api_key = 'RGAPI-b9d751b2-b394-4712-af11-5372360d6780'
watcher = LolWatcher(api_key)

# riot watcher constructor
scrimRegion = 'LA1'
scrimSN = 'emarlin'  # mid player, está en todos los juegos
scrimRW = watcher.summoner.by_name(scrimRegion, scrimSN)
# item list
itemURL = urlopen('http://ddragon.leagueoflegends.com/cdn/12.8.1/data/en_US/item.json')
itemList = json.loads(itemURL.read())
# champ list
championsList = champList.champList
# scrim match history
scrim_match_history = watcher.match.matchlist_by_puuid(scrimRegion, scrimRW['puuid'], None, 10, 0, None, None, None)
print(scrim_match_history)


def getScrimDetails(playerRegion, playerMatchHistory, jsonFile):
    # fetch last match detail
    for i in playerMatchHistory:
        playerlistObj = []
        last_match = i
        print('ID de la partida: ', last_match)
        match_detail = watcher.match.by_id(playerRegion, last_match)
        print('Detalles de la partida: ', match_detail)
        playerCount = len(match_detail['metadata']['participants'])
        if match_detail['info']['gameType'] == 'CUSTOM_GAME' and playerCount == 10:
            playerData = []
            print('Consiguiendo detalles de la partida.')
            gameDetails_row = {}
            gameDetails_row['MatchID'] = match_detail['metadata']['matchId']
            gameDate = int(match_detail['info']['gameCreation']) / 1000
            gameDateConverted = datetime.utcfromtimestamp(gameDate).strftime('%Y-%m-%d')
            gameDetails_row['Date'] = gameDateConverted
            playerData.append(gameDetails_row)
            for team in match_detail['info']['teams']:
                teamDetails_row = {}
                for a in team['bans']:
                    ban = list(championsList.keys())[list(championsList.values()).index(a['championId'])]
                    print(ban)
                teamSide = team['teamId']
                if teamSide == 100:
                    teamDetails_row['Side'] = "Blue"
                else:
                    teamDetails_row['Side'] = "Red"
                teamWin = team['win']
                if teamWin:
                    teamDetails_row['Win'] = 1
                else:
                    teamDetails_row['Win'] = 0
                if team['objectives']['baron']['first']:
                    teamDetails_row['First Baron'] = 1
                else:
                    teamDetails_row['First Baron'] = 0
                teamDetails_row['Baron Kills'] = team['objectives']['baron']['kills']
                if team['objectives']['champion']['first']:
                    teamDetails_row['First Blood'] = 1
                else:
                    teamDetails_row['First Blood'] = 0
                teamDetails_row['Team Kills'] = team['objectives']['champion']['kills']
                if team['objectives']['dragon']['first']:
                    teamDetails_row['First Dragon'] = 1
                else:
                    teamDetails_row['First Dragon'] = 0
                teamDetails_row['Dragon Kills'] = team['objectives']['dragon']['kills']
                if team['objectives']['inhibitor']['first']:
                    teamDetails_row['First Inhib'] = 1
                else:
                    teamDetails_row['First Inhib'] = 0
                teamDetails_row['Inhib Kills'] = team['objectives']['inhibitor']['kills']
                if team['objectives']['riftHerald']['first']:
                    teamDetails_row['First Herald'] = 1
                else:
                    teamDetails_row['First Herald'] = 0
                teamDetails_row['Herald Kills'] = team['objectives']['riftHerald']['kills']
                if team['objectives']['tower']['first']:
                    teamDetails_row['First Turret'] = 1
                else:
                    teamDetails_row['First Turret'] = 1
                teamDetails_row['Turret Kills'] = team['objectives']['tower']['kills']
                playerData.append(teamDetails_row)
                playerlistObj.append(playerData)
            for row in match_detail['info']['participants']:
                participants_row = {}
                participants_row['Game ID'] = gameDetails_row['MatchID']
                puuid = row['puuid']
                account = watcher.summoner.by_puuid(playerRegion, puuid)
                participants_row['Summoner Name'] = account['name']
                participants_row['Champion'] = row['championName']
                participants_row['Kills'] = row['kills']
                participants_row['Solo Kills'] = row['challenges']['soloKills']
                try:
                    participants_row['Kills as Jungle'] = row['challenges']['killsOnLanersEarlyJungleAsJungler']
                except KeyError:
                    participants_row['Kills as Jungle'] = 0
                participants_row['Assists'] = row['assists']
                participants_row['Deaths'] = row['deaths']
                participants_row['KDA'] = row['challenges']['kda']
                try:
                    participants_row['Kill Participation'] = row['challenges']['killParticipation']
                except KeyError:
                    participants_row['Kill Participation'] = 0
                participants_row['Kill Deficit'] = row['challenges']['maxKillDeficit']
                participants_row['Multikills'] = row['challenges']['multikills']
                participants_row['Level'] = row['champLevel']
                try:
                    participants_row['Max Level Advantage'] = row['challenges']['maxLevelLeadLaneOpponent']
                except KeyError:
                    participants_row['Max Level Advantage'] = 0
                participants_row['Farm'] = row['totalMinionsKilled']
                participants_row['Farm at 10 Minutes'] = row['challenges']['laneMinionsFirst10Minutes']
                try:
                    participants_row['Farm Advantage'] = row['challenges']['maxCsAdvantageOnLaneOpponent']
                except KeyError:
                    participants_row['Farm Advantage'] = 0
                participants_row['Camps'] = row['neutralMinionsKilled']
                participants_row['Gold Earned'] = row['goldEarned']
                participants_row['Gold Spent'] = row['goldSpent']
                participants_row['Gold per Minute'] = row['challenges']['goldPerMinute']
                participants_row['Damage Dealt'] = row['totalDamageDealtToChampions']
                participants_row['Damage per Minute'] = row['challenges']['damagePerMinute']
                participants_row['Damage Percentage'] = row['challenges']['damageTakenOnTeamPercentage']
                participants_row['Skillshots Hit'] = row['challenges']['skillshotsHit']
                participants_row['Skillshots Dodged'] = row['challenges']['skillshotsDodged']
                participants_row['Damage to Buildings'] = row['damageDealtToBuildings']
                participants_row['Damage to Objectives'] = row['damageDealtToObjectives']
                participants_row['Barons Killed'] = row['baronKills']
                participants_row['Baron Takedowns'] = row['challenges']['baronTakedowns']
                participants_row['Dragons Killed'] = row['dragonKills']
                participants_row['Dragon Takedowns'] = row['challenges']['dragonTakedowns']
                participants_row['Herald Takedowns'] = row['challenges']['riftHeraldTakedowns']
                participants_row['Objectives Stolen'] = row['challenges']['epicMonsterSteals']
                participants_row['Turrets with Herald'] = row['challenges']['turretsTakenWithRiftHerald']
                participants_row['Turret Plates'] = row['challenges']['turretPlatesTaken']
                participants_row['Turret Takedowns'] = row['challenges']['turretTakedowns']
                try:
                    participants_row['Sight Wards'] = row['sightWardsBoughtInGame']
                except KeyError:
                    participants_row['Sight Wards'] = 0
                try:
                    participants_row['Vision Wards'] = row['visionWardsBoughtInGame']
                except KeyError:
                    participants_row['Vision Wards'] = 0
                try:
                    participants_row['Wards Placed'] = row['wardsPlaced']
                except KeyError:
                    participants_row['Wards Placed'] = 0
                try:
                    participants_row['Wards Killed'] = row['wardsKilled']
                except KeyError:
                    participants_row['Wards Killed'] = 0
                try:
                    participants_row['Vision Score'] = row['visionScore']
                except KeyError:
                    participants_row['Vision Score'] = 0
                try:
                    if row['win']:
                        participants_row['Win'] = 1
                    else:
                        participants_row['Win'] = 0
                except KeyError:
                    participants_row['Win'] = 0
                # item section
                if row['item0'] != 0:
                    item0Id = row['item0']
                    item0 = itemList['data'][str(item0Id)]['name']
                    participants_row['item1'] = item0
                else:
                    participants_row['item1'] = 'NA'
                if row['item1'] != 0:
                    item1Id = row['item1']
                    item1 = itemList['data'][str(item1Id)]['name']
                    participants_row['item2'] = item1
                else:
                    participants_row['item2'] = 'NA'
                if row['item2'] != 0:
                    item2Id = row['item2']
                    item2 = itemList['data'][str(item2Id)]['name']
                    participants_row['item3'] = item2
                else:
                    participants_row['item3'] = 'NA'
                if row['item3'] != 0:
                    item3Id = row['item3']
                    item3 = itemList['data'][str(item3Id)]['name']
                    participants_row['item4'] = item3
                else:
                    participants_row['item4'] = 'NA'
                if row['item4'] != 0:
                    item4Id = row['item4']
                    item4 = itemList['data'][str(item4Id)]['name']
                    participants_row['item5'] = item4
                else:
                    participants_row['item5'] = 'NA'
                if row['item5'] != 0:
                    item5Id = row['item5']
                    item5 = itemList['data'][str(item5Id)]['name']
                    participants_row['item6'] = item5
                else:
                    participants_row['item6'] = 'NA'
                # end of item section
                playerData.append(participants_row)
                # pprint.pprint(playerData, sort_dicts=False)
                playerlistObj.append(playerData)
                with open(jsonFile, "w") as write_file:
                    json.dump(playerlistObj, write_file, indent=4)
                    # with open("matchData.json", "w") as write_file:
                    #    json.dump(playerData, write_file, indent=4)

                    # code for the requests to load

            print('Se consiguieron los detalles correctamente.')
            time.sleep(1)
            jsonReader.openJSON("scrimData.json", "scrimData.txt")
            input("Presione Enter para continuar al siguiente juego...")

        else:
            print("Juego no válido.")
            time.sleep(1)

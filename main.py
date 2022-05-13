# imports
from riotwatcher import LolWatcher
from urllib.request import urlopen
from datetime import datetime
import json
import time
import pprint
import jsonReader
import scrimData


# global variables
api_key = 'RGAPI-b9d751b2-b394-4712-af11-5372360d6780'
watcher = LolWatcher(api_key)

# scrim variables
scrimRegion = 'LA1'
scrimSN = 'emarlin'  # mid player, está en todos los juegos
scrimRW = watcher.summoner.by_name(scrimRegion, scrimSN)

# player regions
# <editor-fold desc="PLAYER REGIONS">
topRegion = 'NA1'
jgRegion = 'NA1'
midRegion = 'NA1'
adcRegion = 'NA1'
suppRegion = 'NA1'
top2Region = "NA1"
# </editor-fold>

# player summoner names
# <editor-fold desc="PLAYERS' SN AND NOTES">
topSN = 'Testlye'  # ElectricDagger
jgSN = 'Suicide Symphony'  # Lullaby
midSN = "Teethkel"  # Emarlin smurf
top2SN = '7w7'  # Darkin
suppSN = 'Grathid'  # Grathid
adcSN = 'Pudrod'  # Daycrow
# </editor-fold>

# player riotWatchers
# <editor-fold desc="RW OBJECT CREATION">
topRW = watcher.summoner.by_name(topRegion, topSN)
jgRW = watcher.summoner.by_name(jgRegion, jgSN)
midRW = watcher.summoner.by_name(midRegion, midSN)
adcRW = watcher.summoner.by_name(adcRegion, adcSN)
suppRW = watcher.summoner.by_name(suppRegion, suppSN)
top2RW = watcher.summoner.by_name(top2Region, top2SN)
# </editor-fold>

# file creation and checkup
# <editor-fold desc="FILE CREATION FROM SCRATCH">
scrimFilename = r'C:\Users\aange\PycharmProjects\RiotAPI\scrimData.json'
scrimlistObj = []

top2Filename = r'C:\Users\aange\PycharmProjects\RiotAPI\top2Data.json'
top2listObj = []

topFilename = r'C:\Users\aange\PycharmProjects\RiotAPI\topData.json'
toplistObj = []

jgFilename = r'C:\Users\aange\PycharmProjects\RiotAPI\jgData.json'
jglistObj = []

midFilename = r'C:\Users\aange\PycharmProjects\RiotAPI\midData.json'
midlistObj = []

adcFilename = r'C:\Users\aange\PycharmProjects\RiotAPI\adcData.json'
adclistObj = []

suppFilename = r'C:\Users\aange\PycharmProjects\RiotAPI\suppData.json'
supplistObj = []
# </editor-fold>

# item list
itemURL = urlopen('http://ddragon.leagueoflegends.com/cdn/12.8.1/data/en_US/item.json')
itemList = json.loads(itemURL.read())

# return the rank status for the account
"""
top_ranked_stats = watcher.league.by_summoner(topRegion, topRW['id'])
print(top_ranked_stats)
jg_ranked_stats = watcher.league.by_summoner(jgRegion, jgRW['id'])
print(jg_ranked_stats)
mid_ranked_stats = watcher.league.by_summoner(midRegion, midRW['id'])
print(mid_ranked_stats)
adc_ranked_stats = watcher.league.by_summoner(adcRegion, adcRW['id'])
print(adc_ranked_stats)
supp_ranked_stats = watcher.league.by_summoner(suppRegion, suppRW['id'])
print(supp_ranked_stats)
time.sleep(3)
"""

# get match history
# <editor-fold desc="MATCH HISTORY CREATION">
scrim_match_history = watcher.match.matchlist_by_puuid(scrimRegion, scrimRW['puuid'], None, 10, 0, None, None, None)
# print(scrim_match_history)
top_match_history = watcher.match.matchlist_by_puuid(topRegion, topRW['puuid'], None, 10, 420, None, None, None)
# top_match_history.extend(watcher.match.matchlist_by_puuid(topRegion, topRW['puuid'], None, 5, 0, None, None, None))
# print(top_match_history)
top2_match_history = watcher.match.matchlist_by_puuid(top2Region, top2RW['puuid'], None, 10, 420, None, None, None)
# top_match_history.extend(watcher.match.matchlist_by_puuid(topRegion, topRW['puuid'], None, 5, 0, None, None, None))
# print(top_match_history)
jg_match_history = watcher.match.matchlist_by_puuid(jgRegion, jgRW['puuid'], None, 10, 420, None, None, None)
# jg_match_history.extend(watcher.match.matchlist_by_puuid(jgRegion, jgRW['puuid'], None, 5, 0, None, None, None))
# print(jg_match_history)
mid_match_history = watcher.match.matchlist_by_puuid(midRegion, midRW['puuid'], None, 10, 420, None, None, None)
# mid_match_history.extend(watcher.match.matchlist_by_puuid(midRegion, midRW['puuid'], None, 5, 0, None, None, None))
# print(mid_match_history)
adc_match_history = watcher.match.matchlist_by_puuid(adcRegion, adcRW['puuid'], None, 10, 420, None, None, None)
# adc_match_history.extend(watcher.match.matchlist_by_puuid(adcRegion, adcRW['puuid'], None, 5, 0, None, None, None))
# print(adc_match_history)
supp_match_history = watcher.match.matchlist_by_puuid(suppRegion, suppRW['puuid'], None, 10, 420, None, None, None)
# </editor-fold>


# supp_match_history.extend(watcher.match.matchlist_by_puuid(suppRegion, suppRW['puuid'], None, 5, 0, None, None, None))
# print(supp_match_history)


def getMatchDetails(playerRegion, playerMatchHistory, jsonFile, playerRW, playerlistObj):
    # fetch last match detail
    for i in playerMatchHistory:
        last_match = i
        print('ID de la partida: ', last_match)
        match_detail = watcher.match.by_id(playerRegion, last_match)
        print('Detalles de la partida: ', match_detail)
        if (match_detail['info']['gameType'] == 'MATCHED_GAME' or match_detail['info']['gameType'] == 'CUSTOM_GAME') and \
                match_detail['info']['gameMode'] == "CLASSIC":
            playerData = []
            print('Consiguiendo detalles de la partida.')
            for row in match_detail['info']['participants']:
                if row['puuid'] == playerRW['puuid']:
                    participants_row = {}
                    gameDate = int(match_detail['info']['gameCreation']) / 1000
                    gameDateConverted = datetime.utcfromtimestamp(gameDate).strftime('%Y-%m-%d')
                    participants_row['Date'] = gameDateConverted
                    participants_row['Game Version'] = match_detail['info']['gameVersion']
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
        else:
            print("Invalid Game")
            time.sleep(1)


"""
getMatchDetails(top2Region, top2_match_history, 'top2Data.json', top2RW, top2listObj)
jsonReader.openJSON("top2Data.json", "top2Data.txt")
getMatchDetails(topRegion, top_match_history, 'topData.json', topRW, toplistObj)
jsonReader.openJSON("topData.json", 'top1Data.txt')
getMatchDetails(jgRegion, jg_match_history, 'jgData.json', jgRW, jglistObj)
jsonReader.openJSON("jgData.json", 'jgData.txt')
getMatchDetails(midRegion, mid_match_history, 'midData.json', midRW, midlistObj)
jsonReader.openJSON("midData.json", "midData.txt")
getMatchDetails(adcRegion, adc_match_history, 'adcData.json', adcRW, adclistObj)
jsonReader.openJSON("adcData.json", "adcData.txt")
getMatchDetails(suppRegion, supp_match_history, 'suppData.json', suppRW, supplistObj)
jsonReader.openJSON("suppData.json", "suppData.txt")"""
scrimData.getScrimDetails(scrimRegion, scrim_match_history, 'scrimData.json')

print("FIN DEL PROGRAMA")

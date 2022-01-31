import requests
import time
from datetime import date
from pprint import pprint
import html2text
import mysql.connector
from mysql.connector import Error
from random import randint
import json

from secrets import TFTheaders
from databases import *



ids=[]
var=""
cursor = conn.cursor()


def check_sql_string(sql, values):
    unique = "%PARAMETER%"
    sql = sql.replace("%s", unique)
    for v in values: sql = sql.replace(unique, repr(v), 1)
    return sql

class masterdata:
    cursor = conn.cursor()

    def addsummoner(self, ids):
        # https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/*

        for summ in ids:
            time.sleep(2)
            r = requests.get(str('https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' +summ), headers=TFTheaders)
            query = """ REPLACE INTO tft_summoner
            (accountId, id, name, profileIconId, puuid, revisionDate, summonerLevel)
            VALUES 
            (%s, %s, %s, %s, %s, %s,%s) """
            summoner=r.json()
            #summoner["_id"]=summoner["id"]
            if "id" in summoner:
                #pprint(summoner["revisionDate"])
                #epoch to datetime
                RevDate= time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime(summoner["revisionDate"]/1000.))
                data = (summoner['accountId'],summoner['id'],summoner['name'],summoner['profileIconId'],summoner['puuid'],RevDate,summoner['summonerLevel'],)
                #pprint(check_sql_string(query,data))
                try:
                    # update
                    cursor = conn.cursor()
                    cursor.execute(query, data)
                    # accept the changes
                    conn.commit()
                    pprint(summoner['name'])

                except Error as error:
                    print(error)

                finally:
                    cursor.close()

    def addleague(self):
        #get all the summoner ids
        query = """SELECT id FROM tft_summoner"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for summ in results:
            summ=''.join(summ)
            time.sleep(2)
            #https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/nqc05hR8dIWltj352vriRHbhrQSwWqM8gLr-6IW_IXHoTqA
            r = requests.get(str('https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/' +summ), headers=TFTheaders)
            summoner=r.json()
            
            #Does the summoner plays TFT at all ?
            if summoner == []:
                continue

            if 'status' in summoner:
                pprint(summoner)
                time.sleep(500)


            for summoner_data in summoner:

                if summoner_data["queueType"]=="RANKED_TFT_TURBO":
                    summoner_turbo=summoner_data
                    #tft_league_ranked_tft_turbo
                    query = """ REPLACE INTO tft_league_ranked_turbo (summonerId, queueType, ratedRating, summonerName, wins, losses, ratedTier, LastUpdateDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
                    data = (summoner_turbo['summonerId'],summoner_turbo['queueType'],summoner_turbo['ratedRating'],summoner_turbo['summonerName'],summoner_turbo['wins'],summoner_turbo['losses'],summoner_turbo['ratedTier'],date.today())
                    try:
                        # update
                        cursor = conn.cursor()
                        cursor.execute(query, data)
                        # accept the changes
                        conn.commit()
                        pprint(str("tft_league_turbo: ")+summoner_turbo['summonerName'])

                    except Error as error:
                        print(error)

                    finally:
                        cursor.close()

                elif summoner_data["queueType"]=="RANKED_TFT":
                    summoner_ranked=summoner_data
                    #tft_league_ranked
                    
                    Tiers_LP_values={"IRON":0,"BRONZE":400,"SILVER":800,"GOLD":1200,"PLATINUM":1600,"DIAMOND":2000,"MASTER":2400,"GRANDMASTER":2400,"CHALLENGER":2400}
                    tftrank_LP_values={"IV":0,"III":100,"II":200,"I":300}
                    CalcRating = Tiers_LP_values[summoner_ranked['tier']] + tftrank_LP_values[summoner_ranked['rank']] +summoner_ranked['leaguePoints']

                    query = """ REPLACE INTO tft_league_ranked (summonerId, summonerName, leagueId, queueType, tier, tftrank, leaguePoints, wins, losses, veteran, IsInactive, freshBlood, hotStreak, CalcRating, LastUpdateDate) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                    data = (summoner_ranked['summonerId'],summoner_ranked['summonerName'],summoner_ranked['leagueId'],summoner_ranked['queueType'],summoner_ranked['tier'],summoner_ranked['rank'],
                    summoner_ranked['leaguePoints'],summoner_ranked['wins'],summoner_ranked['losses'],str(summoner_ranked['veteran']),str(summoner_ranked['inactive']),str(summoner_ranked['freshBlood']),str(summoner_ranked['hotStreak']), CalcRating,date.today())
                    
                    #pprint(check_sql_string(query, data))
                    
                    try:
                        # update
                        cursor = conn.cursor()
                        cursor.execute(query, data)
                        # accept the changes
                        conn.commit()
                        pprint(str("tft_league_ranked: ")+summoner_ranked['summonerName'])

                    except Error as error:
                        print(error)

                    finally:
                        cursor.close()

                else:
                    
                    pprint("!!! NEW queue Type !!!")
                    pprint(summoner_data)
                    break

    def addmatches(self):
        #get all the summoner ids
        query = """SELECT puuid FROM tft_summoner"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for puuid in results:
            puuid=''.join(puuid)
            time.sleep(2)
            #pprint(puuid)
            #https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/nqc05hR8dIWltj352vriRHbhrQSwWqM8gLr-6IW_IXHoTqA
            r = requests.get(str('https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/' +puuid+'/ids?count=20'), headers=TFTheaders)
            matchlist=r.json()
            
            #Does the summoner plays TFT at all ?
            if matchlist == []:
                #pprint("empy: "+puuid)
                continue

            if 'status' in matchlist:
                pprint(matchlist)
                time.sleep(500)

            #pprint(matchlist)
            for match in matchlist:
                #From all matches, only request the unknown ones
                query="""SELECT match_id FROM tft_matches WHERE match_id = %s AND tft_set_number > 0"""
                cursor = conn.cursor()
                #pprint(check_sql_string(query, (match, )))
                cursor.execute(query,(match, ))
                results=cursor.fetchall()
                #pprint(results)

                #unknown one
                if (match,) in results:
                    pprint(match)
                    pprint("is already in the DB")
                    continue
                else:
                    pprint(match)
                    #tft_matches fill
                    time.sleep(2)
                    #https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/nqc05hR8dIWltj352vriRHbhrQSwWqM8gLr-6IW_IXHoTqA
                    r = requests.get(str('https://europe.api.riotgames.com/tft/match/v1/matches/' +match), headers=TFTheaders)
                    thismatch=r.json()
                    #pprint(thismatch)
                    for thisparticipant in thismatch['info']['participants']:
                        #pprint(thisparticipant)
                        game_datetime = time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime(thismatch['info']['game_datetime']/1000.))
                        query = """ REPLACE INTO tft_matches (match_id, game_datetime, game_length, game_version, participant_puuid, gold_left, 
                        last_round, level, placement, players_eliminated, time_eliminated, total_damage_to_players, json_data, queue_id, tft_set_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                        
                        if 'players_eliminated' not in thisparticipant:
                            pprint(thisparticipant)
                            thisparticipant['players_eliminated']=thisparticipant['players_eliminated ']
                            time.sleep(2)
                        
                        
                        data = (thismatch['metadata']['match_id'],game_datetime,thismatch['info']['game_length'], thismatch['info']['game_version'], thisparticipant['puuid'], 
                        thisparticipant['gold_left'],thisparticipant['last_round'], thisparticipant['level'], thisparticipant['placement'], thisparticipant['players_eliminated'], 
                         thisparticipant['time_eliminated'], thisparticipant['total_damage_to_players'], json.dumps(thisparticipant), thismatch['info']['queue_id'], thismatch['info']['tft_set_number'])
                        try:
                            # update
                            cursor = conn.cursor()
                            cursor.execute(query, data)
                            # accept the changes
                            conn.commit()
                            pprint(str("adding match: ")+match)

                        except Error as error:
                            print(error)

                        finally:
                            cursor.close()

def main():

    team =     [
    "Le Jer","Rick Kirck","NarNic","MrBambou","MarleyKings",
    "IkBenTrunken","MaziTFT","Chris Staline",
    "leborouxdescoeur","Wialaë","Cartuosoruse","Margoul1n",
    "Ives côtede porc","efasten","h0llyztw","Crilik",
    "nesuw","shröding3r","Carlòtta","wissvalere","yatan",
    "yataan","NarNic","Langelus83","ADCovayn19",
    "Synanai","twittmann","twittmannx",
    "Forddead","ExÖtiik Giirl","Gilbert","ChMeunou",
    "SushiKali","Orodeluna","Moroes","WBlade ll","Shinjow",
    "Αrva","Cfordead","siournayme"
    ]

    job = masterdata()
    #job.addsummoner(team)
    job.addleague()
    time.sleep(1)
    job.addmatches()


if __name__ == "__main__":
    main()
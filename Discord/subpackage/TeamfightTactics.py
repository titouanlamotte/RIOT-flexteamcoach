
import time
from datetime import date
from pprint import pprint

from mysql.connector import Error
from random import randint
import json

import Consummer
import secrets
from databases import *

class masterdata:
    cursor = conn.cursor()

    def addleague(self):
        #get all the summoner ids from TFT
        query = """SELECT summonerId FROM (
        SELECT summonerId FROM tft_league_ranked 
        UNION ALL  
        SELECT summonerId FROM tft_league_ranked_turbo
        ) as t GROUP BY summonerId"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for summ in results:
            summ=''.join(summ)
            time.sleep(2)
            #https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/*
            r = Consummer.getcall(str('https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/' +summ), secrets.TFTheaders)
            #pprint(r)
            if r == False:
                continue
            else:
                summoner=r.json()
                
                #Does the summoner plays TFT at all ?
                if summoner == []:
                    continue

                if 'status' in summoner:
                    pprint(summoner)
                    time.sleep(60)


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

    def addleaguepairs(self):
        #get all the summoner ids from LOL to retreive the ranked_pairs
        query = """SELECT summonerId FROM tft_league_ranked_pairs GROUP BY summonerId;"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for summ in results:
            summ=''.join(summ)
            time.sleep(2)
            #https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/*
            r = Consummer.getcall(str('https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/by-summoner/' +summ), secrets.LOLheaders)
            #pprint(r)
            if r == False:
                continue
            else:
                summoner=r.json()
                
                #Does the summoner plays at all ?
                if summoner == []:
                    continue

                if 'status' in summoner:
                    pprint(summoner)
                    time.sleep(60)


                for summoner_data in summoner:
                    if summoner_data["queueType"]=="RANKED_TFT_DOUBLE_UP":#RANKED_TFT_DOUBLE_UP old RANKED_TFT_PAIRS
                        #THIS IS A TFT RANKED QUEUE COMING FROM THE LOL API ?!
                        summoner_ranked=summoner_data
                        #tft_league_ranked
                        
                        Tiers_LP_values={"IRON":0,"BRONZE":400,"SILVER":800,"GOLD":1200,"PLATINUM":1600,"DIAMOND":2000,"MASTER":2400,"GRANDMASTER":2400,"CHALLENGER":2400}
                        tftrank_LP_values={"IV":0,"III":100,"II":200,"I":300}
                        CalcRating = Tiers_LP_values[summoner_ranked['tier']] + tftrank_LP_values[summoner_ranked['rank']] +summoner_ranked['leaguePoints']
                        CalcRating = summoner_ranked['leaguePoints']
                        #tiertft = summoner_ranked['leaguePoints']
                        summoner_ranked['leagueId'] = "RANKED_TFT_DOUBLE_UP"
                        #summoner_ranked['rank'] = summoner_ranked['leaguePoints']

                        query = """ REPLACE INTO tft_league_ranked_pairs (summonerId, summonerName, leagueId, queueType, tier, tftrank, leaguePoints, wins, losses, veteran, IsInactive, freshBlood, hotStreak, CalcRating, LastUpdateDate) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                        data = (summoner_ranked['summonerId'],summoner_ranked['summonerName'],summoner_ranked['leagueId'],summoner_ranked['queueType'],summoner_ranked['tier'],summoner_ranked['rank'],
                        summoner_ranked['leaguePoints'],summoner_ranked['wins'],summoner_ranked['losses'],str(summoner_ranked['veteran']),str(summoner_ranked['inactive']),str(summoner_ranked['freshBlood']),str(summoner_ranked['hotStreak']), CalcRating,date.today())
                        
                        
                        try:
                            # update
                            cursor = conn.cursor()
                            cursor.execute(query, data)
                            # accept the changes
                            conn.commit()
                            pprint(str("tft_league_ranked_pairs: ")+summoner_ranked['summonerName'])

                        except Error as error:
                            print(error)

                        finally:
                            cursor.close()


def main():

    job = masterdata()

if __name__ == "__main__":
    main()
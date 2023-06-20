
import time
from datetime import date
from pprint import pprint


from random import randint
import json

import Consummer
import secrets
from databases import *


class masterdata:
    cursor = conn.cursor()

    def addleague(self):
        #get all the summoner ids
        query = """SELECT id FROM lol_summoner"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for summ in results:
            summ=''.join(summ)
            time.sleep(2)
            #https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/*
            r = Consummer.getcall(str('https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' +summ), secrets.LOLheaders)
            if r == False:
                continue
            summoner=r.json()

            for summoner_data in summoner:

                if summoner_data["queueType"]=="RANKED_FLEX_SR":
                    summoner_ranked=summoner_data
                    #lol_league_ranked_solo
                    
                    Tiers_LP_values={"IRON":0,"BRONZE":400,"SILVER":800,"GOLD":1200,"PLATINUM":1600,"DIAMOND":2000,"MASTER":2400,"GRANDMASTER":2400,"CHALLENGER":2400}
                    tftrank_LP_values={"IV":0,"III":100,"II":200,"I":300}
                    CalcRating = Tiers_LP_values[summoner_ranked['tier']] + tftrank_LP_values[summoner_ranked['rank']] +summoner_ranked['leaguePoints']

                    query = """ REPLACE INTO lol_league_ranked_flex (summonerId, summonerName, leagueId, queueType, tier, lolrank, leaguePoints, wins, losses, veteran, IsInactive, freshBlood, hotStreak, CalcRating, LastUpdateDate) 
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
                        pprint(str("lol_league_ranked_solo: ")+summoner_ranked['summonerName'])

                    except Error as error:
                        print(error)

                    finally:
                        cursor.close()

                elif summoner_data["queueType"]=="RANKED_TFT_PAIRS":
                    #THIS IS A TFT RANKED QUEUE COMING FROM THE LOL API ?!
                    summoner_ranked=summoner_data
                    #tft_league_ranked
                    
                    Tiers_LP_values={"IRON":0,"BRONZE":400,"SILVER":800,"GOLD":1200,"PLATINUM":1600,"DIAMOND":2000,"MASTER":2400,"GRANDMASTER":2400,"CHALLENGER":2400}
                    tftrank_LP_values={"IV":0,"III":100,"II":200,"I":300}
                    #CalcRating = Tiers_LP_values[summoner_ranked['tier']] + tftrank_LP_values[summoner_ranked['rank']] +summoner_ranked['leaguePoints']
                    CalcRating = summoner_ranked['leaguePoints']
                    tiertft = summoner_ranked['leaguePoints']
                    summoner_ranked['leagueId'] = "RANKED_TFT_PAIRS"
                    summoner_ranked['rank'] = summoner_ranked['leaguePoints']

                    query = """ REPLACE INTO tft_league_ranked_pairs (summonerId, summonerName, leagueId, queueType, tier, tftrank, leaguePoints, wins, losses, veteran, IsInactive, freshBlood, hotStreak, CalcRating, LastUpdateDate) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                    data = (summoner_ranked['summonerId'],summoner_ranked['summonerName'],summoner_ranked['leagueId'],summoner_ranked['queueType'],tiertft,summoner_ranked['rank'],
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


                elif summoner_data["queueType"]=="RANKED_SOLO_5x5":
                    summoner_ranked=summoner_data
                    #lol_league_ranked_solo
                    
                    Tiers_LP_values={"IRON":0,"BRONZE":400,"SILVER":800,"GOLD":1200,"PLATINUM":1600,"DIAMOND":2000,"MASTER":2400,"GRANDMASTER":2400,"CHALLENGER":2400}
                    tftrank_LP_values={"IV":0,"III":100,"II":200,"I":300}
                    CalcRating = Tiers_LP_values[summoner_ranked['tier']] + tftrank_LP_values[summoner_ranked['rank']] +summoner_ranked['leaguePoints']

                    query = """ REPLACE INTO lol_league_ranked_solo (summonerId, summonerName, leagueId, queueType, tier, lolrank, leaguePoints, wins, losses, veteran, IsInactive, freshBlood, hotStreak, CalcRating, LastUpdateDate) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                    data = (summoner_ranked['summonerId'],summoner_ranked['summonerName'],summoner_ranked['leagueId'],summoner_ranked['queueType'],summoner_ranked['tier'],summoner_ranked['rank'],
                    summoner_ranked['leaguePoints'],summoner_ranked['wins'],summoner_ranked['losses'],str(summoner_ranked['veteran']),str(summoner_ranked['inactive']),str(summoner_ranked['freshBlood']),str(summoner_ranked['hotStreak']), CalcRating,date.today())
                    
                    
                    try:
                        # update
                        cursor = conn.cursor()
                        cursor.execute(query, data)
                        # accept the changes
                        conn.commit()
                        pprint(str("lol_league_ranked_solo: ")+summoner_ranked['summonerName'])

                    except Error as error:
                        print(error)

                    finally:
                        cursor.close()

                else:
                    
                    pprint("!!! NEW queue Type !!!")
                    pprint(summoner_data)
                    break



def main():

    job = masterdata()
    #job.addsummoner()

if __name__ == "__main__":
    main()
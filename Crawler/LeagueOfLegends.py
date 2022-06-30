
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

    def champions(self):
        #https://ddragon.leagueoflegends.com/cdn/10.15.1/data/en_US/champion.json
        r = Consummer.getcall('http://ddragon.leagueoflegends.com/cdn/10.15.1/data/en_US/champion.json','')
        if r == False:
            return 0
        champs=r.json()
        for d in champs['data']:
            cursor = conn.cursor()
            #champs['data'][d]['_id']=int(champs['data'][d]['key'])
            #champs['data'][d]['key']=int(champs['data'][d]['_id'])
            try:
                #pprint(json.dumps(champs['data'][d]['stats']))
                query = """ REPLACE INTO lol_champions (Ckey, version, Cname, title, blurb, info_attack, info_defense, info_magic, info_difficulty, image, partype, stats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                data = (champs['data'][d]['key'], champs['data'][d]['version'],champs['data'][d]['name'],champs['data'][d]['title'],champs['data'][d]['blurb'],
                champs['data'][d]['info']['attack'],champs['data'][d]['info']['defense'],champs['data'][d]['info']['magic'],champs['data'][d]['info']['difficulty'],
                json.dumps(champs['data'][d]['image']),champs['data'][d]['partype'],json.dumps(champs['data'][d]['stats']))
                cursor = conn.cursor()
                #pprint(check_sql_string(query, data))
                cursor.execute(query, data)
                
                # accept the changes
                conn.commit()               
            except Error as error:
                print(error)

            finally:
                cursor.close()  

            #Champions_tags
            for t in champs['data'][d]['tags']:
                try:
                    query = """ REPLACE INTO lol_champions_tags (Ckey, tag) VALUES (%s, %s) """
                    data = (champs['data'][d]['key'], t)
                    cursor = conn.cursor()
                    cursor.execute(query, data)
                    # accept the changes
                    conn.commit()               
                except Error as error:
                    print(error)

                finally:
                    cursor.close()

            pprint(d)


    def queues(self):
        #https://static.developer.riotgames.com/docs/lol/queues.json
        r = Consummer.getcall('https://static.developer.riotgames.com/docs/lol/queues.json','')
        if r == False:
            return 0
        champs=r.json()
        for d in champs:
            #d['_id']=d['queueId']
            try:
                query = """ REPLACE INTO lol_queues (queueId, map, description, notes) VALUES (%s, %s, %s, %s) """
                data = (d['queueId'],d['map'],d['description'],d['notes'])
                cursor = conn.cursor()
                cursor.execute(query, data)
                # accept the changes
                conn.commit()               
            except Error as error:
                print(error)

            finally:
                cursor.close()


            #pprint(d)

    def items(self):
        #https://ddragon.leagueoflegends.com/cdn/10.15.1/data/en_US/item.json
        return 0

    def addsummoner(self):
        #get all the summoner ids
        query = """SELECT summoner FROM vinrougegamingsummoner;"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for summ in results:
            summ=''.join(summ)
            time.sleep(2)
            # https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/*
            # _id is the summoner Id for other endpoints. Nothing to do with accountId!
            r = Consummer.getcall(str('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' +summ), secrets.LOLheaders)
            if r == False:
                continue
            query = """ REPLACE INTO lol_summoner
            (accountId, id, name, profileIconId, puuid, revisionDate, summonerLevel)
            VALUES 
            (%s, %s, %s, %s, %s, %s,%s) """
            summoner=r.json()
            #summoner["_id"]=summoner["id"]
            if "id" in summoner:
                #epoch to datetime
                RevDate= time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime(summoner["revisionDate"]/1000.))
                data = (summoner['accountId'],summoner['id'],summoner['name'],summoner['profileIconId'],summoner['puuid'],RevDate,summoner['summonerLevel'],)
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

    def addmatches(self):
        #get all the matches for all our puuids
        query = """SELECT puuid FROM lol_summoner"""
        cursor = conn.cursor()
        cursor.execute(query)
        results=cursor.fetchall()

        for puuid in results:
            puuid=''.join(puuid)
            time.sleep(2)
            #https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/*/ids?start=0&count=100
            r = Consummer.getcall(str('https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+'/ids?start=0&count=100'), secrets.LOLheaders)
            if r == False:
                continue
            
            matches=r.json()


            for thismatch in matches:

                query = """SELECT matchId FROM lol_match_v5"""
                cursor = conn.cursor()
                cursor.execute(query)
                results=cursor.fetchall()
                if any(thismatch == item[0] for item in results):
                    pprint('match: '+thismatch+' already in DB')
                    continue
                    
                else:
                    query = """SELECT matchId FROM lol_match_v5_errors"""
                    cursor = conn.cursor()
                    cursor.execute(query)
                    results=cursor.fetchall()
                    if any(thismatch == item[0] for item in results):
                        pprint('match: '+thismatch+' already in keyerrors DB')
                        continue
        
                    else:
                        self.addthismatch(thismatch)

    def addthismatch(self, matchid):
        #https://europe.api.riotgames.com/lol/match/v5/matches/*
        r = Consummer.getcall(str('https://europe.api.riotgames.com/lol/match/v5/matches/'+matchid), secrets.LOLheaders)
        time.sleep(3)
        if r == False:
            return 0
        thisMatch=r.json()

        if 'info' not in thisMatch:
            query = """REPLACE INTO lol_match_v5_keyerror (matchId, jsondata) VALUES (%s, %s, %s)"""
            data = (matchid,json.dumps(thisMatch))
            try:
                # update
                cursor = conn.cursor()
                cursor.execute(query, data)
                # accept the changes
                conn.commit()
                pprint(str("lol_match_v5_keyerrors: ")+matchid)

            except Error as error:
                print(error)

            finally:
                cursor.close()
                
        else:
            pprint(matchid)
            query = """ REPLACE INTO lol_match_v5 (gameId, matchId, dataVersion, puuids, gameCreation, gameDuration, gameEndTimestamp, gameMode, gameName, gameStartTimestamp, 
            gameType, gameVersion, mapId, participants) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """


            gameCreation= time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime(thisMatch['info']["gameCreation"]/1000.))

            if 'gameEndTimestamp' in thisMatch['info']:
                gameEndTimestamp= time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime(thisMatch['info']["gameEndTimestamp"]/1000.))
            else:
                gameEndTimestamp = 0

            if 'gameEndTimestamp' in thisMatch['info']: 
                gameStartTimestamp= time.strftime("%Y-%m-%d %H:%M:%S",  time.gmtime(thisMatch['info']["gameStartTimestamp"]/1000.))
            else:
                gameStartTimestamp = 0

            data = (thisMatch['info']['gameId'],thisMatch['metadata']['matchId'],thisMatch['metadata']['dataVersion'],json.dumps(thisMatch['metadata']['participants']),gameCreation,
            thisMatch['info']['gameDuration'],gameEndTimestamp,thisMatch['info']['gameMode'],thisMatch['info']['gameName'], gameStartTimestamp, thisMatch['info']['gameType'],
            thisMatch['info']['gameVersion'], thisMatch['info']['mapId'], json.dumps(thisMatch['info']['participants']))
            
            
            try:
                # update
                cursor = conn.cursor()
                cursor.execute(query, data)
                # accept the changes
                conn.commit()
                pprint(str("lol_match_v5: ")+matchid)

            except Error as error:
                print(error)

            finally:
                cursor.close()


def main():

    job = masterdata()
    job.addsummoner()
    #job.queues()
    #job.addleague()
    #job.addmatches()

if __name__ == "__main__":
    main()
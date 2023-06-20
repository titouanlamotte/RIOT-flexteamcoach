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

    def readdata(self):
        try:
            f = open("players_file.json", "r")
            # Do something with the file
        except IOError:
            print("File not accessible")
            #[
            #{"@Discord#0001":"LeagueOfLegendorTFT1"},
            #{"@Discord#0002":"LeagueOfLegendorTFT2"}
            #]
            #
        finally:
            f.close()

    def addplayers(self):
        #get all the summoner ids
        query = """SELECT id FROM tft_summoner"""
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

def main():

    job = masterdata()
    time.sleep(1)
    job.addplayers()


if __name__ == "__main__":
    main()
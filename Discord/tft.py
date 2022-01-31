# -*- coding: utf-8 -*-

from xml.sax.saxutils import prepare_input_source
import discord
from discord.ext import commands, tasks
from datetime import datetime
import requests
from datetime import date
from pprint import pprint
import html2text


from secrets import *
from databases import *
   
class tft(commands.Cog):
    def __init__(self, client):
        self.client = client
   
   
   
    @tasks.loop(hours=3)
    async def batch_tft_match(self):
        try:
            await tft.TFT()
            print("TFT Batch success")
        except Exception as e:
            print(f"TFT Batch Error {e}")



    @commands.command(pass_context=True, brief='!TFT 🍻', description='')
    async def TFT(self, ctx):
        embedVar = discord.Embed(title="⚔️ Teamfight Tactics ranking", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        pprint("!TFT") 
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.*
                FROM (
                    SELECT summonerId, MAX(LastUpdateDate) as MaxTime
                    FROM tft_league_ranked
                    GROUP BY summonerId
                ) r
                INNER JOIN tft_league_ranked s
                ON s.summonerId = r.summonerId AND s.LastUpdateDate = r.MaxTime
                ORDER BY s.CalcRating DESC"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data=cursor.fetchall()

        #Text format data
        count = 0
        rankings={1:'🥇',2:'🥈',3:'🥉',4:''}
        tiers={"IRON":"<:Season_2022_1_Iron:931897114257154068>","BRONZE":"<:Season_2022_2_Bronze:931897121446166579>","SILVER":"<:Season_2022_3_Silver:931897130925318224>",
        "GOLD":"<:Season_2022_4_Gold:931897140136013884>","PLATINUM":"<:Season_2022_5_Platinum:931897148520431696>","DIAMOND":"<:Season_2022_6_Diamond:931897156481204236>",
        "MASTER":"<:Season_2022_7_Master:931897166019051565>","GRANDMASTER":"<:Season_2022_8_Grandmaster:931897175150051479>",
        "CHALLENGER":"<:Season_2022_9_Challenger:931897186571145216>"}

        for d in data:
            #rankings counter
            count = count+1
            if count > 4:
                count = 4
            embedVar.add_field(name=str(str(tiers[d['tier']])+" "+d['summonerName']+" "+rankings[count]), value=str(d['tier'][0]+". "+d["tftrank"]+" "+str(str(d['leaguePoints'])+" LP")), inline=True)


        await ctx.send(embed=embedVar)


    @commands.command(pass_context=True, brief='!TFT 🍻', description='')
    async def TFT_TURBO(self, ctx):
        embedVar = discord.Embed(title="⚔️ Teamfight Tactics Turbo ranking", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        pprint("!Turbo") 
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM tft_league_ranked_tft_turbo ORDER BY ratedRating DESC"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data=cursor.fetchall()
        pprint(data)
        #Text format data
        count = 0
        rankings={1:'🥇',2:'🥈',3:'🥉',4:''}
        tiers={"GRAY":"<:TFT_Hyper_Roll_1Grey:932250917066129449>","GREEN":"<:TFT_Hyper_Roll_2Green:932250917317783602>","BLUE":"<:TFT_Hyper_Roll_3Blue:932250917393268806>",
        "PURPLE":"<:TFT_Hyper_Roll_4Purple:932250917594607646>","HYPER":"<:TFT_Hyper_Roll_5Hyper:932250917586214932>"}

        for d in data:
            #rankings counter
            count = count+1
            if count > 4:
                count = 4
            embedVar.add_field(name=str(str(tiers[d['ratedTier']])+" "+d['summonerName']+" "+rankings[count]), value=str(d['ratedTier']+" "+str(str(d['ratedRating'])+" LP")), inline=True)


        await ctx.send(embed=embedVar)


def setup(client):
    client.add_cog(tft(client))
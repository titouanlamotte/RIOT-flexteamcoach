# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
from datetime import date
from pprint import pprint

from secrets import *
from databases import *

from subpackage import *

class tft(commands.Cog):
    def __init__(self, client):
        self.client = client
        # For Tasks
        self.index = 0
        #self.bot = bot
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.index)
        self.index += 1

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

        
    @tasks.loop(hours=10)
    async def batch_tft_match_top8(self, ctx):
        try:
            #await tft.TFT()
            #select m.game_datetime, m.gold_left, s.name from tft_matches m INNER JOIN tft_summoner s ON s.puuid= m.participant_puuid WHERE m.game_datetime >= DATE_SUB(NOW(),INTERVAL 1 YEAR) AND m.placement = 8;
            cursor = conn.cursor(dictionary=True)
            query = """
                    select m.game_datetime, m.gold_left, s.name from tft_matches m 
                    INNER JOIN tft_summoner s ON s.puuid= m.participant_puuid 
                    WHERE m.game_datetime >= DATE_SUB(NOW(),INTERVAL 10 HOURS) 
                    AND m.placement = 8;
                    """
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            data=cursor.fetchall()
            if data.length() > 0:
                embedVarTop8 = discord.Embed(title="🤔 Teamfight Tactics TOP 8 of yesterday", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff) 
                for d in data:
                    embedVarTop8.add_field(name=str(), value=str(), inline=True)
                #send message into the TFT channel
                channel = discord.utils.get(ctx.guild.channels, name="")
                channel_id = channel.id
                await ctx.send(embed=embedVarTop8)

            else:
                print("no top8")
                pprint(data)

        except Exception as e:
            print(f"TFT Batch Error {e}")


    @commands.command(pass_context=True, brief='!TFT 🍻', description='')
    async def TFT(self, ctx):
        subpackage.Runner.job.addleague()
        subpackage.Runner.job.addleaguepairs()
        #TFT SOLO QUEUE
        embedVar = discord.Embed(title="⚔️ Teamfight Tactics SoloQ rankings", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff) 
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.*
                FROM (
                    SELECT MAX(LastUpdateDate) as MaxTime
                    FROM tft_league_ranked LIMIT 1
                ) r
                INNER JOIN tft_league_ranked s
                ON s.LastUpdateDate = r.MaxTime
                ORDER BY s.CalcRating+0 DESC"""
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
      
        tiersdisplay={"IRON":"Ir","BRONZE":"Br","SILVER":"Si","GOLD":"Go","PLATINUM":"Pl","DIAMOND":"Di","MASTER":"Ma","GRANDMASTER":"GM","CHALLENGER":"CH"}
        
        #rankings gen
        for d in data:
            #rankings counter
            count = count+1
            if count > 4:
                count = 4
            embedVar.add_field(name=str(str(tiers[d['tier']])+" "+d['summonerName']+" "+rankings[count]), value=str(tiersdisplay[d['tier']]+". "+d["tftrank"]+" "+str(str(d['leaguePoints'])+" LP")), inline=True)


        #TFT TURBO
        embedVarTurbo = discord.Embed(title="⚔️ Teamfight Tactics Turbo rankings", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.*
                FROM (
                    SELECT MAX(LastUpdateDate) as MaxTime
                    FROM tft_league_ranked_turbo
                ) r
                INNER JOIN tft_league_ranked_turbo s
                ON s.LastUpdateDate = r.MaxTime
                ORDER BY s.ratedRating+0 DESC"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data=cursor.fetchall()
        #Text format data
        count = 0
        rankings={1:'🥇',2:'🥈',3:'🥉',4:''}
        tiers={"GRAY":"<:TFT_Hyper_Roll_1Grey:932250917066129449>","GREEN":"<:TFT_Hyper_Roll_2Green:932250917317783602>","BLUE":"<:TFT_Hyper_Roll_3Blue:932250917393268806>",
        "PURPLE":"<:TFT_Hyper_Roll_4Purple:932250917594607646>","ORANGE":"<:TFT_Hyper_Roll_5Hyper:932250917586214932>"}
        #rankings gen
        for d in data:
            #HYPER is stored as ORANGE in the API
            if d['ratedTier'] == 'ORANGE':
                d['DisplayTier'] = 'HYPER'
            else:
               d['DisplayTier'] = d['ratedTier']
            #rankings counter
            count = count+1
            if count > 4:
                count = 4
            embedVarTurbo.add_field(name=str(str(tiers[d['ratedTier']])+" "+d['summonerName']+" "+rankings[count]), value=str(d['DisplayTier']+" "+str(str(d['ratedRating'])+" LP")), inline=True)
        
        #PAIRS/DUO
        embedVarDuo = discord.Embed(title="⚔️ Teamfight Tactics DUO rankings", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.*
                FROM (
                    SELECT summonerId, MAX(LastUpdateDate) as MaxTime
                    FROM tft_league_ranked_pairs
                    GROUP BY summonerId
                ) r
                INNER JOIN tft_league_ranked_pairs s
                ON s.summonerId = r.summonerId AND s.LastUpdateDate = r.MaxTime
                ORDER BY s.CalcRating DESC"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data=cursor.fetchall()

        #Text format data
        count = 0
        rankings={1:'🥇',2:'🥈',3:'🥉',4:''}
        tiers={"IRON":"<:S2022_1_Iron:931897114257154068>","BRONZE":"<:S2022_2_Bronze:931897121446166579>","SILVER":"<:S2022_3_Silver:931897130925318224>",
        "GOLD":"<:S2022_4_Gold:931897140136013884>","PLATINUM":"<:S2022_5_Platinum:931897148520431696>","DIAMOND":"<:S2022_6_Diamond:931897156481204236>",
        "MASTER":"<:S2022_7_Master:931897166019051565>","GRANDMASTER":"<:S2022_8_Grandmaster:931897175150051479>",
        "CHALLENGER":"<:S2022_9_Challenger:931897186571145216>"}

        for d in data:
            #rankings counter
            count = count+1
            if count > 4:
                count = 4
            embedVarDuo.add_field(name=str(str(tiers[d['tier']])+" "+d['summonerName']+" "+rankings[count]), value=str(d['tier'][0]+". "+d["tftrank"]+" "+str(str(d['leaguePoints'])+" LP")), inline=True)
        
        #send message
        await ctx.send(embed=embedVar)
        await ctx.send(embed=embedVarTurbo)
        await ctx.send(embed=embedVarDuo)




def setup(client):
    client.add_cog(tft(client))

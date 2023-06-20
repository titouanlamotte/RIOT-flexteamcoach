# -*- coding: utf-8 -*-

import discord
from discord.ext import commands

from datetime import date
import requests
from pprint import pprint
import html2text
from databases import *

#from LeagueOfLegends import *



#requests user agent for https://dev.whatismymmr.com/
mmrheaders = {
    'User-Agent': 'Discordapp.com:FlexTeam-Coach:0.1.20200729',
    'From': 'Made with love & beer in Frankfurt'
}




class lol(commands.Cog):
    def __init__(self, client):
        self.client = client


    # https://euw.whatismymmr.com/api/v1/summoner?name=nesuw
    @commands.command(pass_context=True, brief='!mmr summoner 🍻 Display mmr from whatismymmr.com', description='!mmr summoner 🍻 Display mmr from whatismymmr.com')
    async def mmr(self, ctx, summoner=""):

        r = requests.get(str('https://euw.whatismymmr.com/api/v1/summoner?name=' +summoner), headers=mmrheaders)
        r.json()
        #pprint(r.json())
        if r.json()["ranked"]["avg"] is None:
            await ctx.send(summoner + " not found on whatismymmr.com" + "\n" +  "No recent solo games to analyze")
        else:
            await ctx.send(summoner + " on whatismymmr.com:  " + str(r.json()["ranked"]["avg"]))
            await ctx.send(html2text.html2text(r.json()["ranked"]["summary"]))


    @commands.command(pass_context=True, brief='!lol_count_games 🍻', description='')
    async def lol_count_games(self, ctx):
        embedVar = discord.Embed(title="LoL game spammer 😮", description="LoL games played by summoner: all queues", color=0x00ffff)
        #embedVar.add_field(name="Field1", value="hi", inline=False)
        #embedVar.add_field(name="Field2", value="hi2", inline=False)
        #work = LeagueOfLegends.lolanalysis()
        #data=work.countallgames()
        data=[]
        count = 0

        for d in data:
            if count == 0:
                count = 1
                #print("🥇 " + str(d['csum'])+ " games for  " + str(d['_id']['name'][0]))
                embedVar.add_field(name=str("🥇 " + str(d['_id']['name'][0])), value=str(d['csum']), inline=True)
            elif count == 1:
                count = 2
                #print("🥈 " + str(d['csum'])+ " games for  " + str(d['_id']['name'][0]))
                embedVar.add_field(name=str("🥈 " + str(d['_id']['name'][0])), value=str(d['csum']), inline=True)
            elif count == 2:
                count = 3
                #print("🥉 " + str(d['csum'])+ " games for  " + str(d['_id']['name'][0]))
                embedVar.add_field(name=str("🥉 " + str(d['_id']['name'][0])), value=str(d['csum']), inline=True)
            else:
                #print(str(d['csum'])+ " games for  " + str(d['_id']['name'][0]))
                embedVar.add_field(name=str(d['_id']['name'][0]), value=str(d['csum']), inline=True)

        await ctx.send(embed=embedVar)

    @commands.command(pass_context=True, brief='!lol_count_masteries 🍻', description='')
    async def lol_count_masteries(self, ctx):
        embedVar = discord.Embed(title="Our LoL best champions 🍻", description="LoL masteries for all of us", color=0xff00ff)
        #work = LeagueOfLegends.lolanalysis()
        #data=work.allmasteries()
        data=[]
        count = 0
        
        for d in data:
            if count == 0:
                count = 1
                #print("🥇 " 
                embedVar.add_field(name=str("🥇 " + str(d['_id']['champion'][0])), value=str('level=' + str(d['sum_level']) + ' | points=' + str(d['sum_points'])), inline=True)
            elif count == 1:
                count = 2
                #print("🥈 " 
                embedVar.add_field(name=str("🥈 " + str(d['_id']['champion'][0])), value=str('level=' + str(d['sum_level']) + ' | points=' + str(d['sum_points'])), inline=True)
            elif count == 2:
                count = 3
                #print("🥉 " 
                embedVar.add_field(name=str("🥉 " + str(d['_id']['champion'][0])), value=str('level=' + str(d['sum_level']) + ' | points=' + str(d['sum_points'])), inline=True)
            else:
                count = count+1
                #print
                embedVar.add_field(name=str(d['_id']['champion'][0]), value=str('level=' + str(d['sum_level']) + ' | points=' + str(d['sum_points'])), inline=True)
                if count == 21:
                    await ctx.send(embed=embedVar)


    @commands.command(pass_context=True, brief='!lol_best_masteries 🍻', description='')
    async def lol_best_masteries(self, ctx):
        embedVar = discord.Embed(title="LoL best champion levels🍻", description="ChampionPoints by Summoner by Champion", color=0xff3388)
        #work = LeagueOfLegends.lolanalysis()
        #data=work.indiv_champ_allmasteries()
        data=[]
        count = 0
        
        for d in data:
            if count == 0:
                count = 1
                #print("🥇 " 
                embedVar.add_field(name=str("🥇 " + str(d['you'][0])), value=str(str(d['champion'][0]) + ': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
            elif count == 1:
                count = 2
                #print("🥈 " 
                embedVar.add_field(name=str("🥈 " + str(d['you'][0])), value=str(str(d['champion'][0]) + ': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
            elif count == 2:
                count = 3
                #print("🥉 " 
                embedVar.add_field(name=str("🥉 " + str(d['you'][0])), value=str(str(d['champion'][0]) + ': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
            else:
                #print
                embedVar.add_field(name=str((d['you'][0])), value=str(str(d['champion'][0]) + ': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
 
        await ctx.send(embed=embedVar)

    @commands.command(pass_context=True, brief='!lol_XP_masteries 🍻', description='')
    async def lol_XP_masteries(self, ctx):
        embedVar = discord.Embed(title="Masteries XP by player🍻", description="Masteries XP by Summoner", color=0xff3388)
        #work = LeagueOfLegends.lolanalysis()
        #data=work.indiv_XP_allmasteries()
        data =[]
        count = 0
        
        for d in data:
            if count == 0:
                count = 1
                #print("🥇 " 
                embedVar.add_field(name=str("🥇 " + str(d['_id']['you'][0])), value=str(': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
            elif count == 1:
                count = 2
                #print("🥈 " 
                embedVar.add_field(name=str("🥈 " + str(d['_id']['you'][0])), value=str(': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
            elif count == 2:
                count = 3
                #print("🥉 " 
                embedVar.add_field(name=str("🥉 " + str(d['_id']['you'][0])), value=str(': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
            else:
                #print
                embedVar.add_field(name=str((d['_id']['you'][0])), value=str(': ' + str(d['sum_points'])[:-3] + 'k'), inline=True)
 
        await ctx.send(embed=embedVar)



        
    @commands.command(pass_context=True, brief='!CLASH 🍻', description='')
    async def CLASH(self, ctx):
        embedVar = discord.Embed(title="⚔️ NEXT CLASH ⚔️", description="16/01 Clash Tier III starting at 19:30", color=0xFF0000)
        #embedVar.add_field(name="Field1", value="hi", inline=False)
        #embedVar.add_field(name="Field2", value="hi2", inline=False)



        Positions={"SUPPORT":"<:Pos_Support:932233525724327937>","ADC":"<:Pos_ADC:932233528035393596>","MID":"<:Pos_MidLane:932233525879521341>",
        "JUNGLE":"<:Pos_Jungle:932233525854347334>","TOP":"<:Pos_TopLane:932233525929857064>"}


        embedVar.add_field(name=str(Positions['TOP']+" xxx"), value=str('Tier xx'))

        embedVar.add_field(name=str(Positions['JUNGLE']+" xxx"), value=str('Tier xx'))
 
        embedVar.add_field(name=str(Positions['MID']+" xxx"), value=str('Tier xx'))

        embedVar.add_field(name=str(Positions['ADC']+"  xxx"), value=str('Tier xx'))

        embedVar.add_field(name=str(Positions['SUPPORT']+"  xxx"), value=str('Tier xx'))
        embedVar.add_field(name=str("🏆"), value=str("🏆"))

        await ctx.send(embed=embedVar)




    @commands.command(pass_context=True, brief='!LOLRANKED 🍻', description='')
    async def LOL(self, ctx):
        #SOLOQUEUE
        embedVarSolo = discord.Embed(title="⚔️ loL RANKED_SOLO_5x5 ranking", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        pprint("!TFT") 
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.*
                    FROM (
                        SELECT summonerId, MAX(LastUpdateDate) as MaxTime
                        FROM lol_league_ranked_solo
                        GROUP BY summonerId
                    ) r
                    INNER JOIN lol_league_ranked_solo s
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
            embedVarSolo.add_field(name=str(str(tiers[d['tier']])+" "+d['summonerName']+" "+rankings[count]), value=str(d['tier'][0]+". "+d["lolrank"]+" "+str(str(d['leaguePoints'])+" LP")), inline=True)
   
        #FLEXQUEUE
        embedVarFlex = discord.Embed(title="⚔️ loL RANKED_SOLO_FLEX ranking", description=str("as of today: "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        pprint("!LOLRANKED") 
        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.*
                FROM (
                    SELECT summonerId, MAX(LastUpdateDate) as MaxTime
                    FROM lol_league_ranked_flex
                    GROUP BY summonerId
                ) r
                INNER JOIN lol_league_ranked_flex s
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
            embedVarFlex.add_field(name=str(str(tiers[d['tier']])+" "+d['summonerName']+" "+rankings[count]), value=str(d['tier'][0]+". "+d["lolrank"]+" "+str(str(d['leaguePoints'])+" LP")), inline=True)

        await ctx.send(embed=embedVarSolo)  
        await ctx.send(embed=embedVarFlex)


    @commands.command(pass_context=True, brief='!NoSoul 🍻', description='')
    async def NOSOUL(self, ctx):
        embedVar = discord.Embed(title="<:Pos_TopLane:932233525929857064> No Soul", description=str("Someone played teemo Top today 😈  "+str(date.today().strftime("%B %d, %Y"))), color=0x00ffff)
        embedVar.set_image(url="https://cdn.discordapp.com/attachments/739152945647583422/935274836970836048/unknown.png")
        embedVar.add_field(name=str("@Yatan#8321"), value=str("Victory +22 LP"), inline=True)
        await ctx.send(embed=embedVar)


def setup(client):
    client.add_cog(lol(client))
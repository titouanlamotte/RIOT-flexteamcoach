# -*- coding: utf-8 -*-
from pprint import pprint
import discord
from discord.ext import commands
import hashlib


class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    # member has joined
    async def on_member_join(member):
        print(f'{member} has joined the server')

    # member has left
    async def on_member_remove(member):
        print(f'{member} has left the server')


    # clear channel if user = nesuw
    @commands.command(pass_context=True, brief='!clear x 🍻 Delete x messages', description='!clear x 🍻 Delete x messages')
    async def clear(self, ctx, amount=10):
        
        print('clear by '+str(ctx.author))
        CurrentUser= hashlib.sha256(bytes(str(ctx.author), encoding='utf8'))
        #pprint(CurrentUser.hexdigest())
        if CurrentUser.hexdigest() == "3d0ac4dd79f7ad27aa5f0e84af563459b4fe267015e4533e8bbe6d75541ff36a":
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send(f'user {ctx.author} not allowed')


def setup(client):
    client.add_cog(admin(client))
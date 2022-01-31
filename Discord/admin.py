# -*- coding: utf-8 -*-
import discord
from discord.ext import commands



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
        if str(ctx.author) == "Margoul1n#6632":
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send(f'user {ctx.author} not allowed')


def setup(client):
    client.add_cog(admin(client))
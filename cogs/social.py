import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.marry

    @commands.command(pass_context=True)
    async def marry(self, ctx, user: discord.Member):
        """Marries a user to your profile"""
        if ctx.message.author.id == self.bot.user.id:
            return

        self.marry = open('./database/marryeds.csv', 'r')
        self.marry.seek(0)

        for line in self.marry:
            if line.split(',')[0] == str(ctx.message.author.id) and line.split(',')[1].replace('\n', '') == str(user.id):
                return await ctx.send('You are already married to this user.')

        self.marry.close()
        self.marry = open('./database/marryeds.csv', 'a')
        self.marry.write(str(ctx.message.author.id) + ',' + str(user.id) + '\n')
        self.marry.close()
        await ctx.send(ctx.message.author.mention + ' has married ' + user.mention)


    @commands.command(pass_context=True)
    async def divorce(self, ctx, user: discord.Member):
        """Divorces a user from your profile"""
        if ctx.message.author.id == self.bot.user.id:
            return

        self.marry = open('./database/marryeds.csv', 'r')
        self.marry.seek(0)

        for line in self.marry:
            if line.split(',')[0] == str(ctx.message.author.id):
                if line.split(',')[1].replace('\n', '') == str(user.id):
                    self.marry.close()
                    self.marry = open('./database/marryeds.csv', 'w')
                    self.marry.write(line.replace(line.split(',')[1], '0'))
                    self.marry.close()
                    await ctx.send(ctx.message.author.mention + ' has divorced ' + user.mention)
                    return
        await ctx.send('You are not married to this user.')

    @commands.command(pass_context=True)
    async def marrylist(self, ctx):
        """Lists all married users"""
        if ctx.message.author.id == self.bot.user.id:
            return

        self.marry = open('./database/marryeds.csv', 'r')
        self.marry.seek(0)

        embed = discord.Embed(title="Married Users", description="", color=0x00ff00)
        for line in self.marry:
            if line.split(',')[0] == str(ctx.message.author.id):
                embed.add_field(name=line.split(',')[0], value=line.split(',')[1].replace('\n', ''), inline=False)

        await ctx.send(embed=embed)
        self.marry.close()

    


def setup(bot):
    bot.add_cog(Social(bot))
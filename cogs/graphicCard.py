import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime

class GraphicCard(commands.Cog):
    """Graphic Card"""

    def __init__(self, bot):
        self.bot = bot

    # list the best graphic cards prices on www.kabum.com.br
    @commands.command(pass_context=True)
    async def gc_k(self, ctx, *, card: str):
        """List the best graphic cards prices on www.kabum.com.br"""
        try:
            url = "https://www.kabum.com.br/busca?query=" + card + '&page_number=1&page_size=20&facet_filters=&sort=price'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            cards = soup.find_all("div", {"class": "productCard"})
            if cards == []:
                return await ctx.send("```Não foi possível encontrar o card informado.```")

            for card in cards[:5]:
                name = card.find("h2", {"class": "nameCard"}).text
                price = card.find("span", {"class": "priceCard"}).text
                link = card.find("a")['href']
                imageLink = card.find("img", {'class': 'imageCard'})['src']
                embed = discord.Embed(title=name, description=price, color=0x00ff00)
                embed.set_image(url=imageLink)
                embed.add_field(name="Link", value=link)
                embed.set_footer(text="Kabum")
                self.save_price(name, price, link)
                await ctx.send(embed=embed)
        except:
            await ctx.send("```Não foi possível encontrar o card informado.```")


    # list the best graphic cards prices on www.pichau.com.br
    @commands.command(pass_context=True)
    async def gc_p(self, ctx, *, gcard: str):
        """List the best graphic cards prices on www.pichau.com.br"""
        try:
            url = "https://www.pichau.com.br/search?q=" + gcard + '&sort=price-asc'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            cards = soup.find_all("div", {"class": "productCard"})
            if cards == []:
                return await ctx.send("```Não foi possível encontrar o card informado.```")

            for card in cards[:5]:
                name = card.find("h2", {"class": "nameCard"}).text
                price = card.find("span", {"class": "priceCard"}).text
                link = card.find("a")['href']
                imageLink = card.find("img", {'class': 'imageCard'})['src']
                embed = discord.Embed(title=name, description=price, color=0x00ff00)
                embed.set_image(url=imageLink)
                embed.add_field(name="Link", value=link)
                embed.set_footer(text="Pichau")
                self.save_price(name, price, link)
                await ctx.send(embed=embed)

        except:
            await ctx.send("```Não foi possível encontrar o card informado.```")        

    # list best prices on google search
    @commands.command(pass_context=True)
    async def gc_g(self, ctx, *, gcard: str):
        """List the best graphic cards prices on google search"""
        try:
            url = "https://www.google.com.br/search?q=" + gcard + '&tbm=shop'
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            cards = soup.find_all("div", text="R$")
            if cards == []:
                return await ctx.send("```Não foi possível encontrar o card informado.```")

            for card in cards[:5]:
                name = card.find("h3", {"class": "sh-d-i-ttl"}).text
                price = card.find("span", {"class": "sh-d-i-pr"}).text
                link = card.find("a")['href']
                imageLink = card.find("img", {'class': 'sh-d-i-img'})['src']
                embed = discord.Embed(title=name, description=price, color=0x00ff00)
                embed.set_image(url=imageLink)
                embed.add_field(name="Link", value=link)
                embed.set_footer(text="Google")
                self.save_price(name, price, link)
                await ctx.send(embed=embed)

        except:
            await ctx.send("```Não foi possível encontrar o card informado.```")

    def save_price(card, price, url):
        date = datetime.datetime.now()

        with open('./database/prices.csv', 'rw') as file:
            file.write(card + ',' + price + ',' + date + ',' + url)
    

def setup(bot):
    bot.add_cog(GraphicCard(bot))
import discord
import sys

import configparser
from discord.ext import commands
from libs.Meme import Meme
from libs.config_loader import config

class MemeCog(commands.Cog, name="Memes"):
    def __init__(self, client):
        self.client = client
        self.config = config()

    @commands.command(pass_context=True)
    async def reddit(self, ctx, secound:str=None):
        chan  = ctx.message.channel.name
        if self.config.has_option("URLS", "reddit"):
            url = self.config["URLS"]["reddit"]

            get = Meme(url)
            get.run()
            title = str(get.title)
            image = get.image
            channel_name = None
            
            if self.config.has_option("SETTINGS", "meme"):
                channel_name = self.config["SETTINGS"]["meme"]
            if str(chan) == str(channel_name):
                try:
                    embed = discord.Embed(title=title, color=discord.Color.dark_blue())
                    embed.set_image(url=image)
                    await ctx.send(embed=embed)
                except Exception as error:
                    await ctx.send(f"Error : {error}")
            elif channel_name is None:
                try:
                    embed = discord.Embed(title=title, color=discord.Color.dark_blue())
                    embed.set_image(url=image)
                    await ctx.send(embed=embed)
                except Exception as error:
                    await ctx.send(f"Error : {error}")
  
  
def setup(client):
    client.add_cog(MemeCog(client))
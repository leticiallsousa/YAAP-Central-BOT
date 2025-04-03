import discord
from discord.ext import commands
from discord.ui import Button, View
from utils.emojis import emoji

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        synced = await self.client.tree.sync()
        embed = discord.Embed(description=f'{emoji["positive"]} Sincronizados {len(synced)} comandos de app para o servidor atual.', colour=discord.Colour(0x3d6333))
        await ctx.reply(embed=embed, mention_author=False)

async def setup(client):
    await client.add_cog(Owner(client))

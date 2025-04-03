import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
from creator_yaap.embed_creator import EmbedCreator
from utils.emojis import emoji

class Administracao(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='embed', description='Cria uma embed personalizada')
    async def embed(self, ctx: commands.Context):
        view = EmbedCreator(bot=self.client, timeout=600)
        async def check(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                return True
            else:
                embed = discord.Embed(description=f'{emoji["negative"]} Apenas {ctx.author} pode usar essa interação!')
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return False
        view.interaction_check = check
        await ctx.reply(embed=view.get_default_embed, view=view, mention_author=False)
    
    @commands.hybrid_command(name='falar', description='Envia uma mensagem personalizada no chat especificado; ou o chat atual, se não for mencionado')
    @app_commands.describe(mensagem='Mensagem que você quer enviar', arquivo='O arquivo ou imagem que você quer enviar', chat='Chat que você quer enviar a mensagem')
    async def falar(self, ctx: commands.Context, mensagem: Optional[str], arquivo: Optional[discord.Attachment], chat: Optional[discord.TextChannel]):
        mensagem = mensagem or None
        arquivo = await arquivo.to_file() if arquivo else None
        chat = chat or ctx.channel
        await chat.send(mensagem, file=arquivo)

        
async def setup(client):
    await client.add_cog(Administracao(client))
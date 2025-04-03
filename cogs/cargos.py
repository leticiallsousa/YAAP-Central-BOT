import discord
from discord.ext import commands
from discord.ui import Button, View
from utils.emojis import emoji
import asyncio

class PersistentCargos(discord.ui.View): 
    def __init__(self, callback): 
        super().__init__(timeout=None)
        self.callback = callback

    @discord.ui.button(label='Criar Solicitação', style=discord.ButtonStyle.green, custom_id='cargos_solicitacao')
    async def solicitacao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.callback(interaction)


class Cargos(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def solicitacao_callback(self, interaction: discord.Interaction):
        user = interaction.user
        channel = interaction.channel
        thread_name = f'👤 {user.global_name} ({user.id})'
        thread = discord.utils.get(channel.threads, name=thread_name)

        if not thread:
            thread = await channel.create_thread(name=thread_name)
        elif thread.locked:
            await thread.edit(locked=False)
        elif not thread.locked:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title=f'{emoji["error"]} Você já possui uma solicitação em andamento!!',
                    description=f'Por favor, aguarde a análise do seu pedido em {thread.mention}.\n\nAssim que nossa equipe terminar de revisar, entraremos em contato para dar sequência ao processo.',
                    colour=discord.Colour(0xe3242b)
                ), 
                ephemeral=True
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                title='✨ Nova Solicitação Criada!', 
                description=f'Vá até {thread.mention} para fornecer as informações necessárias.\n\nNossa equipe estará atenta para revisar sua solicitação assim que os dados forem enviados.', 
                colour=discord.Colour(0x3d6333)
                ), 
            ephemeral=True
        )
        await thread.send(
            content=f'{user.mention}|<@&1317210425791615056>', 
            embed=discord.Embed(
                title='🗃️ Dados Necessários', 
                description='Por favor, forneça as seguintes informações:\n- Seu nome completo\n- Print do e-mail de aprovação referente ao cargo que está solicitando.\n- Seu cargo, área e/ou núcleo\n`Ex₁: Aluno de Artes da YAAP Academy`.\n\n`Ex₂: Coordenador de STEM da YAAP Academy e Time da YAAP 101`.\n\n**Lembre-se:** quando tudo estiver concluído, utilize o comando `!encerrar` para finalizar o atendimento.', 
                colour=discord.Colour(0x3d6333)
            )
        )

    @commands.command()
    async def cargos(self, ctx: commands.Context):
        embed = discord.Embed(
            title='💼 Solicitação de Cargos', 
            description=f'Para solicitar o seus cargos na YAAP e receber acesso ao restante do servidor, clique no botão abaixo para o pedido.', 
            colour=discord.Colour(0x5b1a55)
        )
        embed.add_field(
            name='Como fazer:', 
            value='- Clique no botão abaixo, aguarde a criação do ticket e então informe os dados solicitados.\n- Depois disso, nossa equipe vai verificar sua solicitação e o cargo será atribuído.'
        )
        embed.set_image(url='https://i.imgur.com/nIsKxRK.png')
        await ctx.send(embed=embed, view=PersistentCargos(self.solicitacao_callback))

    @commands.command()
    async def encerrar(self, ctx: commands.Context):
        if not hasattr(ctx.channel, 'parent_id') or ctx.channel.parent_id not in (1304047216108900383, 1296579008904957962, 1336521785407176704, 1336521671401803846):
            return
        await ctx.channel.edit(locked=True)
        embed = discord.Embed(
            title='⌛ Encerrando Atendimento...', 
            description=f'Em alguns instantes, o atendimento atual será encerrado e o canal será excluído.', 
            colour=discord.Colour(0x3d6333)
        )
        await ctx.send(embed=embed)
        await asyncio.sleep(5) 
        await ctx.channel.delete()


async def setup(client):
    await client.add_cog(Cargos(client))
    client.add_view(PersistentCargos(client.get_cog('Cargos').solicitacao_callback))
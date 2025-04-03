import discord
from discord.ext import commands
from discord.ui import Button, View
from utils.emojis import emoji
import asyncio

class PersistentTickets(discord.ui.View): 
    def __init__(self, callback): 
        super().__init__(timeout=None)
        self.callback = callback

    @discord.ui.button(label='Criar Ticket', style=discord.ButtonStyle.green, custom_id='suporte_solicitacao')
    async def solicitacao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.callback(interaction)


class Suporte(commands.Cog):
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
                    title=f'{emoji["error"]} Atendimento em Andamento', 
                    description=f'Você já possui um atendimento ativo em {thread.mention}. Por favor, aguarde nossa equipe finalizar antes de criar uma nova solicitação.', 
                    colour=discord.Colour(0xe3242b)
                ), 
                ephemeral=True
            )
        await interaction.response.send_message(
            embed=discord.Embed(
                title='✨ Novo Ticket Criado!', 
                description=f'Vá até {thread.mention} para fornecer mais informações.\n\nNossa equipe estará atenta para revisar seu caso.', 
                colour=discord.Colour(0x3d6333)
            ), 
            ephemeral=True
        )
        detalhes = discord.Embed(
            title='🗃️ Detalhe sua Solicitação', 
            description='Para que possamos ajudá-lo da melhor forma, por favor, forneça mais detalhes. Você pode:\n- Tirar dúvidas sobre a YAAP.\n- Relatar problemas ou sugerir melhorias.\n- Fazer uma reclamação.\n\n**Lembre-se:** quando tudo estiver concluído, utilize o comando `!encerrar` para finalizar o atendimento.', 
            colour=discord.Colour(0x3d6333)
        )
        await thread.send(content=f'{user.mention}|<@&1317210425791615056>', embed=detalhes)
        
    @commands.command()
    async def suporte(self, ctx: commands.Context):
        embed = discord.Embed(
            title='🎫 Atendimento', 
            description=f'Para tirar suas dúvidas sobre a YAAP ou o servidor, fazer uma sugestão, reclamação ou outro tipo de pedido, clique no botão abaixo para abrir um ticket.', 
            colour=discord.Colour(0x5b1a55)
        )
        embed.add_field(
            name='Como fazer:', 
            value='- Clique no botão abaixo, aguarde a criação do ticket e forneça as informações necessárias.\n- Nossa equipe irá analisar seu caso e fornecer a devida assistência.'
        )
        embed.set_image(url='https://i.imgur.com/aeaptfk.png')
        await ctx.send(embed=embed, view=PersistentTickets(self.solicitacao_callback))
    
    @commands.command()
    async def resolvido(self, ctx: commands.Context):
        if not hasattr(ctx.channel, 'parent_id') or ctx.channel.parent_id not in (1314465036386701322):
            return
        if ctx.author.id == ctx.channel.owner_id:
            await ctx.channel.edit(locked=True)
            await ctx.channel.add_tags(discord.Object(id=1316597367398727720))
            await ctx.send(f'Pronto! Seu post foi marcado como resolvido e o canal foi fechado para novas respostas.')
        else:
            await ctx.send(f'Ei, {ctx.channel.owner.mention}! Se sua dúvida já foi resolvida, use o comando `!resolvido` para encerrar o post.')
    
''' 
    @commands.command()
    async def arquivos(self, ctx: commands.Context):
        await ctx.message.delete()
        message = await ctx.send('Mensagem')
        thread = await message.create_thread(name='Nome da Thread')
        await thread.edit(locked=True)
'''

async def setup(client):
    await client.add_cog(Suporte(client))
    client.add_view(PersistentTickets(client.get_cog('Suporte').solicitacao_callback))
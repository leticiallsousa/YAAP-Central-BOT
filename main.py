import discord
from discord.ext import commands, tasks
from utils.emojis import emoji
import asyncio
import os
from datetime import datetime, timezone, timedelta
import logging
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
tree = client.tree
discord.utils.setup_logging()

@client.event
async def on_ready():
    print('Estou online!')
    inactivity_check.start()

@tasks.loop(hours=1) 
async def inactivity_check(): 
    current_time = datetime.now(tz=timezone.utc)
    cutoff = current_time - timedelta(hours=48)

    for channel_id in (1304047216108900383, 1296579008904957962):
        channel = client.get_channel(channel_id)

        for thread in channel.threads:
            async for message in thread.history(limit=1):
                last_message = message
            if last_message and last_message.created_at <= cutoff:
                embed = discord.Embed(
                    title='⌛ Atendimento Cancelado por Inatividade',
                    description=(
                        'Após `48 horas` sem novas mensagens, este atendimento foi encerrado. '
                        'O tópico será excluído em `2 minutos`. Caso ainda precise de ajuda, '
                        'espere esse tempo e abra uma nova solicitação.'
                    ),
                    colour=discord.Colour(0x3d6333)
                )
                await thread.send(embed=embed)
                await thread.edit(locked=True, archived=True)
                await asyncio.sleep(120)
                await thread.delete()

@client.check
def check_permission(ctx: commands.Context):
    if hasattr(ctx.channel, 'parent_id'):
        if ctx.channel.parent_id in (1304047216108900383, 1296579008904957962) and ctx.message.content == f'{client.command_prefix}encerrar':
            return True
        elif ctx.channel.parent_id == 1314465036386701322 and ctx.message.content == f'{client.command_prefix}resolvido':
            return True
    if not any(role.name == 'admin' for role in ctx.author.roles) and ctx.author.id != 537100512202457089:
        raise commands.CommandError("Você não possui permissão para usar os comandos do YAAP Central Bot")
    return True

@client.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    embed = discord.Embed(description=f'{emoji["error"]} ', colour=discord.Colour(0x3d6333))
    if isinstance(error, commands.CommandInvokeError):
        error = error.original
    elif isinstance(error, commands.GuildNotFound):
        embed.description += 'O servidor informado é inválido. Eu posso não ter acesso a ele, ou ele pode não existir.'
    elif isinstance(error, commands.ChannelNotFound):
        embed.description += 'O chat informado é inválido. Eu posso não ter acesso a ele, ou ele pode não existir.'
    elif isinstance(error, commands.MissingRequiredArgument):
        embed.description += 'Você não forneceu todos os argumentos necessários para este comando.'
    elif isinstance(error, commands.BadArgument):
        embed.description += 'Um ou mais argumentos fornecidos são inválidos.'
    elif isinstance(error, commands.CommandNotFound):
        embed.description += 'Comando não encontrado. Verifique se você digitou corretamente.'
    else:
        embed.description += 'Oops! Ocorreu um erro'
        embed.add_field(name='Erro:', value=f'```py\n{type(error).__name__}: {error}```')

    logging.error(f'Erro no comando: {ctx.command} - {type(error).__name__}: {error}')
    
    await ctx.send(embed=embed, ephemeral=True) if ctx.interaction else await ctx.send(embed=embed, mention_author=False)

async def load():
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
	await load()
	await client.start(TOKEN)

asyncio.run(main())
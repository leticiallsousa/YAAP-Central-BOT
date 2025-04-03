import discord
from discord.ext import commands
from discord.ui import Button, View
import os
import random

class Musica(commands.Cog):
    def __init__(self, client):
        self.client = client

    def play_next(self, voice_client):
        # Seleciona uma música aleatória da lista de audios do drive
        music_url = os.path.join('utils/musicas', random.choice(os.listdir('utils/musicas')))
        source = discord.FFmpegPCMAudio(music_url, options='-b:a 256k -filter:a "volume=0.25"')
        voice_client.play(source, after=lambda e: self.play_next(voice_client)) # faz com que a próxima música seja tocada após a atual terminar

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        study_room_id = 1317280156896723046
        study_room = self.client.get_channel(study_room_id)
        voice_client = discord.utils.get(self.client.voice_clients, guild=study_room.guild)

        # Verifica se o usuário entrou no canal de voz
        if before.channel != study_room and after.channel == study_room:
            if not voice_client or voice_client.channel.id != study_room_id:
                try:
                    voice_client = await study_room.connect()
                except discord.DiscordException as e:
                    print(f"Erro ao conectar ao canal de voz: {e}")
                    return
                # Verifica se a conexão foi bem-sucedida
                if voice_client and voice_client.is_connected():
                    self.play_next(voice_client)     

        # Verifica se o usuário saiu do canal de voz
        if before.channel == study_room and after.channel != study_room:
            # Verifica se o canal de voz está vazio
            if len(before.channel.members) == 1:
                if voice_client and voice_client.is_connected():
                    voice_client.stop()
                    await voice_client.disconnect()

    
        
async def setup(client):
    await client.add_cog(Musica(client))

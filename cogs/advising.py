import discord
from discord.ext import commands
from discord.ui import Button, View
from utils.emojis import emoji

class AdvisingModal(discord.ui.Modal):
    def __init__(self, title):
        super().__init__(title=title)

        self.add_item(discord.ui.TextInput(
            label="Nome",
            placeholder="Digite seu nome",
            required=True
        ))
        self.add_item(discord.ui.TextInput(
            label="E-mail",
            placeholder="Digite seu e-mail",
            required=True
        ))
        self.add_item(discord.ui.TextInput(
            label="Objetivo",
            placeholder="Qual seu objetivo com este advising?",
            required=True,
            max_length=500
        ))

    async def on_submit(self, interaction: discord.Interaction, role_id: int):
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
                    description=f'Por favor, aguarde enquanto nossa equipe revisa sua solicitação em {thread.mention}.\n\nEntraremos em contato assim que possível para dar sequência ao processo. Agradecemos sua paciência e compreensão.',
                    colour=discord.Colour(0xe3242b)
                ), 
                ephemeral=True
            )
        
        embed = discord.Embed(
            title=f'🗃️ Informações de {interaction.user.name}',
            colour=discord.Colour(0x3d6333)
        )
        embed.add_field(name='Nome', value=self.children[0].value, inline=False)
        embed.add_field(name='E-mail', value=self.children[1].value, inline=False)
        embed.add_field(name='Objetivo', value=self.children[2].value, inline=False)
        embed.set_footer(text='Lembre-se: quando tudo estiver concluído, utilize o comando !encerrar para finalizar o atendimento.')
        await thread.send(content=f'{interaction.user.mention}|<@&{role_id}>', embed=embed)
        
        await interaction.response.send_message(
            embed=discord.Embed(
            title='✨ Solicitação Criada!', 
            description=f'Vá até {thread.mention} para interagir com nosso time de Advising e tirar todas as suas dúvidas!', 
            colour=discord.Colour(0x3d6333)
            ), 
            ephemeral=True
        )

class PreCollegeModal(AdvisingModal):
    def __init__(self):
        super().__init__(title='Pre-College Advising')

    async def on_submit(self, interaction: discord.Interaction):
        await super().on_submit(interaction, role_id=1348109621805715507)

class CollegeModal(AdvisingModal):
    def __init__(self):
        super().__init__(title='College Advising')

    async def on_submit(self, interaction: discord.Interaction):
        await super().on_submit(interaction, role_id=1348110100375797872)

class PersistentAdvising(discord.ui.View): 
    def __init__(self, callback, type): 
        super().__init__(timeout=None)
        self.callback = callback
        self.type = type

    @discord.ui.button(label='Solicitar Advising', style=discord.ButtonStyle.green, custom_id='advising_solicitacao')
    async def solicitacao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.callback(interaction, self.type)

class Advising(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def advising_callback(self, interaction: discord.Interaction, type):
        if type == 'precollege':
            await interaction.response.send_modal(PreCollegeModal())
        if type == 'college':
            await interaction.response.send_modal(CollegeModal())
        
    @commands.command()
    async def precollege(self, ctx: commands.Context):
        embed = discord.Embed(
            title='📝 Pre-College Advising', 
            description=f'Se você é um estudante do ensino médio ou gap year e está se preparando para ingressar na faculdade, este é o espaço ideal para tirar dúvidas sobre processos de admissão, preparação para exames, bolsas de estudo e muito mais!', 
            colour=discord.Colour(0xd6951d)
        )
        embed.add_field(
            name='Como fazer:', 
            value='1. Clique no botão abaixo e preencha as informações solicitadas.\n2. Vá até o canal criado e interaja diretamente com um de nossos Pre-College Advisors.\n3. Se necessário, marque uma reunião no canal de voz para um atendimento mais detalhado.'
        )
        embed.set_image(url='https://i.imgur.com/LjpxQfO.png')
        await ctx.send(embed=embed, view=PersistentAdvising(self.advising_callback, 'precollege'))

    @commands.command()
    async def college(self, ctx: commands.Context):
        embed = discord.Embed(
            title='📝 College Advising', 
            description=f'Se você já está na faculdade e precisa de orientação sobre escolha de disciplinas, planejamento de carreira, estágios ou outros assuntos relacionados à vida universitária, este canal é para você!', 
            colour=discord.Colour(0xd6951d)
        )
        embed.add_field(
            name='Como fazer:', 
            value='1. Clique no botão abaixo e preencha as informações solicitadas.\n2. Vá até o canal criado e interaja diretamente com um de nossos College Advisors.\n3. Se necessário, marque uma reunião no canal de voz para um atendimento mais detalhado.'
        )
        embed.set_image(url='https://i.imgur.com/LjpxQfO.png')
        await ctx.send(embed=embed, view=PersistentAdvising(self.advising_callback, 'college'))

async def setup(client):
    await client.add_cog(Advising(client))
    client.add_view(PersistentAdvising(client.get_cog('Advising').advising_callback, 'precollege'))
    client.add_view(PersistentAdvising(client.get_cog('Advising').advising_callback, 'college'))

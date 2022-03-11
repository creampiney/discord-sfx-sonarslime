import discord
import random
import json
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from discord_components.client import DiscordComponents

from soundeffect import SoundEff
# ------------------- for heroku ----------------------------
#import ctypes
#import ctypes.util

#find_opus = ctypes.util.find_library('opus')
#discord.opus.load_opus(find_opus)
# -----------------------------------------------------------
prefix = "-"

with open('config.json') as json_file:
    TOKEN = json.load(json_file)['DISCORD_TOKEN']

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

random.seed(1111)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Sound Effect"))
    DiscordComponents(bot)


@bot.event
async def on_button_click(interaction):
    if interaction.custom_id[:3] == "sf_":
        await interaction.respond(content="HAHAHA", type=6)
        await SoundEff().classify(interaction, bot)


@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return 

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()


@bot.command()
async def help(ctx):
    emBed = discord.Embed(title="Welcome to "+bot.user.name+"!", color=0x977fd7)
    emBed.add_field(name="sf", value="Show sound effect board", inline=False)
    await ctx.channel.send(embed=emBed)


@bot.command()
async def sf(ctx):
    await SoundEff().button(ctx)


@bot.command()
async def quit(ctx, msg):
    if msg == "1234":
        await bot.logout()

bot.run(TOKEN)

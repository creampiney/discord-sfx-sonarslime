import discord
from discord.utils import get
import youtube_dl
import asyncio
from async_timeout import timeout
from functools import partial
from datetime import date, datetime
from discord_components.component import ActionRow
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
import codecs
import math
from datetime import datetime
from deletesf import delete_sf
from infosf import info_sf
from renamesf import rename_sf

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
ydl_opts = {'format': 'bestaudio'}
ytdl_format_options = {
    'format': 
    'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)



class SoundEff:
    async def button(self, ctx):
        guild = ctx.guild
        emBed = discord.Embed(title="Sound Effect Board", color=0x977fd7)
        emBed.add_field(name="Click the buttons to play sound effect", value="Page "+str(1)+" of "+str(await self.get_total_pages_num(guild)), inline=False)

        buttons = await self.get_button_page(guild, pages=1)

        board = await ctx.channel.send(embed=emBed, components=buttons)


    async def classify(self, interaction, bot):
        customid = interaction.custom_id
        guild = interaction.guild
        channel = interaction.channel
        user = interaction.user
        buttonname = interaction.interaction_id
        bot_list = [guild, channel, user, bot, buttonname]

        code_id = customid[3:]
        
        if code_id[:4] == "http":        # If it is website url
            await self.play(bot_list, await self.get_yt_source_url(code_id))
            return

        code_id = code_id.split("_")

        if code_id[0] == "stop":
            voice_client = get(bot.voice_clients, guild=guild)
            if voice_client.is_playing():
                voice_client.stop()

        elif code_id[0] == "refresh":
            board = await channel.fetch_message(int(code_id[1]))
            await self.refresh_message(board)

        elif code_id[0] == "add":
            await self.add_sfx(bot_list, await channel.fetch_message(int(code_id[1])))

        elif code_id[0] == "option":
            await self.get_option_board(interaction)

        elif code_id[0] == "closeoption":
            await interaction.message.delete()

        elif code_id[0] == "previouspage":
            await self.refresh_message(interaction.message, adding=-1)

        elif code_id[0] == "nextpage":
            await self.refresh_message(interaction.message, adding=1)

        elif code_id[0] == "choosepage":
            new_pages = await self.select_pages(bot_list)
            await self.refresh_message(interaction.message, adding=new_pages - await self.get_current_page(interaction.message))

        elif code_id[0] == "delete":
            board = await channel.fetch_message(int(code_id[1]))
            await delete_sf().delete(interaction, board, bot)
            await self.refresh_message(board)

        elif code_id[0] == "info":
            board = await channel.fetch_message(int(code_id[1]))
            await info_sf().info(interaction, board, bot, await self.get_current_page(board))

        elif code_id[0] == "rename":
            board = await channel.fetch_message(int(code_id[1]))
            await rename_sf().rename(interaction, board, bot, await self.get_current_page(board))
            await self.refresh_message(board)

        else:
            await self.play(bot_list, "sf/"+code_id[0]+".mp3")

        
        return



    async def play(self, bot_list, search: str):
        guild = bot_list[0]
        channel = bot_list[1]
        user = bot_list[2]
        bot = bot_list[3]
        buttonname = bot_list[4]
        try:
            channel = user.voice.channel
        except:
            print("ERROR : "+user.name+" was trying to play sf but he is outside vc.")
            return

        voice_client = get(bot.voice_clients, guild=guild)

        if voice_client == None:
            await channel.connect()
            voice_client = get(bot.voice_clients, guild=guild)

        if voice_client.is_playing():
            voice_client.stop()
        
        print(user.name, "-->", buttonname)

        if search[:4] == "http":
            source = discord.FFmpegPCMAudio(source=search, **FFMPEG_OPTIONS)
        else:
            source = discord.FFmpegPCMAudio(source=search)
        guild.voice_client.play(source, after=None)

        # await self.input_history(user, buttonname)



    async def get_yt_source_url(self, code_id):
        with youtube_dl.YoutubeDL(ytdl_format_options) as ydl:
            p = datetime.now()
            info = ydl.extract_info(code_id, download=False)
            print(datetime.now() - p)
            URL = info['formats'][0]['url']
        return URL

    async def get_button_page(self, guild, pages=1):
        return await self.get_button_list_from_file(guild, pages) + await self.get_command_button(guild, pages)
        


    async def get_button_list_from_file(self, guild, pages=1):
        try:
            f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8")
        except FileNotFoundError:
            await self.new_file(guild)
            f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8")

        button_unorg_list = []
        count = 0
        name = f.readline().strip()
        while name != "":
            buttonid = f.readline().strip()
            button_unorg_list.append(Button(label=name, custom_id=buttonid, style=1))
            membername = f.readline().strip()
            buttondate = f.readline().strip()
            name = f.readline().strip()
            count += 1
        f.close()
        button_order_list = [button_unorg_list[i:i+5] for i in range(20*(pages-1),min(count, 20*(pages)),5)]
        return button_order_list

    async def get_command_button(self, guild, pages=1):
        command_button_list = [ 
                                Button(label="Stop sound effect", custom_id="sf_stop", style=4),
                                Button(label="Refresh / Add or Remove SFX", custom_id="sf_option", style=3),
                                ]

        if pages == 1:
            command_button_list.append(Button(label="< Previous Page", custom_id="sf_previouspage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="< Previous Page", custom_id="sf_previouspage_"+str(pages), style=2))

        command_button_list.append(Button(label="Choose page number", custom_id="sf_choosepage", style=2))

        if pages == await self.get_total_pages_num(guild):
            command_button_list.append(Button(label="Next Page >", custom_id="sf_nextpage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="Next Page >", custom_id="sf_nextpage_"+str(pages), style=2))

        return [command_button_list]


    async def refresh_message(self, board, adding=0):
        emBed = discord.Embed(title="Sound Effect Board", color=0x977fd7)
        pages = await self.get_current_page(board) + adding
        if pages > await self.get_total_pages_num(board.guild):
            pages -= 1
        emBed.add_field(name="Click the buttons to play sound effect", value="Page "+str(pages)+" of "+str(await self.get_total_pages_num(board.guild)), inline=False)
        buttons = await self.get_button_page(board.guild, pages)
        await board.edit(embed=emBed, components=buttons)


    async def add_sfx(self, bot_list, mainboard):
        guild = bot_list[0]
        channel = bot_list[1]
        user = bot_list[2]
        bot = bot_list[3]

        emBed = discord.Embed(title="Adding sound effect", color=0x977fd7)
        emBed.add_field(name="Activator : "+user.name, value="Put the sound effect's name (This name will be shown on the button)\nType `sf_exit` to leave this process.", inline=False)
        board = await channel.send(embed=emBed)

        def check(msg):
            return msg.author == user and msg.channel == channel

        try:
            msg = await bot.wait_for('message', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await board.delete()
            return
        
        new_name = msg.content.strip()
        await msg.delete()

        if new_name == "sf_exit":
            await board.delete()
            return

        emBed = discord.Embed(title="Adding sound effect", color=0x977fd7)
        emBed.add_field(name="Activator : "+user.name, value="Put YouTube url of the sound effect\nType `sf_exit` to leave this process.", inline=False)
        await board.edit(embed=emBed)

        def check(msg):
            return msg.author == user and msg.channel == channel

        try:
            msg = await bot.wait_for('message', timeout=600.0, check=check)
        except asyncio.TimeoutError:
            await board.delete()
            return

        new_url = msg.content.strip()
        await msg.delete()

        if new_url == "sf_exit":
            await board.delete()
            return

        status = await self.add_sfx_in_file(new_name, new_url, guild, user)
        await self.refresh_message(mainboard)

        emBed = discord.Embed(title="Adding sound effect", color=0x977fd7)
        if status == 0:
            emBed.add_field(name="Activator : "+user.name, value="Adding SFX completed!", inline=False)
        else:
            emBed.add_field(name="Activator : "+user.name, value="Adding SFX failed!\n[Duplicate URL]", inline=False)
        await board.edit(embed=emBed)
        await asyncio.sleep(2)
        await board.delete()


    async def add_sfx_in_file(self, new_name, new_url, guild, user):
        f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8")
        data_all_list = f.readlines()
        data_all_list = [e.strip() for e in data_all_list]
        f.close()
        if "sf_"+new_url.strip() in data_all_list[1::4]:
            return 1
        
        f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "a", "utf-8")
        f.write(new_name+"\n")
        f.write("sf_"+new_url+"\n")
        f.write(str(user.name)+"\n")
        f.write(str(datetime.now())+"\n")
        f.close()
        return 0

    async def get_option_board(self, interaction):
        board_id = interaction.message.id
        option_button_list = [
                                [ 
                                Button(label="Refresh", custom_id="sf_refresh_"+str(board_id), style=3),
                                Button(label="Add SFX", custom_id="sf_add_"+str(board_id), style=3),
                                Button(label="Remove SFX", custom_id="sf_delete_"+str(board_id), style=4),
                                Button(label="Info", custom_id="sf_info_"+str(board_id), style=2),
                                Button(label="Rename", custom_id="sf_rename_"+str(board_id), style=2),
                                ],
                                [ 
                                Button(label="Close the options", custom_id="sf_closeoption_"+str(board_id), style=4),
                                ],
                                ]
        emBed = discord.Embed(title="Add SFX / Remove SFX / Refresh", color=0x977fd7)
        board = await interaction.channel.send(embed=emBed, components=option_button_list)


    async def get_total_pages_num(self, guild):
        try:
            f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8")
        except FileNotFoundError:
            await self.new_file(guild)
            f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8")
        data_list = f.readlines()
        f.close()
        return max(math.ceil((len(data_list)//4)/20), 1)

    async def get_current_page(self, board):
        content_word_list = board.embeds[0].fields[0].value.split()
        return int(content_word_list[1])

    async def select_pages(self, bot_list):
        guild = bot_list[0]
        channel = bot_list[1]
        user = bot_list[2]
        bot = bot_list[3]

        emBed = discord.Embed(title="Select pages", color=0x977fd7)
        emBed.add_field(name="Put page number here", value="** **", inline=False)
        board = await channel.send(embed=emBed)

        def check(msg):
            return msg.author == user and msg.channel == channel

        isDone = False

        while not isDone:
            try:
                msg = await bot.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await board.delete()
                return

            try:
                new_pages = int(msg.content.strip())
            except ValueError:
                emBed = discord.Embed(title="Select pages", color=0x977fd7)
                emBed.add_field(name="Invalid number. Put page number again.", value="** **", inline=False)
                await board.edit(embed=emBed)
            else:
                if not 1 <= new_pages <= await self.get_total_pages_num(board.guild):
                    emBed = discord.Embed(title="Select pages", color=0x977fd7)
                    emBed.add_field(name="Page number that you put is out of range. Put page number again.", value="** **", inline=False)
                    await board.edit(embed=emBed)
                else:
                    isDone = True
                    await board.delete()

            await msg.delete()

        return new_pages

    
    async def new_file(self, guild):
        f = codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "w", "utf-8")
        p = datetime.now()
        new_str = f"Illuminati\nsf_https://www.youtube.com/watch?v=sahAbxq8WPw\nSonarSlime\n{str(p)}\nQuack\nsf_https://www.youtube.com/watch?v=nucoyLwGsoY\nSonarSlime\n{str(p)}\nDetective Conan\nsf_https://www.youtube.com/watch?v=RsyxFQ23Ezk\nSonarSlime\n{str(p)}\nYEAY\nsf_https://www.youtube.com/watch?v=kp42doFyeiM\nSonarSlime\n{str(p)}\nKahoot\nsf_https://www.youtube.com/watch?v=hnnUD9-hD8A\nSonarSlime\n{str(p)}\n"
        f.write(new_str)
        f.close()
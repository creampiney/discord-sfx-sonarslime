import discord
from datetime import datetime
from discord_components import Button
import codecs
import math
from datetime import datetime
import asyncio


class info_sf:
    async def info(self, interaction, main_board, bot, pages):
        guild = interaction.guild
        channel = interaction.channel
        user = interaction.user
        await self.button(bot, guild, channel, user, main_board, pages)



    async def button(self, bot, guild, channel, user, main_board, pages):
        sf_list = await self.get_all_sf_list(guild)
        current_page = pages

        emBed = discord.Embed(title="Finding information", color=0x977fd7)
        emBed.add_field(name="Click the buttons to see information of sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
        emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
        buttons = await self.get_button_page(guild, sf_list, pages=current_page)
        board = await channel.send(embed=emBed, components=buttons)
        

        while True:
            def check(interaction):
                return interaction.user == user and interaction.message == board and interaction.custom_id.split("_")[0] == "insf"
            try:
                interaction = await bot.wait_for("button_click",timeout=300.0, check=check)
            except asyncio.TimeoutError:
                await board.delete()
                return
            await interaction.respond(content="HAHAHA", type=6)
            customid = interaction.custom_id.split("_")
            abr = customid[0]
            code = customid[1]
            if code == "cancel":
                await board.delete()
                return
            elif code == "nextpage":
                current_page += 1
                emBed = discord.Embed(title="Finding information", color=0x977fd7)
                emBed.add_field(name="Click the buttons to see information of sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                await board.edit(embed=emBed, components=buttons)
            elif code == "previouspage":
                current_page -= 1
                emBed = discord.Embed(title="Finding information", color=0x977fd7)
                emBed.add_field(name="Click the buttons to see information of sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                await board.edit(embed=emBed, components=buttons)
            elif code == "choosepage":
                emBed = discord.Embed(title="Select pages", color=0x977fd7)
                emBed.add_field(name="Put page number here", value="** **", inline=False)
                chooseboard = await channel.send(embed=emBed)
                def check(msg):
                        return msg.author == user and msg.channel == channel

                isDone = False

                while not isDone:
                    try:
                        msg = await bot.wait_for('message', timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        await chooseboard.delete()

                    try:
                        new_pages = int(msg.content.strip())
                    except ValueError:
                        emBed = discord.Embed(title="Select pages", color=0x977fd7)
                        emBed.add_field(name="Invalid number. Put page number again.", value="** **", inline=False)
                        await chooseboard.edit(embed=emBed)
                    else:
                        if not 1 <= new_pages <= await self.get_total_pages_num(sf_list):
                            emBed = discord.Embed(title="Select pages", color=0x977fd7)
                            emBed.add_field(name="Page number that you put is out of range. Put page number again.", value="** **", inline=False)
                            await chooseboard.edit(embed=emBed)
                        else:
                            isDone = True
                            await chooseboard.delete()
                            current_page = new_pages
                            emBed = discord.Embed(title="Finding information", color=0x977fd7)
                            emBed.add_field(name="Click the buttons to see information of sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                            emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                            buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                            await board.edit(embed=emBed, components=buttons)

                    await msg.delete()
            else:
                buttonname = "sf_"+interaction.custom_id[6+len(str(code)):]
                with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8") as f:
                    name = f.readline().strip()
                    while name != "":
                        buttonid = f.readline().strip()
                        membername = f.readline().strip()
                        buttondate = f.readline().strip()
                        if buttonid == buttonname:
                            break
                        name = f.readline().strip()
                    f.close()
                if name != "":
                    emBed = discord.Embed(title="Sound Effect Information", color=0x977fd7)
                    emBed.add_field(name=name, value=f"Link: {buttonid[3:]}\nAdder: {membername}\nAdding Time: {datetime.strptime(buttondate, '%Y-%m-%d %H:%M:%S.%f')}", inline=False)
                    buttons = [Button(label="Close", custom_id="sf_closeoption", style=4)]
                    await board.edit(embed=emBed, components=buttons)
                    return








    async def get_all_sf_list(self, guild):
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8") as f:
            sf_list = []
            name = f.readline().strip()
            idx = 0
            while name != "":
                buttonid = f.readline().strip()
                sf_list.append([name, "insf_"+str(idx)+"_"+buttonid[3:]])
                membername = f.readline().strip()
                buttondate = f.readline().strip()
                name = f.readline().strip()
                idx += 1
            f.close()
        return sf_list


    async def get_total_pages_num(self, sf_list):
        return math.ceil(len(sf_list)/20)


    async def get_button_page(self, guild, sf_list, pages=1):
        # Generate buttons
        button_list = []
        for i in range(20*(pages-1),min(len(sf_list), 20*(pages))):
            button_list.append(Button(label=sf_list[i][0], custom_id=sf_list[i][1], style=1))
        button_list = [button_list[i:i+5] for i in range(0,len(button_list),5)]

        return button_list + await self.get_command_button(guild, sf_list, pages)


    async def get_command_button(self, guild, sf_list, pages=1):
        command_button_list = []

        if pages == 1:
            command_button_list.append(Button(label="< Previous Page", custom_id="insf_previouspage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="< Previous Page", custom_id="insf_previouspage_"+str(pages), style=2))

        command_button_list.append(Button(label="Choose page number", custom_id="insf_choosepage", style=2))

        if pages == await self.get_total_pages_num(sf_list):
            command_button_list.append(Button(label="Next Page >", custom_id="insf_nextpage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="Next Page >", custom_id="insf_nextpage_"+str(pages), style=2))

        command_button_list.append(Button(label="Cancel", custom_id="insf_cancel", style=4))

        return [command_button_list]

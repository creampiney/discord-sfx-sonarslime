import discord
from datetime import datetime
from discord_components import Button
import codecs
import math
from datetime import datetime
import asyncio


class rename_sf:
    async def rename(self, interaction, main_board, bot, pages):
        guild = interaction.guild
        channel = interaction.channel
        user = interaction.user
        await self.button(bot, guild, channel, user, main_board, pages)



    async def button(self, bot, guild, channel, user, main_board, pages):
        sf_list = await self.get_all_sf_list(guild)
        current_page = pages

        emBed = discord.Embed(title="Changing Button Name", color=0x977fd7)
        emBed.add_field(name="Click the buttons to change the button name", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
        emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
        buttons = await self.get_button_page(guild, sf_list, pages=current_page)
        board = await channel.send(embed=emBed, components=buttons)
        

        while True:
            def check(interaction):
                return interaction.user == user and interaction.message == board and interaction.custom_id.split("_")[0] == "rnsf"
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
                emBed = discord.Embed(title="Changing Button Name", color=0x977fd7)
                emBed.add_field(name="Click the buttons to change the button name", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                await board.edit(embed=emBed, components=buttons)
            elif code == "previouspage":
                current_page -= 1
                emBed = discord.Embed(title="Changing Button Name", color=0x977fd7)
                emBed.add_field(name="Click the buttons to change the button name", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
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
                            emBed = discord.Embed(title="Changing Button Name", color=0x977fd7)
                            emBed.add_field(name="Click the buttons to change the button name", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                            emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                            buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                            await board.edit(embed=emBed, components=buttons)

                    await msg.delete()
            else:
                idx = int(customid[1])

                buttonname = "sf_"+interaction.custom_id[6+len(str(code)):]
                emBed = discord.Embed(title="Changing Button Name", color=0x977fd7)
                emBed.add_field(name="Put new button name", value="Type `rename_exit` to leave this process.", inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                confirmboard = await channel.send(embed=emBed)
                def check(msg):
                        return msg.author == user and msg.channel == channel
                try:
                    msg = await bot.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await confirmboard.delete()
                    await msg.delete()
                else:
                    if msg.content == "rename_exit":
                        await confirmboard.delete()
                        await msg.delete()
                    else:
                        await msg.delete()
                        await confirmboard.delete()
                        await board.delete()
                        await self.rename_from_file(guild, msg.content, buttonname, channel)
                        return
                
                








    async def get_all_sf_list(self, guild):
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8") as f:
            sf_list = []
            name = f.readline().strip()
            idx = 0
            while name != "":
                buttonid = f.readline().strip()
                sf_list.append([name, "rnsf_"+str(idx)+"_"+buttonid[3:]])
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
            command_button_list.append(Button(label="< Previous Page", custom_id="rnsf_previouspage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="< Previous Page", custom_id="rnsf_previouspage_"+str(pages), style=2))

        command_button_list.append(Button(label="Choose page number", custom_id="rnsf_choosepage", style=2))

        if pages == await self.get_total_pages_num(sf_list):
            command_button_list.append(Button(label="Next Page >", custom_id="rnsf_nextpage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="Next Page >", custom_id="rnsf_nextpage_"+str(pages), style=2))

        command_button_list.append(Button(label="Cancel", custom_id="rnsf_cancel", style=4))

        return [command_button_list]


    async def rename_from_file(self, guild, newname, linkname, channel):
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8") as f:
            all_list = f.readlines()
            for i in range(len(all_list)):
                if all_list[i].strip() == linkname:
                    oldname = all_list[i-1].strip()
                    all_list[i-1] = newname + "\n"
            f.close()
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "w", "utf-8") as f:
            f.write("".join(all_list))
            f.close()
        
        emBed = discord.Embed(title="Changing Button Name", color=0x977fd7)
        emBed.add_field(name="Changing completed!", value=f"{oldname} --> {newname}", inline=False)
        doneboard = await channel.send(embed=emBed)
        await asyncio.sleep(2)
        await doneboard.delete()

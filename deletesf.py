import discord
from datetime import datetime
from discord_components import Button
import codecs
import math
from datetime import datetime
import asyncio


class delete_sf:
    async def delete(self, interaction, main_board, bot):
        guild = interaction.guild
        channel = interaction.channel
        user = interaction.user
        await self.button(bot, guild, channel, user, main_board)



    async def button(self, bot, guild, channel, user, main_board):
        sf_list = await self.get_all_sf_list(guild)
        current_page = 1

        emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
        emBed.add_field(name="Click the buttons to delete sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
        emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
        buttons = await self.get_button_page(guild, sf_list, pages=current_page)
        board = await channel.send(embed=emBed, components=buttons)
        

        while True:
            def check(interaction):
                return interaction.user == user and interaction.message == board and interaction.custom_id.split("_")[0] in ["dsf", "cdsf"]
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
                emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
                emBed.add_field(name="Click the buttons to delete sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                await board.edit(embed=emBed, components=buttons)
            elif code == "previouspage":
                current_page -= 1
                emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
                emBed.add_field(name="Click the buttons to delete sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
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
                            emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
                            emBed.add_field(name="Click the buttons to delete sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                            emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                            buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                            await board.edit(embed=emBed, components=buttons)

                    await msg.delete()
            elif code == "remove":
                emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
                emBed.add_field(name="Are you sure to delete selected sound effect?", value="** **", inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = [
                            [
                                Button(label="Yes", custom_id="dccsf_yes", style=2),
                                Button(label="No", custom_id="dccsf_no", style=2),
                            ]
                            ]
                confirmboard = await channel.send(embed=emBed, components=buttons)
                def check(interaction):
                    return interaction.user == user and interaction.message == confirmboard

                try:
                    interaction = await bot.wait_for("button_click",timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await confirmboard.delete()
                else:
                    await interaction.respond(content="HAHAHA", type=6)
                    if interaction.custom_id == "dccsf_yes":
                        print("Delete yes")
                        await confirmboard.delete()
                        await board.delete()
                        await self.deleting_sf_from_file(guild, user, sf_list, channel, main_board)
                        return
                    else:
                        print("Delete no")
                        await confirmboard.delete()

            elif abr == "cdsf":
                idx = int(code)
                sf_list[idx][1] = sf_list[idx][1][1:]
                emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
                emBed.add_field(name="Click the buttons to delete sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                await board.edit(embed=emBed, components=buttons)
            else:
                idx = int(code)
                sf_list[idx][1] = "c"+sf_list[idx][1]
                emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
                emBed.add_field(name="Click the buttons to delete sound effect", value="Page "+str(current_page)+" of "+str(await self.get_total_pages_num(sf_list)), inline=False)
                emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
                buttons = await self.get_button_page(guild, sf_list, pages=current_page)
                await board.edit(embed=emBed, components=buttons)







    async def get_all_sf_list(self, guild):
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8") as f:
            sf_list = []
            name = f.readline().strip()
            idx = 0
            while name != "":
                buttonid = f.readline().strip()
                sf_list.append([name, "dsf_"+str(idx)+"_"+buttonid[3:]])
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
            if sf_list[i][1][:4] == "dsf_":
                button_list.append(Button(label=sf_list[i][0], custom_id=sf_list[i][1], style=1))
            else:
                button_list.append(Button(label=sf_list[i][0], custom_id=sf_list[i][1], style=3))
        button_list = [button_list[i:i+5] for i in range(0,len(button_list),5)]

        return button_list + await self.get_command_button(guild, sf_list, pages)


    async def get_command_button(self, guild, sf_list, pages=1):
        command_button_list = [ 
                                Button(label="Remove SFXs", custom_id="dsf_remove", style=4),
                                ]

        if pages == 1:
            command_button_list.append(Button(label="< Previous Page", custom_id="dsf_previouspage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="< Previous Page", custom_id="dsf_previouspage_"+str(pages), style=2))

        command_button_list.append(Button(label="Choose page number", custom_id="dsf_choosepage", style=2))

        if pages == await self.get_total_pages_num(sf_list):
            command_button_list.append(Button(label="Next Page >", custom_id="dsf_nextpage_"+str(pages), style=2, disabled=True))
        else:
            command_button_list.append(Button(label="Next Page >", custom_id="dsf_nextpage_"+str(pages), style=2))

        command_button_list.append(Button(label="Cancel", custom_id="dsf_cancel", style=4))

        return [command_button_list]


    async def deleting_sf_from_file(self, guild, user, sf_list, channel, main_board):
        delete_list = [[e[0],"sf_"+e[1][6+len(e[1].split("_")[1]):]] for e in sf_list if e[1][0] == "c"]
        print(delete_list)
        emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
        emBed.add_field(name=f"Deleting {str(len(delete_list))} sound effects!", value="Please don't add sfx while deleting.", inline=False)
        emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
        board = await channel.send(embed=emBed)
        
        successcount = 0
        failedcount = 0
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "r", "utf-8") as f:
            all_list = f.readlines()
            all_list = [e.strip() for e in all_list]
            f.close()


        for each_element in delete_list:
            try:
                idx = all_list.index(each_element[1])
                for i in range(4):
                    all_list.pop(idx-1)
            except:
                failedcount += 1
            else:
                successcount += 1
        
        with codecs.open("data/buttonlist/buttonlist"+str(guild.id)+".sns", "w", "utf-8") as f:
            f.write("\n".join(all_list)+"\n")
            f.close()

        # Recovery mode
        with codecs.open("data/recover/recover"+str(guild.id)+".sns", "a", "utf-8") as f:
            for each_element in delete_list:
                f.write(each_element[0]+"\n"+each_element[1]+"\n"+user.name+"\n"+str(datetime.now())+"\n")
            f.close()

        emBed = discord.Embed(title="!! Deleting Sound Effect !!", color=0x977fd7)
        emBed.add_field(name=f"Deleting completed!", value=f"{str(successcount)} SFXs were deleted.\n{str(failedcount)} SFXs failed.", inline=False)
        emBed.add_field(name="Activator : "+user.name, value="** **", inline=False)
        await board.edit(embed=emBed)
        await asyncio.sleep(3)
        await board.delete()
        return
        
        
            
                
                


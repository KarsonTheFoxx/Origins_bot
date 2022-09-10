from email.charset import add_alias
from disnake.ext import commands
from disnake import Embed, Color, File, ButtonStyle
from disnake.ui import View, Button
from random import randint
from os import listdir
from json import load
def rgb():
    
    return tuple(rgb)

class info_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="info_beta", description="Info about the bot")
    async def info(self, inter):
        await inter.response.defer()
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        
        emb = Embed(title="Bot stats and other info", description="Designed for the Origins BE server by Vertex Arts\nYou can invite me to your server by clicking the blue button in my profile", color=Color.from_rgb(r, g, b))
        LOGO = File("res/Vertex_Arts_Logo.png")
        emb.set_thumbnail(file=LOGO)
        emb.add_field(name="Bot stats", value="Stats specific to the bot")
        
        files = listdir("./data/")
        files_count = len(files)
        pack_count = 0
        origin_count = 0
        user_count = 0
        guild_count = 0
        
        for file in files:
            with open(f"./data/{file}/data.json") as file_data:
                file_data = load(file_data)
            for pack in file_data["packs"]:
                pack_count += 1
                for origin in file_data["packs"][pack]["origins"]:
                    origin_count += 1
                    
        for guild in self.bot.guilds:
            guild_count += 1
            for member in guild.members:
                if  member.bot == False:
                    user_count += 1
        
        
        emb.add_field(name=f"Servering {guild_count} servers", value=f"{user_count} users")
        emb.add_field(name="Latency (on shard)", value=f"{round(self.bot.latency, 2)*100}ms")
        emb.add_field(name="Version", value="V1.2.0 codename: `roots`")
        emb.add_field(name="Origin stats", value="Stats about the currently listed origins", inline=False)
        emb.add_field(name="Number of packs", value=f"{files_count} ({pack_count} subpacks)")
        emb.add_field(name="Number of origins", value=origin_count)
        
        emb.add_field(name="Credits", value="Credits for various things", inline=False)
        emb.add_field(name="Karsonthefoxx#1260", value="Programmer of this bot")
        emb.add_field(name="lammas123#6714", value="Fine tuning the user experience and sparking the idea in the first place")
        
        emb.add_field(name="Adding a pack", value="Wish to add your pack to the bot? download the attached teplate, edit what you need to, and send it to the bots creator!", inline=False)
        emb.set_footer(text=f"Embed Color: {r}, {g}, {b}")
        
        template = File("template.zip")
        view = View(timeout=15)
        view.add_item(Button(style=ButtonStyle.url, url="https://discord.gg/7KvThGYxCp", label="Support server"))
        view.add_item(Button(style=ButtonStyle.url, url="https://discord.com/api/oauth2/authorize?client_id=998133147172610069&permissions=51200&scope=bot%20applications.commands", label="Invite me"))
        await inter.followup.send(file=template, embed=emb, view=view)

    @info.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            emb = Embed(title="Slow down!", description=f"This command has a rate limit of 5 times in 10 seconds in each server to avoid long load times and crashes", color=Color.from_rgb(r, g, b))
            emb.add_field(name="Retry after", value=f"{round(error.retry_after, 2)} Seconds")
        elif isinstance(error, commands.BotMissingPermissions):
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            emb = Embed(title="Im missing required permissions", description="Some required permissions are missing",color=Color.from_rgb(r, g, b))
            emb.add_field(name="missing permissions", value=" ".join(error.missing_permissions))
        else:
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            emb = Embed(title="Unknow Error", description="Something odd went wrong, if this keeps happening contact support",color=Color.from_rgb(r, g, b))
            
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(info_cog(bot))
from disnake.ext import commands
from disnake import Embed, Color, File
from os import listdir
from json import load
from random import randint

# Autocomplete for the origin name
async def autocomplete(inter, string:str):
    origin_names = []
    for packs in listdir("./data/"):
        with open(f"./data/{packs}/data.json") as packs:
            packs = load(packs)
        
        for pack in packs["packs"]:
            for origin in packs["packs"][pack]["origins"]:
                origin_names.append(origin)

    return [lang for lang in origin_names if string.lower() in lang.lower()]

# Cog handler      
class view_origin_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    # Command call
    @commands.slash_command(name="origins")
    @commands.cooldown(rate=5, per=10, type=commands.BucketType.user)
    async def origin(self, inter, origin:str=commands.Param(autocomplete=autocomplete)):
        await inter.response.defer()
        # Reverse key searching through the files for the specified origin
        for packs in listdir("./data/"):
            pack_name = packs
            with open(f"./data/{packs}/data.json", "rb") as packs:
                packs = load(packs)
            
            for pack in packs["packs"]:
                for origin_name in packs["packs"][pack]["origins"]: 
                    if origin_name == origin:
                        origin = packs["packs"][pack]["origins"][origin_name]
                        description = origin["description"]
                        # Populating the embed
                        emb = Embed(title=origin["display-name"], description=description, color=Color.from_rgb(origin["color"]["r"],origin["color"]["g"],origin["color"]["b"]))
                        file = File(origin["icon_path"])
                        emb.set_thumbnail(file=file)
                        emb.set_footer(text=f"pack: {pack_name}/{pack}")
                        powers = origin["powers"].keys()
                        downsides = origin["downsides"].keys()
                        neutrals = origin["neutrals"].keys()
                        cosmetics = origin["cosmetics"].keys()
                        
                        if origin["impact"] == "none":
                            emb.add_field(name="[Impact]", value="[⚪ ⚪ ⚪]", inline=False)
                        elif origin["impact"] == "low":
                            emb.add_field(name="[Impact]", value="[🟢 ⚪ ⚪]", inline=False)
                        elif origin["impact"] == "medium":
                            emb.add_field(name="[Impact]", value="[🟡 🟡 ⚪]",inline=False)
                        elif origin["impact"] == "high":
                            emb.add_field(name="[Impact]", value="[🔴 🔴 🔴]", inline=False)
                           
                        for power in powers:
                            desc = origin["powers"][power]
                            emb.add_field(name=f"[+] {power}", value = desc, inline=False)
                        
                        for neutral in neutrals:
                            desc = origin["neutrals"][neutral]
                            emb.add_field(name=f"[=] {neutral}", value=desc, inline=False)
                        
                        for downside in downsides:
                            desc = origin["downsides"][downside]
                            emb.add_field(name=f"[-] {downside}", value=desc, inline=False)
                        
                        for cosmetic in cosmetics:
                            desc = origin["cosmetics"][cosmetic]
                            emb.add_field(name=f"[$] {cosmetic}", value=desc, inline=False)
                        await inter.followup.send(embed=emb)
    # Error handler in the event of an error
    @origin.error
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
# Setup 
def setup(bot):
    bot.add_cog(view_origin_cog(bot))

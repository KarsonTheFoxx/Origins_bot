from disnake.ext import commands
from disnake import Embed, Color, File
from random import randint
class realms_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="realms", description="realms support for common issues")
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.guild)
    async def realms(self, inter):
        emb = Embed(title="Common realm issues", description="Addons have always been glitchy with minecraft realms, this is a list of some common issues", color=Color.from_rgb(randint(0, 255), randint(0, 255), randint(0, 255)))
        emb.add_field(name="GameTest framework addons", value="Due to some issues with the gametest framework, addons that use the gametest framework do not work properly on realms, this includes origins.", inline=False)
        emb.add_field(name="Uploading addons", value="As of September 3, 2022, we cannot apply addons directly to Realms. You must first create a world with the addon and then upload that world to your Realm to get it to work. It doesn't always work though.", inline=False)
        emb.add_field(name="Uploading to realms is unstable", value="Because realms are so unstable you have to throttle your internet connection to upload them.", inline=False)
        emb.add_field(name="Hydrophobic origins", value="Hydrophobic origins do not take damage in water as of verson 1.19", inline=False)
        emb.add_field(name="Tall origins", value="Tall origins (1.5 blocks) cant crouch to fit into 2 block tall spaces.", inline=False)
        file = File("res/realms.jpeg")
        emb.set_thumbnail(file=file)
        emb.set_footer(text="Realm information was provided by Rewby23#3830")
        await inter.response.send_message(embed=emb)

def setup(bot):
    bot.add_cog(realms_cog(bot))
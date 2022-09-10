from disnake.ext import commands
from disnake import Status, Activity, ActivityType, Intents, Embed, Color, Guild, CommandInteraction
from random import randint
from os import listdir
from asyncio import sleep

# Bot config and setup
INTENTS = Intents.default()
INTENTS.messages = True
INTENTS.members = True
bot = commands.AutoShardedInteractionBot(sync=True, intents=INTENTS)

for file in listdir("./cogs/"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

TOKEN = "MTAxNTcyNjc5NTE1ODQ2MjYwNA.GhlvVX.g2MvPvMF1jq-rKRgctz05sF_gtE8eOuDaS4NoQ"


# On ready functions
@bot.event
async def on_ready():
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name="Chat"), status=Status.idle)
    print("ready")

@bot.event
async def on_guild_join(guild:Guild):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    
    emb = Embed(title="Thank you for inviting me!", description="The Origins bot Beta is a test version of the bot used to test new features and support external creators unrelated to lammas123's pack, the invite button in the info command invites the classic version, to invite this version click my profile and click the blue add to server button!", color=Color.from_rgb(r, g, b))
    
    for channel in guild.text_channels:
        try:
            await channel.send(embed=emb)
            break
        except Exception:
            pass

@bot.slash_command(name="reload_cogs")
async def reload_cogs(inter:CommandInteraction, exclude:str=""):
    await inter.response.send_message("Reloading cogs")
    exclude = exclude.replace(" ", "").split(",")
    for cog in bot.cogs.copy():
        if not cog in exclude:
            try:
                bot.reload_extension(f"cogs.{cog}", package=None)
                await inter.channel.send(f"Loaded cog: {cog}")
            except Exception as error:
                print(error)
                await inter.channel.send(f"Failed to load cog: {cog}")
    await inter.channel.send(f"Excluded: {' '.join(exclude)}")


@bot.slash_command(name="load-unloaded")
async def load_cogs(inter:CommandInteraction):
    for file in listdir("./cogs/"):
        if file.endswith(".py"):
            try:
                bot.load_extension(f"cogs.{file[:-3]}")
                await inter.response.send_message(f"loaded {file}")
            except Exception:
                pass

@bot.slash_command(name="logoff")
async def log_off(self, inter:CommandInteraction):
    if inter.author.id == 855948446540496896:
        await inter.response.send_message("Logging off now")
        await bot.close()
    else:
        await inter.response.send_message("This command is owner only, this action will be logged", ephemeral=True)

bot.run(TOKEN)
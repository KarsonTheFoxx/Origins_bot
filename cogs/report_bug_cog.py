from disnake import Embed, ui, Color, CommandInteraction, TextInputStyle, ModalInteraction
from disnake.ext import commands
from random import randint
from json import load, dump

class bug_report_modal(ui.Modal):
    def __init__(self, mode, bot):
        self.mode = mode
        self.bot = bot

        components = [
            ui.TextInput(
                label="Name",
                custom_id="title",
                style=TextInputStyle.short,
                placeholder="Bug/feature name",
                required=True,
                max_length=24
            ),
            ui.TextInput(
                label="Description",
                custom_id="description",
                style=TextInputStyle.long,
                placeholder="Description",
                min_length=10,
                max_length=2000
            )
        ]
        super().__init__(title="Bug report/feature request", components=components, timeout=1000)

    async def callback(self, inter:ModalInteraction):
        data = {}
        for id, value in inter.text_values.items():
            data[id] = value
        await inter.response.send_message("bug report successful")

        user = self.bot.get_user(855948446540496896)

        emb = Embed(title=self.mode, description=f"{data['title']}\n{data['description']}")
        emb.add_field(name=inter.author.name+"#"+inter.author.discriminator, value=inter.author.id)

        await user.send(embed=emb)

class report_bug_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="report-bug", description="Report bugs to the developers")
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def report_bug(self, inter:CommandInteraction):
        with open("bug_report_config.json") as config:
            config = load(config)
        
        if inter.author.id not in config["banned"]:
            warning = Embed(title="Disclaimer", description="Missusing this command will result in the loss of use, report bugs at your own risk and refer to the bug guide tomorrow")
            warning.add_field(name="Breaking", value="A bug that reduces bot useability, this does not include the \"Something went wrong\" error for the `origins` and `other_origins` commands", inline=False)
            warning.add_field(name="Minor", value="A minor bug that reduces the appearance of how items are displayed, or permission related issues", inline=False)
            warning.add_field(name="Typo", value="Report typos within the bot, please refer to which command you used and what arguments you used i.e `/origin fox`", inline=False)
            warning.add_field(name="suggestion", value="A suggestion box for adding suggestions for people who add to the bot, this does not include new features", inline=False)
            warning.add_field(name="feature request", value="A feature request, this is for asking for aditional features such as new commands or functions", inline=False)

            view = ui.View()
            select = ui.Select()
            select.add_option(label="major")
            select.add_option(label="Minor")
            select.add_option(label="typo")
            select.add_option(label="suggestion")
            select.add_option(label="feature request")
            view.add_item(select)

            async def select_callback(new_inter):
                if new_inter.author == inter.author:
                    value = new_inter.values[0]
                    view.stop()
                    modal = bug_report_modal(value, self.bot)
                    await new_inter.response.send_modal(modal=modal)
                
                else:
                    new_inter.author.send("This menu isnt for you")
            
            select.callback = select_callback
            await inter.response.send_message(embed=warning, view=view)

def setup(bot):
    bot.add_cog(report_bug_cog(bot))
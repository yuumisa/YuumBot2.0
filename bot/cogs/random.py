import discord
import wavelink
from discord.ext import tasks, commands
from nhlpy import team
from nhlpy import schedule


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "test")
    async def test(self,ctx):
        await ctx.send("test")

    @commands.command(name = "canes")
    async def test_command(self,ctx):
        teams = schedule.Schedule().today(12)
        if(teams['totalItems'] == 0):
            await ctx.send("No Canes game today")
            return
        if(teams['dates'][0]['games'][0]['teams']['home'] == "Carolina Hurricanes"):
            await ctx.send("Carolina is the Home team") 
        else:
            await ctx.send("Carolina is not the Home team")
        if(teams['dates'][0]['games'][0]['status']['abstractGameState'] == "Live"):
            short = teams['dates'][0]['games'][0]['teams']
            awayID = short['away']['team']['id']
            away = team.Team(int(awayID)).info()['teams'][0]['abbreviation']
            awayScore = short['away']['score']
            homeID = short['team']['id']
            home = team.Team(int(homeID)).info()['teams'][0]['abbreviation']
            homeScore = short['home']['score']
            await ctx.send("Carolina is playing now. The score is " + str(away) + " " + str(awayScore) + " - " + str(homeScore) + " " + str(home))
        if(teams['dates'][0]['games'][0]['status']['abstractGameState'] == "Final"):
            short = teams['dates'][0]['games'][0]['teams']
            awayID = short['away']['team']['id']
            away = team.Team(int(awayID)).info()['teams'][0]['abbreviation']
            awayScore = short['away']['score']
            homeID = short['team']['id']
            home = team.Team(int(homeID)).info()['teams'][0]['abbreviation']
            homeScore = short['home']['score']
            if(awayScore > homeScore):
                await ctx.send(str(away) + " won. " + "The score was " + str(away) + " " + str(awayScore) + " - " + str(homeScore) + " " + str(home))
            else:
                await ctx.send(str(home) + " won. " + "The score was " + str(away) + " " + str(awayScore) + " - " + str(homeScore) + " " + str(home))
            if(str(home) == "CAR" and homeScore > awayScore):
                await ctx.send("Claim your free Chick Fil A sandwich")
    
    @tasks.loop(hours = 24)
    async def test_loop(self):
        await self.bot.get_channel(884910067005128794).send("<a:ankhafirerage:904523010030063647>")

    @commands.command()
    async def startBlaze(self, ctx):
        self.test_loop.start()
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def stopBlaze(self, ctx):
        self.test_loop.stop
        await ctx.message.add_reaction('✅')

def setup(bot):
    bot.add_cog(Random(bot))
import logging

import discord
from discord.ext import commands

log = logging.getLogger(__name__)


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Exports channel history")
    async def export(self, ctx):
        with open(f"c{ctx.channel.id}.txt"):
            await ctx.send("Here's the transcript!", file=discord.File(f"c{ctx.channel.id}.txt"))


def setup(bot):
    bot.add_cog(Core(bot))

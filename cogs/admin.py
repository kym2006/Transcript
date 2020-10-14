import logging

from typing import Optional

import discord

from discord.ext import commands

from utils import checks

log = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_admin()
    @commands.command(description="Make me say something.", usage="echo [channel] <message>", hidden=True)
    async def echo(self, ctx, channel: Optional[discord.TextChannel], *, content: str):
        channel = channel or ctx.channel
        await ctx.message.delete()
        await channel.send(content, allowed_mentions=discord.AllowedMentions(everyone=False))

    @checks.is_admin()
    @commands.command(description="Restart the bot.", usage="restart", hidden=True)
    async def restart(self, ctx):
        await ctx.send(embed=discord.Embed(description="Restarting...", colour=self.bot.primary_colour))
        await self.bot.logout()


def setup(bot):
    bot.add_cog(Admin(bot))

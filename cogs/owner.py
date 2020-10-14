import copy
import io
import logging
import subprocess
import textwrap
import traceback

from contextlib import redirect_stdout
from typing import Optional

import discord

from discord.ext import commands

from classes import converters
from utils import checks

log = logging.getLogger(__name__)


def cleanup_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @checks.is_owner()
    @commands.command(description="Load a module.", usage="load <cog>", hidden=True)
    async def load(self, ctx, *, cog: str):
        try:
            self.bot.load_extension(cog)
            await ctx.send(
                embed=discord.Embed(description="Successfully loaded the module.", colour=self.bot.primary_colour)
            )
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"Error: {e}", colour=self.bot.error_colour))

    @checks.is_owner()
    @commands.command(description="Unload a module.", usage="unload <cog>", hidden=True)
    async def unload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            await ctx.send(
                embed=discord.Embed(description="Successfully unloaded the module.", colour=self.bot.primary_colour)
            )
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"Error: {e}", colour=self.bot.error_colour))

    @checks.is_owner()
    @commands.command(description="Reload a module.", usage="reload <cog>", hidden=True)
    async def reload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            await ctx.send(
                embed=discord.Embed(description="Successfully reloaded the module.", colour=self.bot.primary_colour)
            )
        except Exception as e:
            await ctx.send(embed=discord.Embed(description=f"Error: {e}", colour=self.bot.error_colour))

    @checks.is_owner()
    @commands.command(name="eval", description="Evaluate code.", usage="eval <code>", hidden=True)
    async def _eval(self, ctx, *, body: str):
        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }
        env.update(globals())
        body = cleanup_code(body)
        stdout = io.StringIO()
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
        try:
            exec(to_compile, env)
        except Exception as e:
            await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{e.__class__.__name__}: {e}\n```",
                    colour=self.bot.primary_colour,
                )
            )
            return
        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            value = stdout.getvalue()
            await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{value}{traceback.format_exc()}\n```",
                    colour=self.bot.error_colour,
                )
            )
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("✅")
            except discord.Forbidden:
                pass
            if ret is None:
                if value:
                    await ctx.send(
                        embed=discord.Embed(description=f"```py\n{value}\n```", colour=self.bot.primary_colour)
                    )
            else:
                self._last_result = ret
                await ctx.send(
                    embed=discord.Embed(description=f"```py\n{value}{ret}\n```", colour=self.bot.primary_colour)
                )

    @checks.is_owner()
    @commands.command(description="Execute code in bash.", usage="bash <command>", hidden=True)
    async def bash(self, ctx, *, command_to_run: str):
        try:
            output = subprocess.check_output(command_to_run.split(), stderr=subprocess.STDOUT).decode("utf-8")
            await ctx.send(embed=discord.Embed(description=f"```py\n{output}\n```", colour=self.bot.primary_colour))
        except Exception as error:
            await ctx.send(
                embed=discord.Embed(
                    description=f"```py\n{error.__class__.__name__}: {error}\n```",
                    colour=self.bot.error_colour,
                )
            )

    @checks.is_owner()
    @commands.command(
        description="Invoke the command as another user and optionally in another channel.",
        usage="invoke [channel] <user> <command>",
        hidden=True,
    )
    async def invoke(self, ctx, channel: Optional[discord.TextChannel], user: converters.GlobalUser, *, command: str):
        msg = copy.copy(ctx.message)
        channel = channel or ctx.channel
        msg.channel = channel
        msg.author = channel.guild.get_member(user.id) or user
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))
        await self.bot.invoke(new_ctx)


def setup(bot):
    bot.add_cog(Owner(bot))

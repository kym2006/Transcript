import datetime
import logging

import discord

from discord.ext import commands

log = logging.getLogger(__name__)


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log.info(f"{self.bot.user.name}#{self.bot.user.discriminator} is online!")
        log.info("--------")
        embed = discord.Embed(
            title="Bot Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.bot.config.activity))

    @commands.Cog.listener()
    async def on_shard_ready(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Ready",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_shard_connect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Connected",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Disconnected",
            colour=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard):
        embed = discord.Embed(
            title=f"Shard {shard} Resumed",
            colour=self.bot.config.primary_colour,
            timestamp=datetime.datetime.utcnow(),
        )
        await self.bot.http.send_message(self.bot.config.event_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(
            title="Server Join",
            description=f"{guild.name} ({guild.id})",
            colour=0x00FF00,
            timestamp=datetime.datetime.utcnow(),
        )
        guilds = len(self.bot.guilds)
        embed.set_footer(text=f"{guilds} servers")
        await self.bot.http.send_message(self.bot.config.join_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = discord.Embed(
            title="Server Leave",
            description=f"{guild.name} ({guild.id})",
            colour=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        guilds = len(self.bot.guilds)
        embed.set_footer(text=f"{guilds} servers")
        await self.bot.http.send_message(self.bot.config.join_channel, None, embed=embed.to_dict())

    @commands.Cog.listener()
    async def on_message(self, message):
        with open(f"c{message.channel.id}.transcript", "a+") as f:
            f.write(f"{message.author.name}#{message.author.discriminator}: {message.content}\n")
        if message.author.bot:
            return
        ctx = await self.bot.get_context(message)
        if not ctx.command:
            return
        if message.guild:
            permissions = message.channel.permissions_for(message.guild.me)
            if permissions.send_messages is False:
                return
            elif permissions.embed_links is False:
                await message.channel.send("The Embed Links permission is needed for basic commands to work.")
                return
        if ctx.command.cog_name in ["Owner", "Admin"] and (
            ctx.author.id in self.bot.config.admins or ctx.author.id in self.bot.config.owners
        ):
            embed = discord.Embed(
                title=ctx.command.name.title(),
                description=ctx.message.content,
                colour=self.bot.primary_colour,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(name=f"{ctx.author} ({ctx.author.id})", icon_url=ctx.author.avatar_url)
            await self.bot.http.send_message(self.bot.config.admin_channel, None, embed=embed.to_dict())
        if ctx.prefix == f"<@{self.bot.user.id}> " or ctx.prefix == f"<@!{self.bot.user.id}> ":
            ctx.prefix = self.bot.config.default_prefix
        await self.bot.invoke(ctx)


def setup(bot):
    bot.add_cog(Events(bot))

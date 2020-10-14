import logging

from discord.ext import commands

log = logging.getLogger(__name__)


def is_owner():
    def predicate(ctx):
        if ctx.author.id not in ctx.bot.config.owners:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)


def is_admin():
    def predicate(ctx):
        if ctx.author.id not in ctx.bot.config.admins and ctx.author.id not in ctx.bot.config.owners:
            raise commands.NotOwner()
        else:
            return True

    return commands.check(predicate)

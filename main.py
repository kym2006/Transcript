import asyncio
import logging

from discord.ext import commands

import config
from classes.bot import Transcript

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="botlog.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)

log = logging.getLogger(__name__)


bot = Transcript(
    command_prefix=commands.when_mentioned_or(config.default_prefix),
    case_insensitive=True,
    help_command=None,
    owner_id=config.owner,
    heartbeat_timeout=300,
    version="1.0.0",
)


@bot.event
async def on_message(_):
    pass


loop = asyncio.get_event_loop()
loop.run_until_complete(bot.start_bot())

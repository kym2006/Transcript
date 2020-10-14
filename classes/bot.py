import datetime
import logging
import sys
import traceback

from discord.ext import commands
from utils import tools

import config

log = logging.getLogger(__name__)


class Transcript(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = datetime.datetime.utcnow()
        self.version = kwargs.get("version")

    @property
    def uptime(self):
        return datetime.datetime.utcnow() - self.start_time

    @property
    def config(self):
        return config

    @property
    def tools(self):
        return tools

    @property
    def primary_colour(self):
        return self.config.primary_colour

    @property
    def error_colour(self):
        return self.config.error_colour

    async def start_bot(self):
        for extension in self.config.initial_extensions:
            try:
                self.load_extension(extension)
            except Exception:
                log.error(f"Failed to load extension {extension}.", file=sys.stderr)
                log.error(traceback.print_exc())
        await self.start(self.config.token)

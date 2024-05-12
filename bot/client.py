
from typing import Coroutine
from discord.ext import commands
import datetime
import discord

from .lib.gpt import Gpt

import sqlite3


class ChatDefender(commands.Bot):
  
  def __init__(self, **options):
    
    # get the current time and set it as the start time for uptime tracking
    self.start_time = datetime.datetime.now()
    
    # set the database object
    self.db = None
    
    # set the gpt object
    self.gpt = Gpt()
    
    intents = discord.Intents.all()

    super().__init__(command_prefix=self._determine_prefix,
                     options=options,
                     intents=intents)
    
  async def setup_hook(self):
    await self.load_extension('bot.extensions.init')
    self._db_connect()
    return await super().setup_hook()
    
  def _determine_prefix(self, client, message):
    return '?'
  
  def _db_connect(self):
    self.db = sqlite3.connect('root.db')
    
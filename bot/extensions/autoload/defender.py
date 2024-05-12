from ...client import ChatDefender
from discord.ext import commands
from discord import Message
from discord.ext.commands import Context

from ...lib.gpt import Gpt

class Defender(commands.Cog, name="Defender"):
  """
  Provides an AI based content filter to the discord bot
  """
  
  def __init__(self, client):
    self.client : ChatDefender = client
    self.gpt : Gpt = client.gpt
    # Get all the channels that are setup for chat filtering from the database
    self.filter_channels = []
    self.translation_channels = []
    self._build_cache()
    
    
  def _build_cache(self):
    
    cursor = self.client.db.cursor()
      
    # Get all the saved channels that we're filtereing
    query = "SELECT channel_id from FilteredChannels"
    translation_query = "SELECT channel_id from TranslationChannels"
    
    # excecute
    cursor.execute(query)    

    channels = cursor.fetchall()
    self.filter_channels = [int(x[0]) for x in channels]
    
    # excecute
    cursor.execute(translation_query)    

    channels = cursor.fetchall()
    self.translation_channels = [int(x[0]) for x in channels]
  
    return
  
  def _remove_cache(self, channel_id):
    
    cursor = self.client.db.cursor()
    
    query = f"DELETE FROM FilteredChannels WHERE channel_id = {channel_id}"
    
    cursor.execute(query)
    self.filter_channels.remove(channel_id)

    return
    
  def _remove_translation_cache(self, channel_id): 
    cursor = self.client.db.cursor()
    
    query = f"DELETE FROM TranslationChannels WHERE channel_id = {channel_id}"
    
    cursor.execute(query)
    self.translation_channels.remove(channel_id)
    
    return
  
  def _append_cache(self, channel_id):
    
    cursor = self.client.db.cursor()
    
    query = f"INSERT INTO FilteredChannels (channel_id) VALUES ('{channel_id}')"
    
    cursor.execute(query)
    self.filter_channels.append(channel_id)
    
    return
  
  def _append_translation_cache(self, channel_id):
      
      cursor = self.client.db.cursor()
      
      query = f"INSERT INTO TranslationChannels (channel_id) VALUES ('{channel_id}')"
      
      cursor.execute(query)
      self.translation_channels.append(channel_id)
      
      return
    
  # Returns true if the content should be filtered and false if it should not.
  def content_filter(self, message):
    verdict, justification = self.gpt.is_hate_speech(message)
    return verdict, justification
    
  @commands.Cog.listener()
  async def on_message(self, message: Message):

    # Ignore if the message author is a bot user. 
    if message.author.bot:
      return
    
    # Check if the channel is in the filter list.
    if message.channel.id not in self.filter_channels:

      # Check the message content for hate speech
      verdict, justification = self.content_filter(message.content)

      # If there is hate speech then simply delete it
      if (verdict == 'True'):
        await message.delete()
        mention = message.author.mention  # Mention the person who sent the message
        await message.channel.send(content=f"{mention}, {justification}")
        return
    
    if message.channel.id in self.translation_channels:
      # Translate the message
      translated_message = self.gpt.translate_text(message.content) 
      if(translated_message != message.content):
        await message.delete()
        await message.channel.send(message.author.display_name + ": " +translated_message)
        
    return
      

  @commands.command("fallacies", brief="Detect fallacies", help="Detect fallacies in the conversation")
  async def detect_fallacy_command(self, ctx: Context):
    # get all the messages in the channel
    channelmessages = ctx.channel.history(limit=100)
    summarymessages: list[Message] = []
    totalchars = 0
    
    previous_msg = None
    async for msg in channelmessages:
      
      # should skip bot messages and command messages
      if msg.author.bot or msg.clean_content.startswith('?'):
        continue
      totalchars += len(msg.clean_content)

      # concatenates messages that were sent by the same author many times in a row
      if previous_msg and previous_msg.author.id == msg.author.id:
        summarymessages[len(summarymessages) - 1] = summarymessages[len(summarymessages) - 1] + ". " + msg
      else:
        summarymessages.append(msg)
    
      if (totalchars >= 4000):
        break
  
    summarymessages = [f"{x.author.display_name}: {x.clean_content} [{x.created_at}]" for x in summarymessages][::-1]
    summarymessages = "\n".join(summarymessages)
    
    # Send to the summarise function from openai lib
    summary = self.gpt.detect_fallacy(summarymessages)
    await ctx.message.reply(summary)

  @commands.command("summarize", brief="Summarize the conversation", help="Summarize the conversation in the current channel")
  async def summary_command(self, ctx: Context):
  
    # get all the messages in the channel
    channelmessages = ctx.channel.history(limit=100)
    
    summarymessages: list[Message] = []
    totalchars = 0
    
    async for msg in channelmessages:
      totalchars += len(msg.clean_content)
      summarymessages.append(msg)
    
      if (totalchars >= 4000):
        break
    
  
    summarymessages = [f"{x.author.display_name}: {x.clean_content} [{x.created_at}]" for x in summarymessages][::-1]
    summarymessages = "\n".join(summarymessages)
    
    # Send to the summarise function from openai lib
    summary = self.gpt.summerize_converstaion(summarymessages)
    
    await ctx.message.reply(summary)
    
  @commands.command("askgpt", brief="Ask GPT a question", help="Ask GPT-3 a question and get a response.")
  async def gpt(self, ctx: Context, *, prompt: str):
        response = self.gpt.ask_gpt(prompt)
        await ctx.reply(response)
  
  @commands.command("check-grammar", brief="Check grammar", help="Check the grammar of a given text.")
  async def grammar_check(self, ctx: Context, *, text: str = ""):
    response = self.gpt.grammar_check(text)
    await ctx.send(response)
    
  @commands.command("togglefilter", brief="Toggle the filter", help="Toggle the filter on the current channel")
  async def toggle_filter(self, ctx: Context):
    
    channel_id = ctx.channel.id
    
    if channel_id in self.filter_channels:
      self._remove_cache(channel_id)
      await ctx.reply('channel is now being filtered')
      
    else:
      self._append_cache(channel_id)
      await ctx.reply('channel is no longer being filtered')
  
    return
  
  @commands.command("toggletranslate", brief="Toggle the translation", help="Toggle the translation on the current channel")
  async def toggle_translate(self, ctx: Context):
    
    channel_id = ctx.channel.id
    
    if channel_id in self.translation_channels:
      self._remove_translation_cache(channel_id)
      await ctx.reply('channel is no longer being translated')
      
    else:
      self._append_translation_cache(channel_id)
      await ctx.reply('channel is now being translated')
  
    return
     
async def setup(client: ChatDefender):
  await client.add_cog(Defender(client))
  return
from discord import app_commands
import discord

async def hello_world(interaction, message: discord.Message):
  await interaction.response.send_message('hello world')

async def fact_check(interaction, message: discord.Message):
  
  # Send the message to the fact checker function
  fact = 'fact func'
  
  await interaction.response.send_message(fact)

async def translate(interaction: discord.Interaction, message: discord.Message):
  
  # get the translation from the function
  translation = 'translate function'
  
  await interaction.response.send_message(ephemeral=True, content=translation)

async def setup(client):
  hello_context_command = app_commands.ContextMenu(
    name="hello world",
    callback=hello_world
  )
  client.tree.add_command(hello_context_command)
  
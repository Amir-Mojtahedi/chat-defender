from discord import app_commands
import discord

async def fact_check(interaction, message: discord.Message):
  
  # Send the message to the fact checker function
  fact = interaction.client.gpt.fact_check(message.content)
  
  await interaction.response.send_message(ephemeral = True, content = fact)

async def translate(interaction: discord.Interaction, message: discord.Message):
  
  # get the translation from the function
  translation = interaction.client.gpt.translate_text(message.content)
  
  await interaction.response.send_message(ephemeral=True, content=translation)

async def grammar_check(interaction: discord.Interaction, message: discord.Message):
  
  # Get the grammar checked version
  grammar = interaction.client.gpt.grammar_check(message.content)
  await interaction.response.send_message(ephemeral=True, content=grammar)

async def setup(client):
  
  fact_check_cmd = app_commands.ContextMenu(
    name="Fact Check",
    callback=fact_check
  )
  
  grammar_check_cmd = app_commands.ContextMenu(
    name = 'Grammar Check',
    callback=grammar_check
  )
  
  translate_cmd = app_commands.ContextMenu(
    name = "Translate",
    callback = translate
  )
  
  client.tree.add_command(translate_cmd)
  client.tree.add_command(fact_check_cmd)
  client.tree.add_command(grammar_check_cmd)
  client.tree.add_command(hello_context_command)
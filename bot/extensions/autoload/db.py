from ...client import ChatDefender
import os
import sys

SETUP_SCRIPT = """
CREATE TABLE IF NOT EXISTS Config (
	config_guild_snowflake TEXT NOT NULL,
	config_key TEXT NOT NULL,
	config_value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS FilteredChannels(
	channel_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS TranslationChannels(
	channel_id TEXT PRIMARY KEY
);
"""


async def setup(client: ChatDefender):

  cursor = client.db.cursor()
  cursor.executescript(SETUP_SCRIPT)
  cursor.close()
  # check if the database file exists
  if os.path.exists('root.db'):
    # check if all the tables exist in the database
    query = """SELECT name FROM sqlite_master
    WHERE type='table';"""
    
    cursor = client.db.cursor()
    cursor.execute(query)

    tables = cursor.fetchall()
    tables = [x[0] for x in tables]
    print(tables)
    if 'Config' not in tables or 'FilteredChannels' not in tables or 'TranslationChannels' not in tables:
      print("DB IS MISCONFIGURED")
      sys.exit()  
      
  else:
    
    print("DB DOES NOT EXIST")
    sys.exit()
    
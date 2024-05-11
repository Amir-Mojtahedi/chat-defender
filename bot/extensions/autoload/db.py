from client import ChatDefender
import os
async def setup(client: ChatDefender):
  
  # check if the database file exists
  if os.path.exists('root.db'):

    # check if all the tables exist in the database
    return
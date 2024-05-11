import os 
from client import ChatDefender

async def autoload(client : ChatDefender):
  
  exts = [f.split('.py')[0] for f in os.listdir('./bot/extensions/autoload') if f.endswith('.py')]
  
  for ext in exts:
    
    await client.load_extension(f'extensions.autoload.{ext}')
    
  if len(exts) <= 0:
    print("\nNo extensions were automatically loaded.")

  if len(exts) == 1:
    print(f'\n1 extension was automatically loaded.')

  if len(exts) > 1:
    print(f"\n{len(exts)} extensions were automatically loaded.")
    
    
async def setup(client: ChatDefender):
  
  async def ready_event():
    
    await client.wait_until_ready()
    
    await autoload(client)

    await client.load_extension('jishaku')
    
    print(f'\nLogged in as {client.user}')
    print('ready')
    
  client.loop.create_task(ready_event())

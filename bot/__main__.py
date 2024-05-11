from client import ChatDefender

from sys import version as pyversion
import platform

import setup
import dotenv
dotenv.load_dotenv('.env')

client = ChatDefender()

client.__version__ = '1.0.0'


print(f"ChatDefender v{client.__version__}")
print(f"Running on {platform.platform().title()}\nPython v{pyversion}")

client.run(setup.TOKEN)
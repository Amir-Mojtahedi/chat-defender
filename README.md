# chat-defender
ChatDefender is the ultimate AI-powered moderation discord bot.

## How to run it

First thing you should do is create a venv and install all the requirements in a terminal.

```
python3 -m venv .venv
```
Then, activate the venv

linux: 
```
source ./.venv/bin/activate
```

windows:
```
.\.venv\scripts\activate
```

then install all requirements

```
pip install -r requirements.txt
```
Next you need 2 things, an OpenAI secret key, and discord bot secret token.

You can get a bot token by going to the "discord developer portal" and creating a new application in the sidebar. Then, again in the side bar you will see "bot" where you can create your bot account and copy the token.

For openAI API secret key, search up openai API and create your account, add funds to it and then get a secret key in the secret keys tab on the side.

Place your openAI secret in a .env file at the root of the project

```
OPENAI_API_KEY=sk-proj-secretkeyhere
```

Place your bot token in a file called `setup.py` in the `bot` folder

```
TOKEN='TOKEN_HERE'
```

You're done setup!

simply run the bot in the root folder of the project like so

```
python3 -m bot
```

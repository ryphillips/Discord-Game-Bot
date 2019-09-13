# Discord Game Bot
# ryphillips 2019
from os import environ
from os.path import dirname, join
from dotenv import load_dotenv
import discord
from discord.ext.commands import Bot
from cogs import GamesCog, ListenersCog

load_dotenv(join(dirname(__file__), '.env'))

BOT = Bot(command_prefix=['!', '$'],
          help_command=None,
          description='Cool commands for discord!')

BOT.add_cog(GamesCog(BOT))
BOT.add_cog(ListenersCog(BOT))

@BOT.event
async def on_ready():
  '''Adjust instructions for when bot is booted'''
  await BOT.change_presence(status=discord.Status.idle,
                            activity=discord.Game('Dark Souls 3'))

if __name__ == '__main__':
  try:
    print('\nThe bot is now active\nPress (ctrl c) to deactivate and exit\n')
    BOT.run(environ.get('DISCORD_CLIENT_ID'))
  except:
    print('\nNetwork connectivity error!\\n')

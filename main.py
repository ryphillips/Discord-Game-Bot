# Discord Game Bot
# ryphillips ©2019
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

BOT.add_cog(GamesCog(BOT)) # game commands
BOT.add_cog(ListenersCog(BOT)) # listeners

@BOT.event
async def on_ready():
  '''When the bot is booted'''
  await BOT.change_presence(status=discord.Status.idle,
                            activity=discord.Game('Dark Souls 3'))

if __name__ == '__main__':
  print('The Bot is now live\nPress ctrl c to turn it off')
  BOT.run(environ.get('DISCORD_CLIENT_ID')) # this method blocks

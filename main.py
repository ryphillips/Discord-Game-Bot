# Discord Game Bot
# ryphillips ©2019
from os import environ
from os.path import dirname, join
from dotenv import load_dotenv
from discord.ext.commands import Bot
from cogs import GamesCog

load_dotenv(join(dirname(__file__), '.env'))

bot = Bot(command_prefix=['!', '$'],
            help_command=None,
            description='Cool commands for discord!')

bot.add_cog(GamesCog(bot))

if __name__ == '__main__':
  bot.run(environ.get('DISCORD_CLIENT_ID')) # this method blocks

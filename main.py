# Discord Game Bot
# Ryan Phillips ©2019
from os import environ
from os.path import dirname, join
from dotenv import load_dotenv
from discord.ext.commands import Bot
from cogs import GameCog

load_dotenv(join(dirname(__file__), '.env'))
bot = Bot(command_prefix=['!', '$'],
          description='Cool commands for games!')

if __name__ == '__main__':
  bot.add_cog(GameCog(bot))
  bot.run(environ.get('DISCORD_CLIENT_ID'))


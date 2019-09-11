from discord.ext import commands

class ListenersCog(commands.Cog, name='Listeners'):
  '''All Listeners for the bot'''
  def __init__(self, bot: commands.Bot, **options):
    self.bot = bot
    self.options = options

  @commands.Cog.listener()
  async def on_message(self, message):
    '''
    @listener
    When any member sends a message
    '''
    pass

  @commands.Cog.listener()
  async def on_member_join(self, member):
    '''
    @listener
    When a member joins a guild wwhere the bot is active
    '''
    pass

from os import environ
from json import loads
from aiohttp import ClientSession, ClientError
from discord.ext import commands
import discord
from .utils import time_delta_str_tuple

class GamesCog(commands.Cog, name='Game'):
  '''Game Cog - Commands for game related information'''
  def __init__(self, bot, **options):
    '''
    @constructor
      bot - the bot ref that the cog will send messages through
    '''
    self.bot = bot
    self.last_command = None
    self.last_member = None
    self.last_result = None
    self.last_result_was_error = False
    self.last_target = None
    self.options = options

  def __repr__(self):
    return f'Discord Cog {hex(id(self))}'

  def __str__(self):
    if self.last_target is None or self.last_result_was_error:
      return self.bot.__str__()
    return f'Games Cog currently looking at {self.last_target}'

  def __iter__(self):
    if self.last_result is not None and self.last_result:
      return self.last_result[self.last_target].items()
    return dict().items()

  def _update_state(self,
                    command: str,
                    target: str,
                    result: dict,
                    member: discord.Member,
                    err: bool) -> None:
    '''
    @private
    Updates the state of the cog
    '''
    self.last_target = target
    self.last_command = command
    self.last_member = member
    self.last_result = result
    self.last_result_was_error = err

  @commands.command()
  async def when(self, ctx, *args, member: discord.Member = None) -> None:
    '''
    @command: !when

    e.g. !when "game name"

    Replies with the time until the game argument is released
    '''
    if not args:
      ctx.send('when command example -> !when borderlands 3')
      return

    member = member if member is not None else ctx.author
    game_name = str(' ').join(args)
    game, err = await async_query_igdb('games', game_name, 'name,first_release_date')

    self._update_state('date', game_name, game, member, bool(err))

    timestamp = game.get('first_release_date', False)
    if err is not None or not timestamp:
      await ctx.send(f'Sorry, I was unable to find the release date for {game_name}')
      return

    days, hours, mins, secs = time_delta_str_tuple(timestamp)
    msg = f'{game_name} releases in {days}, {hours} hours, {mins} mins, and {secs} seconds!'
    await ctx.send(msg)


async def async_query_igdb(e_point: str, target: str, filters: str) -> tuple:
  '''
  Makes an ansynchronous network request to an igdb endpoint

  Returns a tuple containg two items (RequestResponse, Error)

  @params:
    e_point - the specific endpoint for igdb request
    target - the item you are searching for in the end point
    filters - comma seperated values used to filter the result

  @igdb docs:
    https://api-docs.igdb.com

  '''
  if not (isinstance(target, str) and
          isinstance(e_point, str) and
          isinstance(filter, str)):
    return {}, TypeError('All arguments must be ')

  if not target or not e_point:
    # no game was specified
    return {}, ValueError('Target or endpoint was empty')

  url = f'https://api-v3.igdb.com/{e_point}?search={target}&fields={filters}'
  headers = {'user-key': environ.get('IGDB_KEY')}

  async with ClientSession(headers=headers, raise_for_status=False) as sess:
    try:
      async with sess.get(url, raise_for_status=True) as res:
        data = loads(await res.read())[0]
    except (ClientError, IndexError) as ex:
      if not sess.closed:
        await sess.close()
      return {}, ex
    else:
      return data, None

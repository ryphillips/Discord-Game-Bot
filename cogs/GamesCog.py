# Games Cog
# ryphillips ©2019

from os import environ
from json import loads
from aiohttp import ClientSession, ClientError
from discord.ext import commands
import discord
from utils import time_delta_tuple, make_game_embed

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
          isinstance(filters, str)):
    return {}, TypeError('All arguments must be strings')

  if not target or not e_point:
    # no game was specified
    return {}, ValueError('Target or endpoint is empty')

  url = f'https://api-v3.igdb.com/{e_point}?search={target}&fields={filters}'
  headers = {'user-key': environ.get('IGDB_KEY')}

  async with ClientSession(headers=headers, raise_for_status=False) as sess:
    try:
      async with sess.get(url, raise_for_status=True) as res:
        data = loads(await res.read())
    except (ClientError, IndexError) as ex:
      if not sess.closed:
        await sess.close()
      return {}, ex
    else:
      if not data:
        return {}, Exception()
      return data[0], None

class GamesCog(commands.Cog, name='Games'):
  '''Game Cog - Commands for game related information'''
  def __init__(self, bot: commands.Bot, **options):
    '''
    @constructor
      bot - the bot ref that the cog will send messages through
    '''
    self.bot = bot
    self.last_command = None
    self.last_member = None
    self.last_result = None
    self.last_target = None
    self.options = options

  def __repr__(self):
    return f'Discord Cog {hex(id(self))}'

  def __str__(self):
    if self.last_target is None:
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
                    member: discord.Member) -> None:
    '''
    @private
    Updates the state of the cog
    '''
    self.last_target = target
    self.last_command = command
    self.last_member = member
    self.last_result = result

  @commands.command(name='when')
  async def when(self, ctx, *args, member: discord.Member = None) -> None:
    '''
    @command: !when

    e.g. !when "game name"

    Replies with the time until the game argument is released
    '''
    if not args:
      await ctx.send('when command example -> !when borderlands 3')
      return

    game_name = str(' ').join([str(arg).title() for arg in args])
    await self.bot.change_presence(status=discord.Status.online,
                                   activity=discord.Game(game_name))

    member = member if member is not None else ctx.author
    filters = 'name,first_release_date,cover.url,genres.name,involved_companies.company.name'
    game, err = await async_query_igdb('games', game_name, filters)
    timestamp = game.get('first_release_date', False)

    if err is not None or not timestamp:
      await ctx.send(f'Sorry, I was unable to find the release date for {game_name}')
      return

    # known to be a valid result for the !when command
    self._update_state('date', game_name, game, member)
    days, hours, mins, secs = time_delta_tuple(timestamp)
    
    if days < 0:
      await ctx.send(f'{game_name} has already been released!')
      return

    countdown = '{} countdown:\n{} days, {} hours, {} mins, and {} seconds!'.format(game_name,
                                                                                    days,
                                                                                    hours,
                                                                                    mins,
                                                                                    secs)
    await ctx.send('', embed=make_game_embed(game, game_name, countdown))
    await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game(game_name))

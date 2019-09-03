import os
import asyncio
from aiohttp import ClientSession, ClientError
from json import loads
from discord.ext import commands
import discord
from .utils import time_delta_str_tuple

class GameCog(commands.Cog):
  '''
  Game Cog - Commands for game related information
  '''
  def __init__(self, bot):
    '''
    @constructor
    @params:
      bot (discord.Bot) - the bot ref that the cog will be added to
    '''
    self.bot = bot
    self.last_command = None
    self.last_member = None
    self.last_result = None

  def __repr__(self):
    return f'{hex(id(self))}'
  def __iter__(self):
    if self.last_result is not None and self.last_result:
      return self.last_result[self.last_target].items()
    return iter([])

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
    self.last_result =  result
    self.last_result_was_error = err

  @commands.command()
  async def date(self, ctx, *args, member: discord.Member = None) -> None:
    '''
    Attempts to send the time until release for the game argument
    
    @params:
      ctx - provided by discord to send messages with the bot
      *args - what the client types after !date
      member (discord.Member) - discord provided member
    '''
    if len(args) == 0:
      return

    member = member if member is not None else ctx.author
    game_name = str(' ').join(args)
    game, err = await async_query_igdb('games',
      game_name, 'name,first_release_date')
    timestamp = game.get('first_release_date', False)

    self._update_state('date', game_name, game, member, err)

    if err is not None or not timestamp:
      await ctx.send(f'Sorry, I was unable to find the release date for {game_name}')
    else:
      days, hours, minutes, seconds = time_delta_str_tuple(timestamp)
      await ctx.send(f'{game_name} releases in {days}, {hours} hours, {minutes} mins, and {seconds} seconds!')


async def async_query_igdb(e_point: str, target: str, filters: str) -> tuple:
  '''
  Makes an ansynchronous network request to an igdb endpoint

  @params:
    e_point (str) - the specific endpoint for igdb request
    target (str) - the item you are searching for in the end point
    filters (str) - comma seperated values used to filter the result
    https://api-docs.igdb.com

  @return:
    Returns a tuple containg two items (RequestResponse, Error)
  '''
  if len(target) == 0 or len(e_point) == 0:
    return {}, ValueError()

  url = f'https://api-v3.igdb.com/{e_point}?search={target}&fields={filters}'
  headers = { 'user-key': os.environ.get('IGDB_KEY') }

  async with ClientSession(headers=headers, \
      raise_for_status=False) as sess:
    try:
      async with sess.get(url, raise_for_status=True) as res:
        data = loads(await res.read())[0]
    except (ClientError, IndexError) as ex:
      if not sess.closed:
          await sess.close()
      return {}, ex
    else:
      return data, None

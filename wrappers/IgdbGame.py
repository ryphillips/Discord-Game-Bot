'''
ryphillips 2019
Igdb Game object Wrapper for python
'''
from copy import deepcopy
import discord

class IgdbGame(object):
  '''Wraps a igdb game query response into a valid python object'''
  def __init__(self, json: dict):
    self._json = None
    self.json = json


  @property
  def json(self) -> dict:
    return self._json

  @json.setter
  def json(self, json: dict) -> None:
    if not isinstance(json, dict):
      raise TypeError('Json property must be a dictionary')
    self._json = deepcopy(json) if json else {}

  def to_embed(self) -> discord.Embed:
    pass

  @property
  def companies(self) -> list:
    '''Returns a list of all the invlved companies'''
    if not self._json.get('involved_companies', False):
      return []
    return [x['company']['name'] for x in self.json['involved_companies']]

  @property
  def genres(self) -> list:
    '''Returns a list of all the genres for the game'''
    if not self._json.get('genres', False):
      return ['None']
    return [x['name'] for x in self.json['genres']]

  @property
  def big_image(self) -> str:
    '''Returns a full sized cover image url'''
    return self.small_image.replace('t_thumb', 't_cover_big') if self.small_image else ''

  @property
  def small_image(self) -> str:
    '''Returns a thumbnail sized cover image url'''
    if self.json.get('cover', False):
      return 'https:' + self.json['cover']['url']
    return ''

  def copy(self) -> dict:
    '''Returns a deep copy of the json data'''
    return deepcopy(self.json)

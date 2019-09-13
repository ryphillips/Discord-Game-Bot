'''
ryphillips 2019
Igdb Game object Wrapper for python
'''
from copy import deepcopy

def check_json_val(function):
  def wrap(*args):
    print(args, function)
  return wrap

class IgdbGame(object):
  '''Wraps a igdb game query response into a valid python object'''
  def __init__(self, json: dict):
    if not isinstance(json, dict):
      raise TypeError('json data must be in a dictionary')
    self.json = deepcopy(json) if json else None

  @property
  def json(self) -> dict:
    return self.json

  @json.setter
  def json(self, json: dict) -> None:
    if not isinstance(json, dict):
      raise TypeError('Json argument must be a dict')
    self.json = deepcopy(json)

  @property
  def companies(self) -> list:
    '''Returns a list of all the invlved companies'''
    if not self.json.get('involved_companies', False):
      return []
    return [x['company']['name'] for x in self.json['involved_companies']]

  @property
  def genres(self) -> list:
    '''Returns a list of all the genres for the game'''
    if not self.json.get('genres', False):
      return []
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

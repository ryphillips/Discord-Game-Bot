'''
Ryan Phillips 2019 ©

Igdb Game object Wrapper for python
'''

class IgdbGame(object):
  '''Wraps a igdb game query response into a valid python object'''
  def __init__(self, json: dict, **opt):
    self.json = json
    self.opt = opt

  @property
  def companies(self) -> str:
    '''Returns a list of all the invlved companies'''
    pass

  @property
  def genres(self):
    '''Returns a list of all the genres for the game'''
    if not self.json.get('genres')
    pass

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

  def copy(self):
    '''Returns a shallow copy of the json data'''
    return self.json.copy()








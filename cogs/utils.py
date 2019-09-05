from datetime import datetime
import discord

def time_delta_tuple(timestamp: datetime.timestamp) -> tuple:
  '''Returns a datetime time delta tuple'''
  delta = datetime.fromtimestamp(timestamp) - datetime.now()
  times = str(delta).split(', ')

  if len(times) == 1:
    hours, minutes, seconds = times[0].split(':')
    return 0, int(hours), int(minutes), float(seconds)

  days = times[0].split(' ')[0]
  hours, minutes, seconds = times[1].split(':')
  return int(days), int(hours), int(minutes), float(seconds)


def make_game_embed(game: dict, title: str, description: str, **options) -> discord.Embed:
  '''
  @private
  Creates a new embeded message w/ game meta info
  '''
  embed = discord.Embed(title=title,
                        description=description,
                        colour=1024228,
                        type='rich')

  for key, value in options.items():
    embed.add_field(name=key, value=game.get(key, value))

  if game.get('cover', None) is not None:
    game_pic_sm = 'https:'+game['cover']['url']
    game_pic_lg = game_pic_sm.replace('t_thumb', 't_cover_big', 1)
    embed.set_image(url=game_pic_lg)

    genres = ''
    if game.get('genres', None) is not None and game['genres']:
      for genre in game['genres']:
        if genres:
          genres += ', '
        genres += genre['name']

    if not genres:
      genres = 'Any'

    embed.add_field(name='Genres', value=genres)
    git = 'Powered by https://github.com/ryphillips/DiscordBot/blob/master/cogs/GamesCog.py'
    embed.set_footer(text=git, icon_url=game_pic_sm)

  return embed

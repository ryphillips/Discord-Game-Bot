from datetime import datetime

def time_delta_str_tuple(timestamp: datetime.timestamp) -> tuple:
  delta = datetime.fromtimestamp(timestamp) - datetime.now()
  times = str(delta).split(', ')
  days = times[0]
  hours, minutes, seconds = times[1].split(':')
  return days, hours, minutes, seconds
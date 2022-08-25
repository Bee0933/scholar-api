# helper functions
from datetime import datetime, date, timedelta


# search text formating
def format_search_text(txt : str) -> str:
      text_list = txt.replace(' ', '+')
      return text_list

# format date
def time_post(post_time_str : str) -> datetime:
      num = [int(s) for s in post_time_str.split() if s.isdigit()]
      current_date = date.today() 
      actual_date = current_date - timedelta(days=num[0])
      post_time = actual_date
      return post_time



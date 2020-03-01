#from bot.src.cleaner import *
#from bot.trimming.main import *

from main import tweet_collect
from test_connection import is_connected

if(is_connected()):
    tweet_collect()




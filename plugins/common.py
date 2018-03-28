import threading
import time


# todo - this file should not be inside "plugin " dir.

def is_number(s):
    try:
        a = float(s)
        return a
    except:
        return None

class AvgCalc(object):
    
    def __init__(self):
        self._total_num = 0
        self._count = 0.0

    def add(self, num):
        self._total_num  +=  num
        self._count += 1

    def get_avg(self):
        return self._total_num/self._count
    

class UsersAvgManager(object):

	lock = threading.Lock()
	_total_num = 0
	_total_count = 0.0
	users_avg = dict()
	last_updated_ts = -1
	last_reported_ts = -1  # holds the last time the bot reported 

	@classmethod
	def add(cls, user_id, num):
		with cls.lock:
			cls._total_num += num
			cls._total_count += 1

			cls.users_avg.setdefault(user_id, AvgCalc())
			cls.users_avg[user_id].add(num)
			cls.last_updated_ts = time.time()

	@classmethod
	def get_total_avg(cls):
		with cls.lock:
			if cls.last_updated_ts > cls.last_reported_ts:
				cls.last_reported_ts = time.time()
				return cls._total_num/cls._total_count
		return None

	@classmethod
	def get_user_avg(cls, user_id):
		return cls.users_avg[user_id].get_avg()


class ChannelsManager(object):
	channels_per_user = dict()

	@classmethod
	def add(cls, user, channel):
		cls.channels_per_user[user] = channel

	# todo - there might be closed channels or channels we've missed
	@classmethod 
	def get_channels(cls):
		return cls.channels_per_user.values()
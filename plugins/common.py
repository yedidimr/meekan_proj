import threading
import time


# todo - this file should not be inside "plugin " dir.



def is_number(s):
    """
    checks if a string is a number , and returns that number
    """
    try:
        a = float(s)
        return a
    except:
        return None

class AvgCalc(object):
    """
    calculates total average by saving only two numbers - 
       the total numbers added untill now and the amount of numbers added
    """
    
    def __init__(self):
        self._total_num = 0
        self._count = 0.0

    # adds new number to the average
    def add(self, num):
        self._total_num  +=  num
        self._count += 1

    # calculates and returns the average so far
    def get_avg(self):
        return self._total_num/self._count
    

class UsersAvgManager(object):
    """
    manages the average for each user 
    """

    lock = threading.Lock()
    _total_num = 0            # total numbers added so far
    _total_count = 0.0        # the amount of numbers added so far
    users_avg = dict()        # average per user
    last_updated_ts = -1    # the last number addition timestamp
    last_reported_ts = -1   # the last time the bot reported total average

    @classmethod
    def add(cls, user_id, num):
        """
        adds new number to a user.
        adds it to the total average as well.
        """

        with cls.lock:  # locks the action (so that the timed job won't report before we finish updating)
            cls._total_num += num
            cls._total_count += 1

            cls.users_avg.setdefault(user_id, AvgCalc())
            cls.users_avg[user_id].add(num)

            cls.last_updated_ts = time.time()  # update last timestamp

    @classmethod
    def get_total_avg(cls):
        """
        returns the total average of all users, only if there were any new messages since the last time
        """

        with cls.lock:
            if cls.last_updated_ts > cls.last_reported_ts:
                cls.last_reported_ts = time.time()
                return cls._total_num/cls._total_count
        return None

    @classmethod
    def get_user_avg(cls, user_id):
        """
        returns the average of the requested user
        """
        return cls.users_avg[user_id].get_avg()


class ChannelsManager(object):
    """
    --- a patch to map user id to it's channel with the bot (implements a dict) ---

    I'm sure there are other ways to do it (ask for all the open channels)
    but didn't have time to look for it
    """
    channels_per_user = dict()

    @classmethod
    def add(cls, user, channel):
        cls.channels_per_user[user] = channel

    # todo - there might be closed channels or channels we've missed
    @classmethod 
    def get_channels(cls):
        return cls.channels_per_user.values()
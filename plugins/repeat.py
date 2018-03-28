from __future__ import print_function
from __future__ import unicode_literals
from rtmbot.core import Plugin
from common import UsersAvgManager, is_number, ChannelsManager

class CalcAvg(Plugin): 

        def process_message(self, data): # todo - there must be a way to register actions to process message
            if data['channel'].startswith("D") and data['type'] == 'message':

                # save new channels (there might be other way to get the existing channels, didn't have time to explore)
                ChannelsManager.add(data['user'], data['channel'])

                # check if msg is a number
                num = is_number(data['text'])
                if num is not None:
                    print("user", data['user'], "sent a number:", num)

                    # add new number
                    UsersAvgManager.add(data['user'], num)

                    # return the  average of the numbers the user wrote.
                    self.outputs.append([data['channel'], "your avg is" + str(UsersAvgManager.get_user_avg(data['user']))])



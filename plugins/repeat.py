from rtmbot.core import Plugin
from common import UsersAvgManager, is_number, ChannelsManager

class CalcAvg(Plugin): 
    """
    processes messages so that whenever the user writes a number, the bot sends back the average of the numbers the user wrote.
    """

    def process_message(self, data): 
        if data['channel'].startswith("D"):

            # save new channels (there might be other way to get the existing channels, didn't have time to explore)
            ChannelsManager.add(data['user'], data['channel'])

            # if the msg is a number - add it to the total average
            num = is_number(data['text'])
            if num is not None:
                print("user", data['user'], "sent a number:", num)

                # add the  number to the user
                UsersAvgManager.add(data['user'], num)

                # send back the  average of the numbers the user wrote so far
                self.outputs.append([data['channel'], "your avg is" + str(UsersAvgManager.get_user_avg(data['user']))])



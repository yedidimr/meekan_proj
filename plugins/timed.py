from rtmbot.core import Plugin, Job
from common import UsersAvgManager, is_number, ChannelsManager

JOB_WINDOW = 10  # in seconds


class ReportTotalAvgJob(Job):
    """
    reports the total average so far
    """

    def run(self, slack_client):
        print("job in action")
        avg = UsersAvgManager.get_total_avg()
        if avg is not None:
            return [[channel, "total users avg is " + str(avg)] for channel in ChannelsManager.get_channels()]



class JobRegister(Plugin):
    """
    registers job to the bot
    """

    def register_jobs(self):
        job = ReportTotalAvgJob(JOB_WINDOW)
        self.jobs.append(job)

from modules.essential.Core import Core
from modules.ping.Ping import Ping
from config.settings import features
from modules.class_check.CourseChecking import CourseChecking


def add_cogs(bot):
    bot.add_cog(Core(bot))
    if features.get('ping'):
        bot.add_cog(Ping(bot))
    if features.get('course_checking'):
        bot.add_cog(CourseChecking(bot))

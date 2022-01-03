from discord.ext import commands
from keep_alive import keep_alive
import os

#import all of the cogs
from main_cog import main_cog
from attributes import attributes

bot = commands.Bot(command_prefix='>')

#remove the default help command so that we can write our own version of it
bot.remove_command('help')

#register the class with the bot
bot.add_cog(main_cog(bot))
bot.add_cog(attributes(bot))

keep_alive()
#start the bot with our token
bot.run(os.environ['TOKEN'])
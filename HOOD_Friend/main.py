import os
from discord.ext import commands
from keep_alive import keep_alive
from main_cog import main_cog
from attributes import attributes
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

token = os.environ["TOKEN"]

bot = commands.Bot(command_prefix='=>')
bot.remove_command('help')
bot.add_cog(main_cog(bot))
bot.add_cog(attributes(bot))
#bot.add_cog(feats(bot))

keep_alive()

bot.run(token)

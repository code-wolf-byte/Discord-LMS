import discord
from discord.ext import commands
from main import Utilities

print(discord.__version__)
client = commands.Bot(command_prefix='!',)
client.add_cog(Utilities(client))
client.run("")
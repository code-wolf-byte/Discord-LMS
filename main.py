import discord
from discord.ext import commands
from stuff.move import Utilities
print(discord.__version__)

client = commands.Bot(command_prefix='!',)

client.add_cog(Enrollment(client))


client.run("ODM2MzcwODYxNTQ4MTA5ODk0.YIdBEA.3jW1_FAMPFePnMvcj9eVaFU2d8U")
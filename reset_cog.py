import db_handler as dbh
from discord.ext import commands


class Reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.category(name='reset')
    @commands.guild_only()
    @commands.has_permissions
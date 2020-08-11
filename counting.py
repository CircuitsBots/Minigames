import db_handler as dbh, discord
from discord.ext import commands
from discord.ext.commands import Cog
from asyncio import Lock
from typing import Union


async def handle_message(message):
    try:
        num = int(message.content)
    except ValueError:
        return None
    
    if message.guild.id not in dbh.database.locks:
        dbh.database.locks[message.guild.id] = Lock()
    async with dbh.database.locks[message.guild.id]:
        last_user = dbh.database.db['guilds'][message.guild.id]['counting']['last-counter']
        current_num = dbh.database.db['guilds'][message.guild.id]['counting']['current-num']
        if num != current_num + 1:
            await message.add_reaction('❌')
            return False
        if last_user == message.author.id:
            await message.add_reaction('❌')
            return False
        dbh.database.db['guilds'][message.guild.id]['counting']['current-num'] += 1
        dbh.database.db['guilds'][message.guild.id]['counting']['last-counter'] = message.author.id
        await message.add_reaction('✅')
        return True


class Counting(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='counting'
    )
    @commands.guild_only()
    @commands.has_permissions(manage_channels=True)
    async def set_counting_channel(self, ctx, channel: Union[discord.TextChannel, str]):
        if channel is None:
            await ctx.send("I could not find that channel")
            return
        if ctx.guild.id not in dbh.database.locks:
            dbh.database.locks[ctx.guild.id] = Lock()
        if type(channel) is str and channel.lower() == 'none':
            async with dbh.database.locks[ctx.guild.id]:
                dbh.database.db['guilds'][ctx.guild.id]['counting']['channel'] = None
            await ctx.send("Unset counting channel")
            return
        async with dbh.database.locks[ctx.guild.id]:
            dbh.database.db['guilds'][ctx.guild.id]['counting']['channel'] = channel.id
        await ctx.send(f"Set counting channel to {channel.mention}")

    @commands.command(
        name='current', aliases=['num', 'number']
    )
    @commands.guild_only()
    async def get_current_number(self, ctx):
        current = dbh.database.db['guilds'][ctx.guild.id]['counting']['current-num']
        await ctx.send(f"The current number is **{current}**")
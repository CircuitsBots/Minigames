from discord.ext.commands import Bot
from secrets import BETA_TOKEN, TOKEN, INVITE
from asyncio import sleep
import db_handler as dbh
import sys
# Bot Functions:
import counting
import rps
import hangman

if len(sys.argv) > 1 and sys.argv[1] == 'beta':
    bot = Bot('beta ')
    token = BETA_TOKEN
else:
    bot = Bot('mg ')
    token = TOKEN
running = True


async def loop_save():
    while dbh.database is None:
        await sleep(1)
    while running:
        await sleep(5)
        dbh.database.save_database()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} in {len(bot.guilds)} guilds!")
    if dbh.database is None:
        dbh.set_database(bot)
        await bot.loop.create_task(loop_save())


@bot.event
async def on_guild_join(guild):
    while dbh.database is None:
        await sleep(1)
    dbh.database.add_guild(guild.id)


@bot.event
async def on_message(message):
    if message.guild is not None:
        if message.channel.id == dbh.database.db['guilds'][message.guild.id]['counting']['channel']:
            await counting.handle_message(message)
    await bot.process_commands(message)


if __name__ == '__main__':
    try:
        bot.add_cog(counting.Counting(bot))
        bot.add_cog(rps.RockPaperScissors(bot))
        bot.add_cog(hangman.Hangman(bot))
        bot.run(token)
    finally:
        running = False
        dbh.database.save_database()
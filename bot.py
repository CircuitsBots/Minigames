from discord.ext.commands import Bot
from secrets import TOKEN, INVITE
from asyncio import sleep
import db_handler as dbh
# Bot Functions:
import counting

bot = Bot('mg ')
database = None
running = True

async def loop_save():
    while database is None:
        await sleep(1)
    while running:
        await sleep(60)
        dbh.database.db.save_database()



@bot.event
async def on_ready():
    global database
    print(f"Logged in as {bot.user.name} in {len(bot.guilds)} guilds!")
    dbh.set_database(bot)
    bot.loop.create_task(loop_save())


@bot.event
async def on_guild_join(guild):
    while dbh.database is None:
        await sleep(1)
    dbh.database.add_guild(guild.id)


@bot.event
async def on_message(message):
    if message.channel.id == dbh.database.db['guilds'][message.guild.id]['counting']['channel']:
        await counting.handle_message(message)
    await bot.process_commands(message)


if __name__ == '__main__':
    try:
        bot.add_cog(counting.Counting(bot))
        bot.run(TOKEN)
    finally:
        running = False
        dbh.database.save_database()
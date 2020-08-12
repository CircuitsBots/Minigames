from discord.ext import commands
import discord
import db_handler as dbh


async def play_game(p1, p2, bot, ctx):
    winner = None
    plist = [p1, p2]
    lives = [[3], [3]]

    R = '1'
    P = '2'
    S = '3'

    def determine_winner(players):
        c1, c2 = players
        if c1 == c2:
            return None
        if c1 == R:
            if c2 == P:
                return 1
            return 0
        if c1 == P:
            if c2 == S:
                return 1
            return 0
        if c1 == S:
            if c2 == R:
                return 1
            return 0

    class Check:
        def __init__(self, user):
            def check(msg):
                if msg.author.id != user.id:
                    return False
                if msg.content not in [R, P, S]:
                    return False
                return True
            self.check = check

    while True:
        choice_list = []
        for x, p in enumerate(plist):
            await p.send("Please choose an option: (1) Rock, (2) Paper, (3) Scissors.")
            check = Check(p)
            msg = await bot.wait_for('message', check=check.check)
            choice_list.append(msg)
        this_game_winner = determine_winner(choice_list)
        return this_game_winner


class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rps')
    @commands.guild_only()
    async def start_rps_game(self, ctx, target: discord.User):
        if target is None or target.id not in [m.id for m in ctx.guild.members]:
            await ctx.send("I can't find that user")
            return
        if target.bot:
            await ctx.send("You can't challenge a bot")
            return
        #if target.id == ctx.message.author.id:
        #    await ctx.send("You can't play yourself")
        #    return
        await ctx.send(f"{target.mention}, {ctx.message.author.mention} is challenging you to a game of rock-paper-scissors!\
            \nType \"accept\" to accept, or \"decline\" to decline.")
        def check(message):
            if message.author.id != target.id:
                return False
            if message.content.lower() not in ['accept', 'yes', 'deny', 'no', 'decline']:
                return False
            return True
        msg = await self.bot.wait_for('message', check=check)
        if msg.content.lower() in ['deny', 'no', 'decline']:
            await ctx.send("Cancelled")
            return
        await ctx.send("Game started!")
        winner = await play_game(ctx.message.author, target, self.bot)
        if winner == 0:
            await ctx.send(f"{ctx.message.author.mention} Wins!")
            return
        await ctx.send(f"{target.mention} Wins!")
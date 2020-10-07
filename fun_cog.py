import random
import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='8ball', brief='Answers a question randomly',
        description='Answers a question randomly'
    )
    async def eight_ball(self, ctx, *, question):
        respond_no = [
            'No.', 'Nope.', 'Highly Doubtful.', 'Not a chance.',
            'Not possible.', 'Don\'t count on it.'
        ]
        respond_yes = [
            'Yes.', 'Yup', 'Extremely Likely', 'It is possible',
            'Very possibly.'
        ]
        combined = [respond_no, respond_yes]
        group = random.choice([0, 1])
        answer = random.choice(combined[group])

        embed = discord.Embed(
            description=f"**Question:** {question}"
            f"\n\n**Answer:** {answer}"
        )
        embed.set_author(
            name=str(ctx.message.author),
            url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=embed)

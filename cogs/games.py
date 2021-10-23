import discord
from discord.ext import commands
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.score = [{'name': '', 'score': 0, 'id': '', 'color': 0x000000, 'emoji': '', 'emoji_id': ''}]

    @commands.command(name='8ball', aliases=['eightball', 'eight_ball', '8_ball'])
    async def eight_ball(self, ctx, *, question):
        if question == "":
            await ctx.send('Please ask a question.')
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now.',
            'Cannot predict now.',
            'Concentrate and ask again.',
            'Don\'t count on it.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'Very doubtful.'
        ]
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command(name='roll', aliases=['dice', 'rolldice', 'roll_dice'])
    async def roll(self, ctx, *, roll):
        if roll.isdigit():
            await ctx.send(f'{ctx.author.mention} rolled {random.randint(1, int(roll))}')
        else:
            await ctx.send(f'{ctx.author.mention} rolled {random.randint(1, 6)}')
    
    @commands.command(name='flip', aliases=['coin', 'flipcoin', 'flip_coin'])
    async def flip(self, ctx):
        await ctx.send(f'{ctx.author.mention} flipped a coin and got {random.choice(["heads", "tails"])}')

    @commands.command(name='rps', aliases=['rockpaperscissors', 'rock_paper_scissors', 'rock_paper_scissors_game'])
    async def rps(self, ctx, *, choice):
        if self.score.index(lambda x: x['id'] == ctx.author.id) == -1:
            self.score.append({'name': ctx.author.name, 'score': 0, 'id': ctx.author.id, 'color': ctx.author.color.value, 'emoji': ctx.author.display_name, 'emoji_id': ctx.author.emojis[0].id})

        if choice.lower() == "rock":
            choice = "rock"
        elif choice.lower() == "paper":
            choice = "paper"
        elif choice.lower() == "scissors":
            choice = "scissors"
        else:
            await ctx.send(f'{ctx.author.mention} please enter a valid choice.')
            return
        choices = ["rock", "paper", "scissors"]
        await ctx.send(f'{ctx.author.mention} chose {choice}')
        await ctx.send(f'{ctx.author.mention} vs {random.choice(choices)}')
        if choice == random.choice(choices):
            await ctx.send(f'{ctx.author.mention} tied with {random.choice(choices)}')
        elif choice == "rock" and random.choice(choices) == "scissors":
            self.score[self.score.index(lambda x: x['id'] == ctx.author.id)]['score'] += 1
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        elif choice == "paper" and random.choice(choices) == "rock":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        elif choice == "scissors" and random.choice(choices) == "paper":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        else:
            await ctx.send(f'{ctx.author.mention} lost with {choice}')
        

    
    @commands.command(name='rpsls', aliases=['rockpaperscissorslizard', 'rock_paper_scissors_lizard', 'rock_paper_scissors_lizard_spock', 'rock_paper_scissors_lizard_spock_game'])
    async def rpsls(self, ctx, *, choice):
        if choice.lower() == "rock":
            choice = "rock"
        elif choice.lower() == "paper":
            choice = "paper"
        elif choice.lower() == "scissors":
            choice = "scissors"
        elif choice.lower() == "lizard":
            choice = "lizard"
        elif choice.lower() == "spock":
            choice = "spock"
        else:
            await ctx.send(f'{ctx.author.mention} please enter a valid choice.')
            return
        choices = ["rock", "paper", "scissors", "lizard", "spock"]
        await ctx.send(f'{ctx.author.mention} chose {choice}')
        await ctx.send(f'{ctx.author.mention} vs {random.choice(choices)}')
        if choice == random.choice(choices):
            await ctx.send(f'{ctx.author.mention} tied with {random.choice(choices)}')
        elif choice == "rock" and random.choice(choices) == "scissors":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        elif choice == "paper" and random.choice(choices) == "rock":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        elif choice == "scissors" and random.choice(choices) == "paper":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        elif choice == "lizard" and random.choice(choices) == "spock":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        elif choice == "spock" and random.choice(choices) == "lizard":
            await ctx.send(f'{ctx.author.mention} won with {choice}')
        else:
            await ctx.send(f'{ctx.author.mention} lost with {choice}')

def setup(bot):
    bot.add_cog(Games(bot))
from redbot.core import commands
import random
import asyncio

BaseCog = getattr(commands, "Cog", object)

class Simon(BaseCog):
    """Play Simon, and guess the write number sequence!
    
    WARNING:
    This cog sends a lot of messages, edits emojis and edits messages.  It may use up rate limits heavily, so only one game can be played at a time."""

    def __init__(self, bot):
        self.bot = bot
        self.playing = False

    @commands.group()
    async def simon(self, ctx):
        """Group command for playing Simon"""
        pass

    @simon.command()
    async def start(self, ctx):
        if self.playing == True:
            await ctx.send("A game is already in progress.  Please wait for that person to finish!")
            return
        else:
            self.playing = True
        await ctx.send("Starting game...\n**RULES:**\n```1. When you are ready for the sequence, click the green checkmark.\n2. Watch the sequence carefully, then repeat it back into chat.  For example, if the 1 then the 2 changed, I would type 12.\n3. You are given 10 seconds to repeat the sequence.\n4. When waiting for confirmation for next sequence, click the green check within 5 minutes of the bot being ready.\n5. Answer as soon as you can once the bot adds the stop watch emoji.```")
        board = [
            [1, 2],
            [3, 4]
        ]
        level = [1, 4]
        message = await ctx.send("```" + self.print_board(board) + "```")
        await message.add_reaction("\u2705")
        await message.add_reaction("\u274C")
        await ctx.send("Click the Green Check Reaction when you are ready for the sequence.")

        def check(reaction, user):
            return (user == ctx.author) and str(reaction.emoji) in ["\u2705", "\u274C"]

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                await message.delete()
                await ctx.send("Game has ended due to no response for starting the next sequence.")
                self.playing = False
                return
            else:
                if str(reaction.emoji) == "\u274C":
                    await message.delete()
                    self.playing = False
                    return
                await message.remove_reaction('\u2705', self.bot.user)
                await message.remove_reaction('\u2705', ctx.author)
                await message.add_reaction('\u26A0')
                randoms = []
                for x in range(level[1]):
                    randoms.append(random.randint(1, 4))
                for x in randoms:
                    if x == 1:
                        old = board[0][0]
                        board[0][0] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[0][0] = old
                        await message.edit(content="```" + self.print_board(board) + "```")
                    elif x == 2:
                        old = board[0][1]
                        board[0][1] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[0][1] = old
                        await message.edit(content="```" + self.print_board(board) + "```")
                    elif x == 3:
                        old = board[1][0]
                        board[1][0] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[1][0] = old
                        await message.edit(content="```" + self.print_board(board) + "```")
                    elif x == 4:
                        old = board[1][1]
                        board[1][1] = "-"
                        await message.edit(content="```" + self.print_board(board) + "```")
                        await asyncio.sleep(level[0])
                        board[1][1] = old
                        await message.edit(content="```" + self.print_board(board) + "```")
                await message.remove_reaction('\u26A0', self.bot.user)
                answer = "".join(list(map(str, randoms)))
                await message.add_reaction("\u23F1")

                def check_t(m):
                    return m.author == ctx.author and m.content.isdigit()
                try:
                    user_answer = await self.bot.wait_for('message', check=check_t, timeout=10.0)
                except asyncio.TimeoutError:
                    await ctx.send(f"Sorry {ctx.author.mention}!  You took too long to answer.")
                    await message.remove_reaction("\u23F1", self.bot.user)
                    self.playing = False
                    return
                else:
                    await user_answer.delete()
                    await message.remove_reaction("\u23F1", self.bot.user)
                    if str(user_answer.content) == str(answer):
                        await message.add_reaction('\U0001F44D')
                    else:
                        await message.add_reaction('\U0001F6AB')
                        await ctx.send(f"Sorry, but that was the incorrect pattern.  The pattern was {answer}")
                        self.playing = False
                        return
                    another_message = await ctx.send("Sequence was correct.")
                    await asyncio.sleep(3)
                    await message.remove_reaction("\U0001F44D", self.bot.user)
                    await message.add_reaction("\u2705")
                    await message.add_reaction("\u274C")
                    await another_message.delete()
                level[0] *= 0.90
                level[1] += 1

    def print_board(self, board):
        col_width = max(len(str(word)) for row in board for word in row) + 2  # padding
        whole_thing = ""
        for row in board:
            whole_thing += "".join(str(word).ljust(col_width) for word in row) + '\n'
        return whole_thing
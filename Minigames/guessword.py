from Other.variables import getRandomWord
from string import ascii_lowercase
from Other.private import Private
from Other.variables import Variables
from Commands.minigame import MiniGame
import re

class GuessWord(MiniGame):
    def __init__(self, game_manager, msg, playerID):
        super().__init__(game_manager, msg)
        self.playerID = playerID
        self.guessed_word = ""
        self.definition = None
        while self.definition is None:
            self.word = getRandomWord()
            if self.word.lower() in Variables.eng_dict.keys():
                defi = Variables.eng_dict[self.word.lower()]
                if 200 < len(defi) < 1000:
                    self.definition = re.sub(self.word, "*" * len(self.word), defi.lower())


    async def start_game(self):
        await self.msg.edit(content=self.get_board())
        self.msg2 = await self.msg.channel.send("** **")
        self.game_manager.open_games[self.msg2.id] = self
        for i in range(len(ascii_lowercase)):
            if i < 13:
                await self.msg.add_reaction(Variables.DICT_ALFABET[ascii_lowercase[i]])
            if i >= 13:
                await self.msg2.add_reaction(Variables.DICT_ALFABET[ascii_lowercase[i]])
        await self.msg2.add_reaction(Variables.BACK_EMOJI)
        await self.msg2.add_reaction(Variables.STOP_EMOJI)

    async def update_game(self, reaction, user):
        if user.id in Private.BOT_ID: return

        if not user.id == self.playerID:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        if reaction.emoji == Variables.BACK_EMOJI:
            self.guessed_word = self.guessed_word[:-1]
            await reaction.message.remove_reaction(reaction.emoji, user)
            await self.msg.edit(content=self.get_board())
            return

        if reaction.emoji == Variables.STOP_EMOJI:
            await self.msg2.delete()
            await self.msg.edit(content="Game closed.\nThe word was \"" + "".join(self.word) + "\"")
            await self.end_game()
            return

        for letter, emoji in Variables.DICT_ALFABET.items():
            if emoji == reaction.emoji:
                if len(self.guessed_word) < 25:
                    self.guessed_word += letter
                break

        await reaction.message.remove_reaction(reaction.emoji, user)
        await self.msg.edit(content=self.get_board())

        if self.guessed_word == self.word:
            await reaction.message.channel.send("Congratulations <@" +str(self.playerID) + ">, you found the word!")
            await self.msg2.delete()
            await self.end_game()

    def get_board(self):
        text = "```\nDefinition:\n"
        text += self.definition
        text += "\n\nYour guess: "
        for i in range(len(self.guessed_word)):
            text += str(self.guessed_word[i])
        text += "\n```"
        return text
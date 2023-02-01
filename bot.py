import os
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import errors
from platform import python_version
from models import BaseConfig
from config import Config


class Bot(commands.Bot):
    loaded: bool = False
    config: BaseConfig

    def __init__(self) -> None:
        self.config = Config
        super().__init__(commands.when_mentioned_or(self.config.prefix), intents= self.config.intents)

    async def setup_hook(self):
        self.remove_command('help')
        await self.load_extension('jishaku')

        for filename in os.listdir('./cogs'):
            if not filename.startswith('!'):
                try:
                    await self.load_extension(f'cogs.{filename}')
                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)

    async def on_ready(self):
        if self.loaded:
            return

        self.loaded = True

        print(f'Python v{python_version()}')
        print(f'discord.py v{discord.__version__}')
        print(f'Bot account - {self.user}')
        print(f'Guilds: {len(self.guilds)}')

    async def on_command_error(self, context: commands.Context, exception: errors.CommandError) -> None:
        if isinstance(exception, errors.NoPrivateMessage):
            return
        return await super().on_command_error(context, exception)

    def run(self):
        super().run(self.config.token)


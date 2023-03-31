import discord
from discord.ext import commands
from discord import app_commands
from login_modal import LoginCog
from webhook_manager import WebhookManager
from data import db_session


class ImageSender(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def setup_hook(self) -> None:
        await self.add_cog(WebhookManager(self))
        await self.add_cog(LoginCog(self))
        await self.tree.sync()


if __name__ == "__main__":
    db_session.global_init()
    bot = ImageSender()
    bot.run("MTA4OTQzNjY3MjI0NjE1MzI0Ng.GWFVOe.07ReZ0_kli3iBhiIRIPqJYBrgZaMDv-v7XVm48")

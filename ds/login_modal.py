import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button
from data.db_session import create_session
from data.users import User


class LoginModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Авторизация")

        self.add_item(discord.ui.TextInput(label="Логин"))
        self.add_item(discord.ui.TextInput(label="Пароль"))

    async def on_submit(self, interaction: discord.Interaction):
        db_sess = create_session()
        user = db_sess.query(User).filter(User.name == self.children[0].value).first()

        async def accept_callback(interaction: discord.Interaction):
            try:
                db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first().ds_id = None
            except:
                pass
            user.ds_id = str(interaction.user.id)
            await interaction.response.edit_message(content="Успешно")

        async def refuse_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(content="Отменено")

        if not user:
            await interaction.response.send_message("Похоже, что пользователя с таким логином не существует")
        elif db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first() and db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first() == user:
            return await interaction.response.send_message("Вы уже в аккаунте", ephemeral=True)
        elif db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first() and\
                db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first() != user and \
                user.check_password(self.children[1].value):
            button_accept = Button(label="Да", style=discord.ButtonStyle.green)
            button_refuse = Button(label="Нет", style=discord.ButtonStyle.red)
            button_accept.callback = accept_callback
            button_refuse.callback = refuse_callback
            view = discord.ui.View()
            view.add_item(button_accept)
            view.add_item(button_refuse)
            await interaction.response.send_message("Данный аккаунт discord уже привзяан к другому аккаунту. "
                                                    "Вы уверены, что хотите продолжить?", view=view, ephemeral=True)
        elif user.ds_id:
            button_accept = Button(label="Да", style=discord.ButtonStyle.green)
            button_refuse = Button(label="Нет", style=discord.ButtonStyle.red)
            button_accept.callback = accept_callback
            button_refuse.callback = refuse_callback
            view = discord.ui.View()
            view.add_item(button_accept)
            view.add_item(button_refuse)
            await interaction.response.send_message("Данный аккаунт уже привзяан к другому аккаунту discord. "
                                                    "Вы уверены, что хотите продолжить?", view=view, ephemeral=True)
        elif user and user.check_password(self.children[1].value):
            user.ds_id = str(interaction.user.id)
            db_sess.commit()
            await interaction.response.send_message("Успешно ✅", ephemeral=True)
        else:
            await interaction.response.send_message("Не удалось войти в аккаунт", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(error)


class LoginCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="login", description="login to your account")
    async def login(self, interaction: discord.Interaction):
        modal = LoginModal()
        await interaction.response.send_modal(modal)

    @app_commands.command(name="quit", description="this command will log out of your account")
    async def quit(self, interaction: discord.Interaction):
        db_sess = create_session()
        user = db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first()
        if user:
            user.ds_id = None
            db_sess.commit()
            await interaction.response.send_message("успешно, чертила ✅", ephemeral=True)
        else:
            await interaction.response.send_message("Но ты ведь и так не в аккаунте 🤨 💊 🚑", ephemeral=True)

import discord
from discord import app_commands
from discord.ext import commands
from data.users import User
from data import db_session
from data.discord_webhooks import Webhook
import os
from data.discord_webhooks import Webhook


class WebhookManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(manage_webhooks=True)
    @app_commands.command(name="create_webhook")
    async def create_webhook(self, interaction: discord.Interaction, name: str, channel: discord.TextChannel):
        db_sess = db_session.create_session()
        dis_webhook = await channel.create_webhook(name=name)
        cur_webhook = Webhook(ds_id=dis_webhook.id, ds_url=dis_webhook.url, guild_id=str(dis_webhook.guild_id),
                              user_id=db_sess.query(User).filter(User.ds_id == str(interaction.user.id)).first().id)
        db_sess.add(cur_webhook)
        db_sess.commit()
        await interaction.response.send_message("Успешно", ephemeral=True)

    @commands.has_permissions(manage_webhooks=True)
    @app_commands.command(name="get_my_webhooks")
    async def get_webhooks(self, interaction: discord.Interaction):
        db_sess = db_session.create_session()
        webhooks = db_sess.query(Webhook).filter(Webhook.guild_id == str(interaction.guild_id) and
                                                 Webhook.user.ds_id == str(interaction.user.id))
        embed = discord.Embed(color=0x7b917b, title=f"Вебхуки пользователя {interaction.user.id}")
        for webhook in webhooks:
            embed.add_field(name=(await self.bot.fetch_webhook(webhook.ds_id)).name, value=f"ID: {webhook.ds_id}\nURL:"
                                                                                      f" {webhook.ds_url}", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.has_permissions(manage_webhooks=True)
    @app_commands.command(name="delete_webhook", description="deletes your created webhooks")
    async def delete_webhook(self, interaction: discord.Interaction, webhook_id: str, reason: str):
        db_sess = db_session.create_session()
        webhook_to_delete = db_sess.query(Webhook).filter(Webhook.ds_id == webhook_id).first()
        if not webhook_to_delete:
            await interaction.response.send_message("Данный вебхук не существует либо не принадлежит вам", ephemeral=True)
        try:
            await (await self.bot.fetch_webhook(int(webhook_id))).delete(reason=reason)
            db_sess.delete(webhook_to_delete)
            db_sess.commit()
            await interaction.response.send_message("Успешно", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Укажите правильный ID", ephemeral=True)
        except Exception as exc:
            await interaction.response.send_message(exc)
            db_sess.delete(webhook_to_delete)
            db_sess.commit()

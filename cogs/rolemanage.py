import discord
import sqlite3
from discord.ext import commands
from config import *
from discord.ui import Button, View
import time
import math
import os

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)

data_base = sqlite3.connect('bot_test.db', timeout=10)

cursor = data_base.cursor()

global payment1
global channelid
global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма
global vtime


class Shop(commands.Cog):

    def __init__(self):
        self.bot = bot

    # КНОПОЧКИ!!
    # @commands.command(aliases=['магазин', 'магаз'])
    # async def shop(self, ctx):
    #     emb = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
    #     emb.add_field(name='Магазин сервера.', value="Ниже представлены категории покупки.", inline=False)
    #     roles_button = Button(label='Роли', style=discord.ButtonStyle.primary, emoji='<:booster:1029482318118797412>')
    #     room_button = Button(label='Комната', style=discord.ButtonStyle.primary, emoji='🔊')
    #
    #     async def role_callback(interaction):
    #         await ctx.send('понял-понял')
    #         await interaction.response.is_done()
    #     async def room_callback(interaction):
    #         await interaction.response.send_message("WASSUP")
    #
    #     roles_button.callback = role_callback
    #     room_button.callback = room_callback
    #     view = View()
    #     view.add_item(roles_button)
    #     view.add_item(room_button)
    #     await ctx.send(embed=emb, view=view)
    #



        # @commands.command()  # создание роли
        # async def newrole(self, ctx, *, content):
        #     connection = sqlite3.connect('bot_test.db')
        #     a = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #     oplata = 10000
        #     op = a
        #     connection.commit()
        #
        #     if op < 10000:
        #
        #         emb = discord.Embed(title="[BuyRole]", colour=discord.Colour(0x3e038c))
        #         emb.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
        #         await ctx.send(embed=emb)
        #
        #     elif op >= 10000:
        #
        #         cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
        #         guild = ctx.guild
        #         role = await guild.create_role(name=content)
        #         roleid = role.id
        #         await ctx.author.add_roles(role)
        #         description = f'''
        #             **Name:** <@{roleid}>
        #             **Created by:** {ctx.author.mention}
        #             '''
        #         await ctx.send("Роль была создана и выдана. Для редакции обратитесь к @St1zy3 ")
        #         print(roleid)
        #
        # @commands.command()
        # async def shop(self, ctx):
        #     emb = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        #     emb.add_field(name='Магазин ролей.', value="Ниже представлены роли для покупки.", inline=False)
        #     emb.add_field(name='1. [1]', value="35.000 SH", inline=False)
        #     emb.add_field(name='2. [2]', value="50.000 SH", inline=False)
        #     emb.add_field(name='Покупка.', value="Для покупки необходимо написать '/buyrole Номер роли'", inline=False)
        #     await ctx.send(embed=emb)
        #
        # @commands.command()  # Не работает выдача ролиы
        # async def buyrole(self, ctx, count: int = None):
        #     member = ctx.message.author
        #     role = discord.Role.name == '[1]'
        #     oplata = 35000
        #     role: discord.Role
        #     member: discord.Member
        #     connection = sqlite3.connect('bot_test.db')
        #     cursor = connection.cursor()
        #     balance = cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        #     connection.commit()
        #     if count == 1:
        #         if balance >= 35000:
        #             roles = 1050283874938261544
        #             role = int(roles)
        #             await member.add_roles(roles)
        #             cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(oplata, ctx.author.id))
        #             emb = discord.Embed(title="[SHOP]", colour=discord.Colour(0x3e038c))
        #             emb.add_field(name='Спасибо за покупку!', value="Роль была выдана.", inline=False)
        #             await ctx.send(embed=emb)
        #         else:
        #             emb = discord.Embed(title="[Buy]", colour=discord.Colour(0x3e038c))
        #             emb.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
        #             await ctx.send(embed=emb)
        #


async def setup(bot):
    await bot.add_cog(Shop())


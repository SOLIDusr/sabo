import discord
import sqlite3
from discord.ext import commands
from config import *
from discord.ext.commands import has_permissions, MissingPermissions


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)

data_base = sqlite3.connect('bot_test.db', timeout=10)

cursor = data_base.cursor()

global payment1
global channelid
global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма
global vtime


intents = discord.Intents.all()


class Economics(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['bal', 'баланс', 'бал'])
    async def balance(self, ctx, member:discord.Member=None):

        if member is not None:

            try:

                for row in cursor.execute(f"SELECT nickname, money FROM users where id={member.id}"):

                    embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
                    embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
                    await ctx.send(embed=embed)

            except Exception as E:

                print(f'money command error: {E}')
                embed = discord.Embed(title='Оповещение', color=0xFF0000)
                embed.add_field(name='Оповещение', value='Ошибка при выполнение программы.')
                await ctx.send(embed=embed)

        elif member is None:

            for row in cursor.execute(f"SELECT nickname, money FROM users where id={ctx.author.id}"):

                embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
                embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
                await ctx.send(embed=embed)

    @bot.command(name="set_money", pass_context=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def set_money(self, ctx, member: discord.Member, amount:int = None):

        if amount < 0:

            await ctx.send('Количество не может быть отрицательным!')
            return None

        else:

            for row in cursor.execute(f'SELECT money FROM users where id={member.id}'):

                cursor.execute(f'UPDATE users SET money= {int(amount)+row[0]} where id={member.id}')
            data_base.commit()

            for row in cursor.execute(f'SELECT nickname FROM users where id={member.id}'):

                embed = discord.Embed(title='Пополнение баланса', color=0x42f566)
                embed.set_author(name='Community Bot')
                embed.add_field(name='Оповещение', value=f'Баланс пользователя {row[0]} пополнен на {amount} SH')
                await ctx.send(embed=embed)

    @set_money.error
    async def set_money_error(self, ctx, error):

        if isinstance(error, MissingPermissions):

            text = "Извините {}, У вас нет полномочий на это!".format(ctx.message.author)
            await ctx.send(ctx.message.channel, text)

    @commands.command()
    async def profile(self, ctx):

        profile_nick = \
            cursor.execute("SELECT nickname FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        profile_balance = \
            cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
        embed = discord.Embed(title=f'[Profile]', color=0x42f566)
        embed.add_field(name='Nickname:', value=f'{profile_nick}', inline=False)
        embed.add_field(name='Balance:', value=f'{profile_balance} SH', inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economics())

import discord
from discord.ext import commands
from configs.config import *
from discord.ext.commands import has_permissions, MissingPermissions
import psycopg2 as sql
from configs.database_config import *
from logs import logger


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)


global payment1
global channelid
global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма
global vtime


data_base = sql.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port,

)
data_base.autocommit = False

try:

    cursor = data_base.cursor()

except Exception as _ex:

    logger.info(f'Error happend while connecting to Database! {_ex}')


class Economics(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['bal', 'баланс', 'бал'])
    async def balance(self, ctx, member: discord.Member = None):

        if member is not None:

            try:

                cursor.execute(f'SELECT nickname, money FROM users where id={member.id}')
                row = cursor.fetchone()
                embed = discord.Embed(title=f'Аккаунт пользователя {row[0]}', color=0x42f566)
                embed.add_field(name='Баланс:', value=f'{row[1]} SH', inline=False)
                await ctx.send(embed=embed)

            except Exception as error:

                logger.info(f'money command error: {error}')
                embed = discord.Embed(title='Оповещение', color=0xFF0000)
                embed.add_field(name='Оповещение', value='Ошибка при выполнение программы.')
                await ctx.send(embed=embed)

        elif member is None:

            cursor.execute(f'SELECT nickname, money FROM users where id={ctx.author.id}')
            response = cursor.fetchone()

            embed = discord.Embed(title=f'Аккаунт пользователя {response[0]}', color=0x42f566)
            embed.add_field(name='Баланс:', value=f'{response[1]} SH', inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="set_money", pass_context=True)
    @has_permissions(manage_roles=True, ban_members=True)
    async def set_money(self, ctx, member: discord.Member, amount: int = None):

        if amount < 0:

            await ctx.send('Количество не может быть отрицательным!')

        else:

            cursor.execute(f'SELECT money FROM users where id={member.id}')
            row = cursor.fetchone()
            cursor.execute(f'UPDATE users SET money= {int(amount) + row[0]} where id={member.id}')
            data_base.commit()
            cursor.execute(f'SELECT nickname FROM users where id={member.id}')
            row = cursor.fetchone()
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

        cursor.execute('SELECT nickname, money FROM users WHERE id = {}'.format(ctx.author.id))
        nickname, balance = cursor.fetchone()[0], cursor.fetchone()[1]

        embed = discord.Embed(title=f'[Profile]', color=0x42f566)
        embed.add_field(name='Nickname:', value=f'{nickname}', inline=False)
        embed.add_field(name='Balance:', value=f'{balance} SH', inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Economics())

import discord
from discord.ext import commands
from config import *
import random


import psycopg2 as sql
from configs.database_config import *
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

    print(f'Error happend while connecting to Database! {Exception}')

# the goad to get rid of globals
global payment1
global channelid
# global Oplata  # Переменная в которой будет хранится оплаченная за команту сумма (Not used(strange))
global vtime


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


class Gambling(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['Казино', 'казино', 'casino', 'Casino'])
    async def __casino(self, ctx, amount: int = None):
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))
        balance = cursor.fetchone()[0]
        connection = data_base
        number = random.randint(1, 100)
        jackpot = random.randint(5000, 20000)

        # Условия и т.д

        if amount is None:

            emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='[Ошибка]', value="Вы забыли указать ставку!", inline=False)
            await ctx.send(embed=emb)

        elif amount > balance or amount < 0:

            emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
            await ctx.send(embed=emb)

        elif balance <= 0:

            emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
            emb.add_field(name='[Ошибка]', value="Недостаточно средств.", inline=False)
            await ctx.send(embed=emb)

        else:

            if number < 50:

                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                connection.commit()
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                await ctx.send(embed=embed)

            elif number == 93:

                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(jackpot, ctx.author.id))
                connection.commit()
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='О боже мой!!! Вы выйграли JACKPOT, мы добавили вам на баланс:',
                                value=f'{jackpot} SH', inline=False)
                await ctx.send(embed=embed)

            elif number == 27:

                emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.",
                              inline=False)
                await ctx.send(embed=emb)

            elif number == 13:

                emb = discord.Embed(title="[CASINO]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='[Итог]', value="Вам попалось SAFE-ЯЧЕЙКА, вы не потеряли свой баланс.",
                              inline=False)
                await ctx.send(embed=emb)

            else:

                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount, ctx.author.id))
                connection.commit()
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount} SH', inline=False)
                await ctx.send(embed=embed)

    @commands.command()
    async def roulette(self, ctx, amount: int = None, count: int = None):

        connection = data_base
        number = random.randint(0, 36)
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))
        balance = cursor.fetchone()[0]

        if amount is None:

            await ctx.send("Вы забыли указать ставку!")

        elif count is None:

            await ctx.send("Нужно выбрать на что ставить.")

        elif count > 36 or count < 0:

            await ctx.send("Нужно выбрать число от 0 до 36")

        elif amount > balance or amount < 0:

            await ctx.send("Недостаточно :leaves:, иди на работу.")

        elif balance <= 0:

            await ctx.send("Недостаточно :leaves:, иди на работу.")

        else:

            if count != number:

                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(amount, ctx.author.id))
                connection.commit()
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                await ctx.send(embed=embed)

            elif count == number:

                cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(amount * 36, ctx.author.id))
                connection.commit()
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount * 36} SH', inline=False)
                embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                await ctx.send(embed=embed)

    @commands.command(aliases=["кейс", "кейсы", "контейнер"])
    async def case(self, ctx, move: str = None):

        moves = ["открыть", "купить", "buy", "open"]
        cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id))
        cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))
        keys = cursor.fetchone()
        balance = cursor.fetchone()

        connection = data_base

        if move is None:

            embed = discord.Embed(title=f'[CASE]', color=0x42f566)
            embed.add_field(name='У вас в наличии:', value=f'{keys} кейсов.', inline=False)
            await ctx.send(embed=embed)

        elif move is not None and move not in moves:

            emb = discord.Embed(title='[ERROR] сase', description=f'{ctx.author.mention}, Укажите правильное действие!',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Действия:', value=f'{moves}', inline=False)
            emb.add_field(name='Пример :', value='/case открыть')
            await ctx.send(embed=emb)

        elif move in ['окрыть', 'open']:

            cursor.execute("SELECT keys FROM users WHERE id = {}".format(ctx.author.id))
            keys = cursor.fetchone()
            connection = data_base
            val = 1

            if keys >= 1:

                cursor.execute("UPDATE users SET keys = keys - {} WHERE id = {}".format(val, ctx.author.id))
                connection.commit()
                rand = random.randint(0, 100)

                if 0 <= rand <= 70:

                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="К сожалению вам ничего не выпало.",
                                  inline=False)
                    await ctx.send(embed=emb)

                elif 71 <= rand <= 80:

                    pp1 = 400000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp1, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 400.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 81 <= rand <= 90:

                    pp2 = 800000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp2, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 800.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 91 <= rand <= 95:

                    pp3 = 1600000
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 1.600.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 96 <= rand <= 100:

                    pp3 = 5555555
                    cursor.execute("UPDATE users SET money = money + {} WHERE id = {}".format(pp3, ctx.author.id))
                    connection.commit()
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 5.555.555SH", inline=False)
                    await ctx.send(embed=emb)

            elif keys < 1:

                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)
                await ctx.send(embed=emb)

        elif move in ['buy', 'купить']:

            cent = 100000  # Цена кейса
            val = 1  # Кол-во покупаемых кейсов.
            if balance < cent:

                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)
                await ctx.send(embed=emb)

            elif balance >= cent:

                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(cent, ctx.author.id))
                cursor.execute("UPDATE users SET keys = keys + {} WHERE id = {}".format(val, ctx.author.id))
                connection.commit()
                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Успешно.', value="Кейс был куплен, для открытия введите '/case открыть или /case open'.", inline=False)
                await ctx.send(embed=emb)


async def setup(bot):
    await bot.add_cog(Gambling())

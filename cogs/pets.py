import discord
from discord.ui import Select, View
from discord.ext import commands
from configs.config import *
import random
from logs import logger
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

    logger.info(f'Error happend while connecting to Database! {_ex}')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)


class Pets(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command()
    async def casepets(self, ctx, move: str = None):
        moves = ["открыть", "купить", "buy", "open"]
        cursor.execute(f"SELECT pet_has FROM users WHERE id = {ctx.author.id}")
        user_pets = list(cursor.fetchone()[0])
        cursor.execute(f"SELECT casepets FROM users WHERE id = {ctx.author.id}")
        casepets = cursor.fetchone()[0]
        cursor.execute(f'SELECT money FROM users WHERE id = {ctx.author.id}')
        balance = cursor.fetchone()[0]
        cursor.execute(f'SELECT pet_active FROM users WHERE id = {ctx.author.id}')
        activepet = cursor.fetchone()[0]


        if move is None:

            embed = discord.Embed(title=f'[CasePets]', color=0x42f566)
            embed.add_field(name='У вас в наличии:', value=f'{casepets} кейсов с питомцами.', inline=False)
            await ctx.send(embed=embed)

        elif move is not None and move not in moves:

            emb = discord.Embed(title='[ERROR] CasePets',
                                description=f'{ctx.author.mention}, Укажите правильное действие!',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Действия:', value=f'{moves}', inline=False)
            emb.add_field(name='Пример :', value='/casepets открыть')
            await ctx.send(embed=emb)

        elif move in ['окрыть', 'open']:

            cursor.execute(f"SELECT casepets FROM users WHERE id = {ctx.author.id}")
            casepets = cursor.fetchone()[0]

            val = 1

            if casepets >= 1:
                cursor.execute(f"UPDATE users SET casepets = casepets - {val} WHERE id = {ctx.author.id}")
                data_base.commit()
                rand = random.randint(0, 50)

                if rand == 31:

                    if 'wolf' in user_pets:

                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Волк', но он у вас уже есть. Кейс "
                                                           "не был потрачен",
                                      inline=False)
                        await ctx.send(embed=emb)
                        cursor.execute(f"UPDATE users SET casepets = casepets + {val} WHERE id = {ctx.author.id}")
                        data_base.commit()

                    else:

                        cursor.execute(
                            "UPDATE users SET pet_has = pet_has + {} WHERE id = {}".format('wolf', ctx.author.id))
                        data_base.commit()
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Волк'.", inline=False)
                        emb.add_field(name='Питомец "Волк".',
                                      value="Данный питомец прибавляет процент от суммы выйгрыша в казино на 7% .",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы сыграли в казино на 50.000 SH, победили, вам прибавляется на"
                                            " баланс 50.000 SH которые вы выйграли и сверху 3.500 SH за счет того "
                                            "что у вас данный питомец .",
                                      inline=False)
                        emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
                        emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
                        await ctx.send(embed=emb)

                elif rand == 14:

                    if 'fox' in user_pets == 1:

                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Лиса', но он у вас уже есть."
                                                           "Кейс не потрачен!",
                                      inline=False)
                        await ctx.send(embed=emb)
                        cursor.execute(f"UPDATE users SET casepets = casepets + {val} WHERE id = {ctx.author.id}")
                        data_base.commit()

                    else:

                        cursor.execute(
                            "UPDATE users SET pet_has = users.pet_has + {} WHERE id = {}".format('fox', ctx.author.id))
                        data_base.commit()
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Лиса'.", inline=False)
                        emb.add_field(name='Питомец "Лиса".',
                                      value="Данный питомец прибавляет 7% SH от времени которое вы находились"
                                            " в голосовом канале.",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы просидели в голосовом канале 4 часа, после выхода вас начислятся "
                                            "4.800 SH, за счет того что у вас данный питомец , вам сверху прибавится"
                                            " 336 SH.",
                                      inline=False)
                        emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
                        emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
                        await ctx.send(embed=emb)

                elif rand == 37:

                    if 'dog' in user_pets:

                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Собака', но он у вас уже есть."
                                                           "Кейс не потрачен",
                                      inline=False)
                        cursor.execute(f"UPDATE users SET casepets = casepets + {val} WHERE id = {ctx.author.id}")
                        data_base.commit()
                        await ctx.send(embed=emb)

                    else:

                        cursor.execute(
                            "UPDATE users SET pet_has = pet_has + {} WHERE id = {}".format('dog', ctx.author.id))
                        data_base.commit()
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Собака'.", inline=False)
                        emb.add_field(name='Питомец "Собака".',
                                      value="Данный питомец возвращает вам 5 % от проигрыша в казино.",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы поставили в казино 5000 SH и проиграли , за счет того что у вас данный питомец, вам вернется 250 SH. :exclamation: Если ставка менее 100 SH возврата средств не будет :exclamation: ",
                                      inline=False)
                        emb.add_field(name='Посмотреть ваших питомцев:', value="/mypets", inline=False)
                        emb.add_field(name='Узнать информацию о всех питомцах', value="/help питомцы", inline=False)
                        await ctx.send(embed=emb)

                else:

                    emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='[Итог]', value="К сожалению вам ничего не выпало.",
                                  inline=False)
                    await ctx.send(embed=emb)

            elif casepets <= 0:

                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="У вас нет кейсов.", inline=False)
                await ctx.send(embed=emb)

        elif move in ['buy', 'купить']:

            price = 5000  # Цена кейса
            val = 1  # Кол-во покупаемых кейсов.

            if balance < price:

                emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Ошибка.', value="Недостаточно средств.", inline=False)
                await ctx.send(embed=emb)

            elif balance >= price:

                cursor.execute("UPDATE users SET money = money - {} WHERE id = {}".format(price, ctx.author.id))
                cursor.execute("UPDATE users SET casepets = casepets + {} WHERE id = {}".format(val, ctx.author.id))
                data_base.commit()
                emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Успешно.',
                              value="Кейс с питомцами был куплен, для открытия введите '/casepets открыть или /casepets open'.",
                              inline=False)
                await ctx.send(embed=emb)

    @commands.command(aliases=["мои питомцы", "мои петы"])
    async def mypets(self, ctx):
        effects = ''
        cursor.execute(f"SELECT pet_has FROM users WHERE id = {ctx.author.id}")
        user_pets = cursor.fetchone()[0]
        cursor.execute(f"SELECT casepets FROM users WHERE id = {ctx.author.id}")
        activepet = cursor.fetchone()[0]

        if activepet == 'wolf':

            effects += 'Прибавляет процент от суммы выйгрыша в казино на 7%\n'

        elif activepet == 'fox':

            effects += 'Прибавляет 7% SH от времени которое вы находились в голосовом канале.\n'

        elif activepet == 'dog':

            effects += 'Возвращает вам 5 % от проигрыша в казино.'

        elif activepet is None:

            effects = 'У вас нет активного питомца...'

        if user_pets != '' and activepet is None:

            embi = discord.Embed(title='[MyPets]', colour=discord.Colour(0x3e038c))
            embi.add_field(name='Ваши питомцы', value=f'{user_pets}')
            embi.add_field(name='Активого питомца', value='нет')

        elif activepet is not None:

            embi = discord.Embed(title='[MyPets]', colour=discord.Colour(0x3e038c))
            embi.add_field(name='Ваши питомцы', value=f'{user_pets}')
            embi.add_field(name='Активный питомец', value=f'{activepet}')
            embi.add_field(name='Эффект от питомца', value=effects)

        else:
            embi = discord.Embed(title='[MyPets]', colour=discord.Colour(0x3e038c))
            embi.add_field(name='У вас нет питомцев', value='нет питомцев')

        await ctx.send(embed=embi)

    @commands.command()  # Выбрать питомца
    async def selectpet(self, ctx):
        cursor.execute(f"SELECT pet_has FROM users WHERE id = {ctx.author.id}")
        user_pets = list(cursor.fetchone()[0])
        cursor.execute(f'SELECT pet_active FROM users WHERE id = {ctx.author.id}')
        activepet = cursor.fetchone()[0]

        select = Select(

            options=[
                discord.SelectOption(
                    label="Wolf",
                    emoji="🐺"
                ),

                discord.SelectOption(
                    label="Fox",
                    emoji="🦊"
                ),

                discord.SelectOption(
                    label="Dog",
                    emoji="🐶"
                )
            ])

        async def my_callback(interaction):  # Если namepet active - выбран данный питомец

            if select.values[0] == 'wolf':
                if 'wolf' not in user_pets:
                    await ctx.send('У вас нет данного питомца.')
                else:
                    if 'wolf' not in activepet:
                        await ctx.send('У вас уже установлен данный питомец.')
                    else:
                        await ctx.send('Вы установили питомца!')
                        cursor.execute(f"UPDATE users SET pet_active = 'wolf' WHERE id = {ctx.author.id}")
                        data_base.commit()

            elif select.values[0] == 'fox':
                if 'fox' not in user_pets:
                    await ctx.send('У вас нет данного питомца.')
                else:
                    if 'fox' not in activepet:
                        await ctx.send('У вас уже установлен данный питомец.')
                    else:
                        await ctx.send('Вы установили питомца!')
                        cursor.execute(f"UPDATE users SET pet_active = 'fox' WHERE id = {ctx.author.id}")
                        data_base.commit()

            elif select.values[0] == 'dog':
                if 'dog' not in user_pets:
                    await ctx.send('У вас нет данного питомца.')
                else:
                    if 'dog' not in activepet:
                        await ctx.send('У вас уже установлен данный питомец.')
                    else:
                        await ctx.send('Вы установили питомца!')
                        cursor.execute(f"UPDATE users SET pet_active = 'dog' WHERE id = {ctx.author.id}")
                        data_base.commit()
            await interaction.response.defer()

        select.callback = my_callback
        view = View()
        view.add_item(select)
        await ctx.send("Select Pet", view=view)


async def setup(bot):
    await bot.add_cog(Pets())


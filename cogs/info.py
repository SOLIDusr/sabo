import discord

from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)


class Info(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['хелп', 'помощь'])
    async def help(self, ctx, state: str = None):

        states = ['валюта', "деньги", "вал", "казик", "казино", "казин", "роль", "роли", "войс", "комната", "голос",
                  "кейсы", "кейс", "контейнеры", "команды"]
        # Если ошибка при вводе команды /help [something]
        if state is not None and state not in states:

            emb = discord.Embed(title='[ERROR] help', description=f'{ctx.author.mention}, Укажите правильный раздел',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Разделы:', value='команды, валюта, казино, роли, войс, кейсы', inline=False)
            emb.add_field(name='Пример :', value='/help кейсы')
            await ctx.send(embed=emb)
        # если не назначено
        elif state is None:

            emb = discord.Embed(title="О функциях бота", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Напишет', value='Главный тех менеджер - Дима, который лучше меня знает. :leaves:')
            emb.add_field(name='/help команды', value='Информация по командам сервера. :leaves:')
            await ctx.send(embed=emb)
        # команды
        elif state == "команды":

            emb = discord.Embed(title="О активностях и командах сервера", description='Помощь по командам бота',
                                colour=discord.Colour(0x3e038c))
            emb.add_field(name='/help казино', value="Узнать о том какие игры есть на сервере и как они "
                                                     "работают.:leaves:", inline=False)
            emb.add_field(name='/help валюта', value="Узнать о том что за валюта есть на данном сервере и все о "
                                                     "ней.:leaves:", inline=False)
            emb.add_field(name='/help роли', value="Узнать о покупке кастомной роли.:leaves:", inline=False)
            emb.add_field(name='/help войс', value="Узнать о покупке личного голосового канала.:leaves:", inline=False)
            emb.add_field(name='/help кейсы', value="Узнать о покупке кейсов.:leaves:", inline=False)
            await ctx.send(embed=emb)
        # валюта
        elif state in ['валюта', "деньги", "вал"]:

            emb = discord.Embed(title="Информация о валюте", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Валюта данного сервера - "SH".', value="Чтобы ее получить нужно находиться в "
                                                                       "войсе.:leaves:", inline=False)
            emb.add_field(name='Система начисления.', value="1 минута в войсе = 20 SH.:leaves:", inline=False)
            emb.add_field(name='Для чего нужна данная валюта?:leaves:',
                          value="В данный момент на нее можно только играть в казино, в будущем планируется "
                                "добавления нескольких вариантов тратить SH.:leaves:",
                          inline=False)
            emb.add_field(name='Первый вариант.', value="Создание личного голосового чата , поддержание его за SH ("
                                                        "Если валюты не будет хватать , войс будет удален).:leaves:",
                          inline=False)
            emb.add_field(name='Второй вариант.', value="Покупка различных ролей а так же создание кастомной "
                                                        "роли.:leaves:", inline=False)
            await ctx.send(embed=emb)
        # казино
        elif state in ["казик", "казино", "казин"]:

            emb = discord.Embed(title="CasinoHelp", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Игры Casino:', value="--->", inline=False)
            emb.add_field(name='Первая игра.',
                          value='/casino ставка.''В данной игре при победе вы получаете x2 от ставки, в случае '
                                'проигрыша отнимается сумма вашей ставки. Так же есть шанс словить "JACKPOT", '
                                'а приз там весьма неплохой.:leaves:',
                          inline=False)
            emb.add_field(name='Вторая игра.',
                          value="/roulette ставка число.""В данной игре рандомно выпадает число от 0 до 36, "
                                "вы пытаетесь угадать что выпадет и в случае победы вы получаете x36 от суммы "
                                "ставки.:leaves:",
                          inline=False)
            emb.add_field(name='Откуда брать валюту для игры в Казино?:leaves:', value="/Valhelp", inline=False)
            await ctx.send(embed=emb)
        # Роли
        elif state in ["роль", "роли"]:
            emb = discord.Embed(title="Система покупки ролей", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Кастомные роли.', value="На нашем сервере есть возможность создать свою роль.",
                          inline=False)
            emb.add_field(name='Цена.',
                          value='Начнем с ценника, стоимость данной услуги составляет 10.000 SH, дорого , но сделано '
                                'это чтобы у каждого второго не было своей роли, это предаст обладателям кастомной '
                                'роли некий эксклюзив.',
                          inline=False)
            emb.add_field(name='Создание роли.', value="Создание роли выполняется командой '/newrole Название роли'",
                          inline=False)
            emb.add_field(name='Создал роль. Что дальше?',
                          value="Роль создается 'Дефолтной', так что после покупки вы можете обратиться к @St1zy3 для "
                                "редакции вашей роли (Цвет, значимость)",
                          inline=False)
            emb.add_field(name='Значимость роли',
                          value='Под значимостью мы подразумеваем то, что роль будет находиться выше остальных и тем '
                                'самым будет выделять вас.',
                          inline=False)
            await ctx.send(embed=emb)
        # Войсы
        elif state in ["войс", "комната", "голос"]:

            he1 = discord.Embed(title="Приватные голосовые каналы", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Личная комната.',
                          value="На нашем сервере есть возможность создать свою личную комнату.", inline=False)
            he1.add_field(name='Как создать свою личную комнату?', value='Создание происходит командой '
                                                                         '"/create_voice", стоимость создания '
                                                                         'составляет 2.500 SH.', inline=False)
            he1.add_field(name='Оплата личной комнаты.', value="Личную комнату нужно оплачивать, иначе она будет "
                                                               "удалена.", inline=False)
            he1.add_field(name='Создал комнату. Что дальше?', value="После создания личной комнаты у вас будет 24 "
                                                                    "часа на оплату. Оплата недельная , стоимость 7 "
                                                                    "дней составяет 12.000 SH.", inline=False)
            he1.add_field(name='Как оплатить свою комнату?', value='Оплатить комнату можно командой "/payment".',
                          inline=False)
            he1.add_field(name='Команды управления комнатой.', value='В данный момент есть 2 команды : "/open" - '
                                                                     'открыть комнату(зайти может каждый), '
                                                                     '"/lock" - закрыть комнату (никто не может '
                                                                     'попасть в вашу комнату).', inline=False)
            he1.add_field(name='Могу ли я зарабатывать SH пока нахожусь в своей комнате?', value='Да, можете.',
                          inline=False)
            await ctx.send(embed=he1)
        # Кейсы
        elif state in ["кейсы", "кейс", "контейнеры"]:

            emb = discord.Embed(title="CaseHelp", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Кейсы.', value="На нашем сервере есть возможность покупать кейсы.", inline=False)
            emb.add_field(name='Как купить кейс?', value='Покупка кейса происходит командой "/buycase".', inline=False)
            emb.add_field(name='Какая стоимость кейса?', value="Стоимость одного кейса составляет 100.000 SH.",
                          inline=False)
            emb.add_field(name='Как узнать сколько у меня кейсов?', value="Это можно сделать командой '/case'.",
                          inline=False)
            emb.add_field(name='Как открыть кейс?', value='Открыть кейс можно при помощи команды "/opencase".',
                          inline=False)
            await ctx.send(embed=emb)


async def setup(bot):
    await bot.add_cog(Info())

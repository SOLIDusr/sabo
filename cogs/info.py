import discord
from discord.ext import commands
from configs.config import *

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents, help_command=None)


class Info(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['хелп', 'помощь'])
    async def help(self, ctx, state: str = None):

        states = ['валюта', "деньги", "вал", "казик", "казино", "казин", "роль", "роли", "войс", "комната", "голос",
                  "кейсы", "кейс", "контейнеры", "команды", "питомцы", "питомец"]

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
            emb.add_field(name='Бот Sabo',
                          value='Разработчики: @Director#6404, @St1zy3#8330. Информация по командам '
                                'сервера - /help команды. Если будут вопросы или баги связанные с ботом '
                                '- пишите.')
            emb.add_field(name='Что есть у нас в боте?',
                          value='Бот с каждым днем улучшается , но мы расскажем что есть на данный момент в нашем'
                                ' боте. Пройдем по порядку, попробуем объяснить кратко и понятно все по пунктам.'
                                ' Приступим.')
            emb.add_field(name='1. Валюта',

                          value='На нашем сервере есть своя валюта "SH", за эту валюту можно купить все на этом '
                                'сервере у чего только есть стоимость, как получать ее можете глянуть с помощью '
                                'команды "/help валюта".')
            emb.add_field(name='2. Куда тратить валюту?',
                          value='Как получать валюту разобрались, а тратить куда? Вообще способов не слишком много , '
                                'но думаем пока что неплохо, да и со временем их становится все больше. Сейчас все '
                                'расскажем подробнее.')
            emb.add_field(name='3. Казино',
                          value='У нас есть пару казино игр , в которых можно как и приумножить свой баланс , так '
                                'и потерять полностью, узнать подробнее про игры казино можно с помощью команды "/'
                                'help казино".')
            emb.add_field(name='4. Роли',
                          value='Еще один способ того как можно потратить валюту, у нас на сервере можно создать'
                                ' кастомную роль, естестенно не за бесплатно, подробнее читайте тут - "/help роли".')
            emb.add_field(name='5. Голосовые каналы.',
                          value='Интересный способ потратить валюту - создать приватный голосовой канал который можно'
                                ' настраивать (в данный момент открывать и закрывать), зачем? Ну там с кентами посидеть'
                                ' в компании и т.д, кому интересно - "/help войс".')
            emb.add_field(name='6. Кейсы',
                          value='Классная тема - Кейсы. Можно купить кейс и открыть его , после открытия кейса вам '
                                'выпадет какая - либо сумма денег , как и в казино можно поднять деньги , а можно и '
                                'уйти с пустым кошельком. Подробнее - "/help кейсы".')
            emb.add_field(name='7. Питомцы',
                          value='Тоже кейсы , но из них можно выбить питомцев с помощью которых можно получить очень'
                                ' классные эффекты , выбить питомцев довольно сложно и дорого, но я думаю это того стоит. Подробнее - "/help питомцы".')
            emb.add_field(name='Итоги',
                          value='Вроде самое основное вам поведал , вы все же почитайте , не зря же мы все это писали,'
                                ' а вообще спасибо, что пользуйтесь нашим ботом :)')
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
            emb.add_field(name='/help питомцы(В разработке!!)', value="Узнать о кейсах с питомцами и о"
                                                                      " самих питомцах.:leaves:",
                          inline=False)
            await ctx.send(embed=emb)

        # валюта

        elif state in ['валюта', "деньги", "вал"]:

            emb = discord.Embed(title="Информация о валюте", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Валюта данного сервера - "SH".', value="Чтобы ее получить нужно находиться в "
                                                                       "войсе.:leaves:", inline=False)
            emb.add_field(name='Система начисления.', value="1 минута в войсе = 20 SH.:leaves:", inline=False)
            emb.add_field(name='Для чего нужна данная валюта?:leaves:',
                          value="Мы объяснили все способы тратить нашу валюту в команде '/help'.:leaves:",
                          inline=False)

            await ctx.send(embed=emb)

        # казино

        elif state in ["казик", "казино", "казин"]:

            emb = discord.Embed(title="Игры, казино", colour=discord.Colour(0x3e038c))
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
            emb.add_field(name='Откуда брать валюту для игры в Казино?:leaves:', value="/help валюта", inline=False)
            await ctx.send(embed=emb)

        # Роли

        elif state in ["роль", "роли"]:

            emb = discord.Embed(title="Система покупки ролей", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Кастомные роли.', value="На нашем сервере есть возможность создать свою роль.",
                          inline=False)
            emb.add_field(name='Цена.',
                          value='Начнем с ценника, стоимость данной услуги составляет 10.000 SH, не дорого , уделив немного времени серверу , можно спокойно накопить и купить себе ту роль , которую вы хотите.',
                          inline=False)
            emb.add_field(name='Создание роли.', value="Пока что в разработке.'",
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

            emb = discord.Embed(title="Помощь по кейсам", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Кейсы.', value="На нашем сервере есть возможность покупать кейсы.", inline=False)
            emb.add_field(name='Как купить кейс?', value='Покупка кейса происходит командой "/case купить".',
                          inline=False)
            emb.add_field(name='Какая стоимость кейса?', value="Стоимость одного кейса составляет 10.000 SH.",
                          inline=False)
            emb.add_field(name='Как узнать сколько у меня кейсов?', value="Это можно сделать командой '/case'.",
                          inline=False)
            emb.add_field(name='Как открыть кейс?', value='Открыть кейс можно при помощи команды "/case открыть.',
                          inline=False)
            await ctx.send(embed=emb)

        # Питомцы

        elif state in ["питомцы", "питомец"]:

            emb = discord.Embed(title="Помощь по питомцам", colour=discord.Colour(0x3e038c))
            emb.add_field(name='Питомцы.', value="На нашем сервере есть возможность покупать кейсы с питомцами.",
                          inline=False)
            emb.add_field(name='Как купить кейс?', value='Покупка кейса происходит командой "/casepets купить".',
                          inline=False)
            emb.add_field(name='Какая стоимость данного кейса?', value="Стоимость одного кейса составляет 5.000 SH.",
                          inline=False)
            emb.add_field(name='Как узнать сколько у меня кейсов с питомцами?',
                          value="Это можно сделать командой '/casepets'.",
                          inline=False)
            emb.add_field(name='Как открыть кейс с питомцами?',
                          value='Открыть кейс можно при помощи команды "/casepets открыть".',
                          inline=False)
            emb.add_field(name='Какой шанс выбить питомца из кейса?', value='Очень маленький :)',
                          inline=False)
            emb.add_field(name='Для чего нужны питомцы?', value='Питомцы дают различные положительные эффекты.',
                          inline=False)
            emb.add_field(name='Каких питомцев можно выбить в данный момент?', value='Сейчас расскажу.',
                          inline=False)
            emb.add_field(name='1."Волк"', value='Данный питомец прибавляет процент от суммы выйгрыша в казино на 7%.',
                          inline=False)
            emb.add_field(name='Пример:',
                          value='Вы сыграли в казино на 50.000 SH, победили, вам прибавляется на баланс 50.000 SH которые вы выйграли и сверху 3.500 SH за счет того что у вас данный питомец.',
                          inline=False)
            emb.add_field(name='2."Лиса"',
                          value='Данный питомец прибавляет 7% SH от времени которое вы находились в голосовом канале.',
                          inline=False)
            emb.add_field(name='Пример:',
                          value='Вы просидели в голосовом канале 4 часа, после выхода вам начислятся 4.800 SH, за счет того что у вас данный питомец , вам сверху прибавится 336 SH.',
                          inline=False)
            emb.add_field(name='3."Собака"', value='Данный питомец возвращает вам 5 % от проигрыша в казино.',
                          inline=False)
            emb.add_field(name='Пример:',
                          value='Вы поставили в казино 5000 SH и проиграли , за счет того что у вас данный питомец, вам вернется 250 SH. :exclamation: Если ставка менее 100 SH возврата средств не будет :exclamation: .',
                          inline=False)
            emb.add_field(name='Как узнать какие у меня есть питомцы?', value='/mypets (В разработке)',
                          inline=False)
            emb.add_field(name=':exclamation: Важно :exclamation:',
                          value='Если у вас несколько питомцев , выбран может быть только один , выбрать питомца можно командой "/selectpet".',
                          inline=False)

            await ctx.send(embed=emb)


async def setup(bot):
    await bot.add_cog(Info())
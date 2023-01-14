import discord
from discord.ext import commands
import datetime
import asyncio
import psycopg2 as sql
from configs.database_config import *
from tools.logs import Log as logger


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
    exit()


cursor.execute(f'SELECT prefix FROM guilds WHERE id = 780063558482001950')
prefix = cursor.fetchone()[0]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
cost = 12000


class Voices(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['войс'])
    async def voice(self, ctx, move: str = None):

        moves = ['купить', 'buy', 'закрыть', 'remove', 'menu', 'меню']
        member_name = str(ctx.author.name)
        week_cost = 12_000

        if move not in moves:

            he1 = discord.Embed(title="[Voice]", colour=discord.Colour(0x3e038c))
            print('Пришли не туда')
            he1.add_field(name='Доступные команды:', value="/voice купить(buy)\n/voice закрыть(remove)\n/voice меню(menu)", inline=False)
            await ctx.send(embed=he1)
            
        elif move in ['купить, buy']:
            print('Пришли 1')
            cursor.execute("SELECT money FROM users WHERE id = {}".format(ctx.author.id))  # Присваиваем баланс из бд к переменной
            balance = cursor.fetchone()[0]
            purchase = 5500
            print(move)
            if balance < purchase:
                print('Пришли 2')
                he1 = discord.Embed(title="[Payment]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
                await ctx.send(embed=he1)

            else:
                print('Пришли 2.5')
                cursor.execute(f"UPDATE users SET money = money - {purchase} WHERE id={ctx.author.id}")
                guild = ctx.guild
                data_base.commit()
                channel = await guild.create_voice_channel(member_name+'`s room')
                insert_query = """ INSERT INTO channels (id, ownerid, create_time)
                                              VALUES (%s, %s, %s)"""
                timestamp = datetime.datetime.now()
                item_tuple = (channel.id, ctx.author.id, timestamp)
                cursor.execute(insert_query, item_tuple)
                data_base.commit()
                he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Голосовой канал создан.',
                              value="Внесите недельный платеж в течение 5-и минут, иначе он будет"
                                    " удален.",
                              inline=False)
                he1.add_field(name='Управление каналом.', value="/voicemenu", inline=False)
                he1.add_field(name='Помощь с личным каналом.', value="/voicehelp", inline=False)
                await ctx.send(embed=he1)
                await asyncio.sleep(300)
                cursor.execute(f'SELECT account FROM channels WHERE id = {channel.id}')
                channel_balance = cursor.fetchone()[0]
                cursor.execute(f'SELECT id FROM channels WHERE id = {channel.id}')
                channel_id = cursor.fetchone()[0]

                if channel_balance < week_cost:

                    await bot.get_channel(channel_id).delete()

                else:

                    timestamp = datetime.datetime.now()
                    cursor.execute(f'UPDATE channels SET account = account - {week_cost} WHERE ownerid = {ctx.author.id}')
                    cursor.execute(f'UPDATE channels SET last_payment = {timestamp} WHERE ownerid = {ctx.author.id}')
                    data_base.commit()

        elif move in ['удалить', 'remove']:

            timestamp = datetime.datetime.now()
            cursor.execute(f'SELECT id FROM channels WHERE ownerid={ctx.author.id}')
            channel_id = cursor.fetchone()[0]
            cursor.execute(f'SELECT account FROM channels WHERE ownerid={ctx.author.id}')
            channel_account = cursor.fetchone()[0]
            cursor.execute(f'SELECT last_payment FROM channels WHERE ownerid={ctx.author.id}')
            payment_date = cursor.fetchone()[0]
            channel = bot.get_channel(channel_id)
            delta = timestamp - payment_date
            cashback = ((week_cost // 7) * (7 - delta.days)) // 2
            cashback += (channel_account * 0.7)
            await channel.delete()
            he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Голосовой канал удалён.',
                          value=f"Голосовой канал был удалён. Ваша компенсация за удаление составила {cashback}",
                          inline=False)
            await ctx.send(embed=he1)
            cursor.execute(f'UPDATE users SET money = money + {cashback} WHERE id = {ctx.author.id}')
            cursor.execute(f'DELETE FROM channels WHERE ownerid = {ctx.author.id}')
            data_base.commit()

        elif move in ['закрыть', 'lock']:

            await ctx.channel.purge(limit=1)
            channel_id = cursor.fetchone()[0]
            cursor.execute(f'SELECT id FROM channels WHERE ownerid={ctx.author.id}')
            channel = bot.get_channel(channel_id)
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        elif move in ['открыть', 'open']:
            await ctx.channel.purge(limit=1)
            channel_id = cursor.fetchone()[0]
            cursor.execute(f'SELECT id FROM channels WHERE ownerid={ctx.author.id}')
            channel = bot.get_channel(channel_id)
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        elif move in ['оплатить', 'pay']:
            cursor.execute(f'SELECT money FROM users WHERE id = {ctx.author.id}')
            balance = cursor.fetchone()[0]
            week_cost = 12_000

            if balance >= week_cost:

                cursor.execute(f'UPDATE users SET money = money- {week_cost} WHERE id={ctx.author.id}')
                cursor.execute(f'UPDATE channels SET account = account - {week_cost}')
                data_base.commit()
                he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Оплата за голосовой канал произведена.',
                              value=f"На счет вашего канала была положна еженедельная сумма в {week_cost}.",
                              inline=False)
                await ctx.send(embed=he1)

            else:

                he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Оплата за голосовой канал *НЕ* произведена.',
                              value=f"На вашем счету должно быть хотя бы {week_cost}.",
                              inline=False)
                await ctx.send(embed=he1)


async def setup(bot):
    await bot.add_cog(Voices())



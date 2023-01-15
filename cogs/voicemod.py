import discord
from discord.ext import commands
import datetime
import asyncio
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request


bot = Request.get_bot()

class Voices(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['войс'])
    async def voice(self, ctx, move: str = None):

        member: discord.Member = ctx.author
        moves = ['купить', 'buy', 'закрыть', 'remove', 'menu', 'меню']
        member_name = str(ctx.author.name)
        week_cost = 12_000

        if move not in moves:

            he1 = discord.Embed(title="[Voice]", colour=discord.Colour(0x3e038c))
            print('Пришли не туда')
            he1.add_field(name='Доступные команды:', value="/voice купить(buy)\n/voice закрыть(remove)\n/voice меню(menu)", inline=False)
            await ctx.send(embed=he1)
            
        elif move in ['купить, buy']:

            balance = Request.Get.balance_by_id(member.id)
            purchase = 5500
            print(move)
            if balance < purchase:

                he1 = discord.Embed(title="[Payment]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Ошибка оплаты.', value="Недостаточно средств!", inline=False)
                await ctx.send(embed=he1)

            else:
                Request.Update.balance(member.id, -purchase)
                guild = ctx.guild
                channel = await guild.create_voice_channel(member_name+'`s room')
                insert_query = """ INSERT INTO channels (id, ownerid, create_time, discord_id)
                                              VALUES (%s, %s, %s)"""
                timestamp = datetime.datetime.now()
                discord_id = channel.id
                item_tuple = (channel.id, ctx.author.id, timestamp, discord_id)
                cursor.execute(insert_query, item_tuple)
                he1 = discord.Embed(title="[VoiceManager]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Голосовой канал создан.',
                              value="Внесите недельный платеж в течение 5-и минут, иначе он будет"
                                    " удален.",
                              inline=False)
                he1.add_field(name='Управление каналом.', value="/voicemenu", inline=False)
                he1.add_field(name='Помощь с личным каналом.', value="/voicehelp", inline=False)
                await ctx.send(embed=he1)
                await asyncio.sleep(300)
                channel_balance = Request.Get.channel_account(discord_id)

                if channel_balance < week_cost:

                    await bot.get_channel(channel_id).delete()

                else:

                    timestamp = datetime.datetime.now()
                    Request.Update.any('channels', 'account', -week_cost, 'ownerid', member.id)
                    Request.Set.any('channels', 'last_payment', timestamp, 'ownerid', member.id)

        elif move in ['удалить', 'remove']:

            timestamp = datetime.datetime.now()
            channel_id = Request.Get.channel_discordid(member.id)
            channel_account = Request.Get.channel_account(member.id)
            payment_date = Request.Get.channel_payment_ownerid(member.id)
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
            Request.Update.balance(member.id, cashback)
            Request.Remove.any('channels', 'ownerid', member.id)

        elif move in ['закрыть', 'lock']:

            await ctx.channel.purge(limit=1)
            channel_id = Request.Get.channel_discordid(member.id)
            channel = bot.get_channel(channel_id)
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        elif move in ['открыть', 'open']:
            await ctx.channel.purge(limit=1)
            channel_id = Request.Get.channel_discordid(member.id)
            channel = bot.get_channel(channel_id)
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

        elif move in ['оплатить', 'pay']:
            balance = Request.Get.balance_by_id(member.id)
            week_cost = 12_000

            if balance >= week_cost:
                
                Request.Update.balance(member.id, -week_cost)
                Request.Update.channel_account_by_ownerid(member.id, week_cost)
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



#  Модерирование бота
#  Выдача: Времени/Лвла Установка джекпота и кик
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request
import datetime as dtt


bot = Request.get_bot()

class Moderation(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=["kick", "кик", "выгнать"])
    @has_permissions(manage_roles=True, ban_members=True)
    async def _kick(self, ctx, intruder: discord.Member = None, reason: str = None):
        if intruder is None:
            await ctx.send('Не указан участник для кика.')
        else:
            await intruder.kick()
            if reason is not None:
                await ctx.send(f'Участник {intruder} был выгнан с сервера участником {ctx.message.author} по причине'
                               f' {reason}.')

    @_kick.error
    async def _kick_error(ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await bot.send_message(ctx.message.channel, text)
    
    @commands.command(aliases=["jackpot", "kush", "куш"])
    @has_permissions(ban_members=True)
    async def _jackpot(self, ctx, amount):
        Request.Set.any('guilds', 'jackpot', amount, 'id', 780063558482001950)
        await ctx.send('Jackpot был изменен!')
    
    @commands.command(aliases=["setlvl", "lvlset", "lvladd"])
    @has_permissions(manage_roles=True, ban_members=True)
    async def _lvl(self, ctx, intruder: discord.Member = None, amount: int = 1):
        if intruder is None:
            await ctx.send('Не указан участник.')
        else:
            Request.Update.lvl(intruder.id, amount)
            await ctx.send('GJ.')

    @_lvl.error
    async def _lvl_error(ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await bot.send_message(ctx.message.channel, text)
    
    @commands.command(aliases=["settime", "timeset", "set_time"])
    @has_permissions(manage_roles=True, ban_members=True)
    async def _timer(self, ctx, intruder: discord.Member = None, amount:int = None):

        if intruder is None:
            await ctx.send('Не указан участник.')
        if amount == None:
            amount = dtt.timedelta(hours=1)
        else:
            amount = dtt.timedelta(hours=amount)
            Request.Set.voicetime(intruder.id, amount)
            await ctx.send('GJ.')

    @_timer.error
    async def _timer_error(ctx, error):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await bot.send_message(ctx.message.channel, text)

    @commands.command(aliases=['logger', 'log'])
    async def _log(self, ctx):

        logger.info('DISCORD REQUEST!')

# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Moderation())


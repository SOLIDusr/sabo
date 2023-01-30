import discord
import random
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request


bot = Request.get_bot()

class Gambling(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['Казино', 'казино', 'casino', 'Casino'])
    async def _casino(self, ctx, amount: int = None):
        member = ctx.author
        balance = Request.Get.balance_by_id(member.id)
        number = random.randint(1, 100)
        jackpot = Request.Get.jackpot(780063558482001950)

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
            response = Request.Update.balance(member.id, -amount)
            if number < 50:
                if response is Exception:
                    ctx.send('Произошла ошибка! Уведомите Администратора.')
                    logger.error(f'Error occured while updating variable! Error:\n{response}')
                else:
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                    await ctx.send(embed=embed)

            elif number == 93:
                response = Request.Update.balance(member.id, jackpot+amount)
                if response is Exception:
                    ctx.send('Произошла ошибка! Уведомите Администратора.')
                    logger.error(f'Error occured while updating variable! Error:\n{response}')
                else:
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Вы выйграли JACKPOT! Мы добавили вам на баланс:',
                                    value=f'{jackpot} SH', inline=False)
                    await ctx.send(embed=embed)


            else:
                Request.Update.balance(member.id, amount*2)
                if response is Exception:
                    ctx.send('Произошла ошибка! Уведомите Администратора.')
                    logger.error(f'Error occured while updating variable! Error:\n{response}')
                else:
                    embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                    embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount} SH', inline=False)
                    await ctx.send(embed=embed)

    @commands.command(aliases=['Рулетка', 'рулетка', 'roulette', 'roll'])
    async def _roulette(self, ctx, amount: int = None, count: int = None):
        member:discord.Member = ctx.author
        number = random.randint(0, 36)
        balance = Request.Get.balance_by_id(member.id)

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
            Request.Update.balance(member.id, -amount)
            if count != number:
                
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Вы проиграли в казино, у вас отняли:', value=f'{amount} SH', inline=False)
                embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                await ctx.send(embed=embed)
                amount = 0 - amount


            elif count == number:

                Request.Update.balance(member.id, amount*36)
                embed = discord.Embed(title=f'[CASINO]', color=0x42f566)
                embed.add_field(name='Поздравляю! Вы выйграли:', value=f'{amount * 36} SH', inline=False)
                embed.add_field(name='Выпало число:', value=f'{number} SH', inline=False)
                await ctx.send(embed=embed)


    @commands.command(aliases=["кейс", "кейсы", "контейнер", "case"])
    async def _case(self, ctx, move: str = None):
        member: discord.Member = ctx.author
        moves = ["открыть", "купить", "buy", "open"]
        balance, keys = Request.Get.balance_by_id(member.id), Request.Get.keys(member.id)

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

            val = 1

            if keys >= 1:
                keys = Request.Update.keys(member.id, -val)
                rand = random.randint(0, 100)

                if 0 <= rand <= 70:

                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="К сожалению вам ничего не выпало.",
                                  inline=False)
                    await ctx.send(embed=emb)

                elif 71 <= rand <= 80:

                    Request.Update.balance(member.id, 400_000)
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 400.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 81 <= rand <= 90:

                    Request.Update.balance(member.id, 800_000)
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успено открыли кейс.', value="Вам выпало 800.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 91 <= rand <= 95:
                    Request.Update.balance(member.id, 1_600_000)
                    emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                    emb.add_field(name='Вы успешно открыли кейс.', value="Вам выпало 1.600.000SH", inline=False)
                    await ctx.send(embed=emb)

                elif 96 <= rand <= 100:

                    Request.Update.balance(member.id, 5_555_555)
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
                
                Request.Update.balance(member.id, -cent)
                Request.Update.keys(member.id, val)
                emb = discord.Embed(title="[CASE]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Успешно.', value="Кейс был куплен, для открытия введите '"
                                                     "/case открыть или /case open'.", inline=False)
                await ctx.send(embed=emb)

    @commands.command(aliases = ['slots', 'slot', 'слоты'])
    async def _slots(self, ctx, amount: int = None):
        member: discord.Member = ctx.author
        choices = ["🪙", "💵", "⚡", "💎","🔥", " "]
        balance = Request.Get.balance_by_id(member)
        mult_points = 1
        combo = 0
        #  slots statement
        slots = []
        for n in range(25):
            slots.append(random.choice(choices))
        
        #  combos

        #  all in
        for i in range(1, 5):
            
            for item in range(0, 3):
                if slots[item*i] == slots[item*i+1]:
                    combo += 1
                    mult_points += 5
                else:break
                if combo == 5:
                    print('win')
                else:print('loose')
        #  lightning
        for i in range(0, 3):
            if slots[0 + 5 * i] == slots[1] == slots[2] == slots[7] == slots[8] == slots[9]:
                mult_points += 0.3
                combo += 1
    
        if combo in range(2, 3):
            mult_points += 30

        if combo == 4:
            mult_points += 50
        
        
        
# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Gambling())

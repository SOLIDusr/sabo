from discord.ui import Select, View
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request
import random


bot = Request.get_bot()

class Pets(commands.Cog):

    def __init__(self):
        self.bot = bot

    @commands.command()
    async def pets(self, ctx, move: str = None):
        moves = ["открыть", "купить", "buy", "open", "select", "выбрать", "active"]
        effects = ''
        member = ctx.author
        user_pets, casepets, balance, active_pet = Request.Get.pets(member.id),\
                            Request.Get.casepets(member.id), Request.Get.balance_by_id(member.id), Request.Get.pet_active(member.id)

        if active_pet == 'wolf':
            effects += 'Прибавляет процент от суммы выйгрыша в казино на 7%\n'
        elif active_pet == 'fox':
            effects += 'Прибавляет 7% SH от времени которое вы находились в голосовом канале.\n'
        elif active_pet == 'dog':
            effects += 'Возвращает вам 5 % от проигрыша в казино.'
        else :
            effects = 'У вас нет активного питомца...'

        if move is None:

            embed = discord.Embed(title='[Pets]',color=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f'{member}')
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name='Ваши питомцы:🎒', value=user_pets, inline=False)
            embed.add_field(name='Активный питомец:✅', value=active_pet, inline=False)
            embed.add_field(name='Эффект от питомца:🪄', value=effects, inline=False)
            embed.add_field(name='У вас в наличии:', value=f'{casepets} кейсов с питомцами.', inline=False)
            embed.add_field(name='Доступные команды:🎚️', value='/pets купить(buy) - купить кейс с питомцами\n'
                    '/pets открыть(open) - открыть кейс\n/pets select - выбрать активного питомца')

            await ctx.send(embed=embed) 

        elif move is not None and move not in moves:

            emb = discord.Embed(title='[ERROR] CasePets',
                                description=f'{ctx.author.mention}, Укажите правильное действие!',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Действия:', value=f'{moves}', inline=False)
            emb.add_field(name='Пример :', value='/casepets открыть')
            await ctx.send(embed=emb)

        elif move in ['окрыть', 'open']:

            casepets = Request.Get.casepets(member.id)

            val = 1

            if casepets >= 1:

                rand = random.randint(0, 50)
                if rand == 6:

                    if 'wolf' in user_pets:

                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='[Итог]', value="Вам бы выпал питомец 'Волк', но он у вас уже есть. Кейс "
                                                           "не был потрачен",
                                      inline=False)
                        await ctx.send(embed=emb)

                    else:
                        Request.Update.casepets(member.id, -val)
                        user_pets.append('wolf')
                        Request.Update.pet_has(member.id, user_pets)
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

                    else:
                        Request.Update.casepets(member.id, -val)
                        user_pets.append('fox')
                        Request.Update.pet_has(member.id, user_pets)
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
                        await ctx.send(embed=emb)

                    else:
                        Request.Update.casepets(member.id, -val)
                        user_pets.append('dog')
                        Request.Update.pet_has(member.id, user_pets)
                        emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                        emb.add_field(name='Поздравляем.', value="Вам выпал питомец 'Собака'.", inline=False)
                        emb.add_field(name='Питомец "Собака".',
                                      value="Данный питомец возвращает вам 5 % от проигрыша в казино.",
                                      inline=False)
                        emb.add_field(name='Пример:".',
                                      value="Вы поставили в казино 5000 SH и проиграли , за счет того что у вас "
                                            "данный питомец, вам вернется 250 SH. :exclamation: Если ставка менее"
                                            " 100 SH возврата средств не будет :exclamation: ",
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
                Request.Update.balance(member.id, -price)
                Request.Update.casepets(member.id, val)
                emb = discord.Embed(title="[CasePets]", colour=discord.Colour(0x3e038c))
                emb.add_field(name='Успешно.',
                              value="Кейс с питомцами был куплен, для открытия введите '/casepets открыть"
                                    " или /casepets open'.",
                              inline=False)
                await ctx.send(embed=emb)

        elif move in ['select', 'выбрать', 'active']:

            user_pets, active_pet = Request.Get.pets(member.id), Request.Get.pet_active(member.id)

            select = Select(

                options=[
                    discord.SelectOption(
                        label="wolf",
                        emoji="🐺"
                    ),

                    discord.SelectOption(
                        label="fox",
                        emoji="🦊"
                    ),

                    discord.SelectOption(
                        label="dog",
                        emoji="🐶"
                    )
                ])

            async def my_callback(interaction):  # Если namepet active - выбран данный питомец

                if select.values[0] not in user_pets:
                    await ctx.send('У вас нет данного питомца.')

                else:

                    if select.values[0] == active_pet:
                        await ctx.send('Данный питомец уже установлен как активный!')
                        
                    else:
                        Request.Update.pet_active(member.id, select.values[0]) 
                        await ctx.send('Активный питомец установлен.')

                await interaction.response.defer()

            select.callback = my_callback
            view = View()
            view.add_item(select)
            await ctx.send("Выбор питомца:", view=view)

# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Pets())

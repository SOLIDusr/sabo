import discord
from discord.ext import commands
from discord.ui import Button, View
from tools.logs import Log as logger
from tools.db_connect import cursor
from tools.db_request import Request


bot = Request.get_bot()

class Roles(commands.Cog):
    def __init__(self):
        self.bot = bot

    @commands.command(aliases=['rolebuy', 'buyrole'])
    async def _rolebuy(self, ctx, num:int = None):
 
        cursor.execute(f'SELECT id FROM roles_shop')
        idss = cursor.fetchall()
        member:discord.Member = ctx.author
        ids = []
        for id in idss:
            ids.append(id[0])

        if num is None:

            ctx.send('Вы не ввели обязательный параметр числа!')

        elif num not in ids:

            he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
            he1.add_field(name='Ошибка!', value="Используйте правильный номер роли.", inline=False)
            he1.add_field(name='Покупка', value="/role купить", inline=False)
            await ctx.send(embed=he1)

        else:

            role_cost, discord_id = Request.Get.role_cost(num), Request.Get.role_discord(num)
            balance = Request.Get.balance_by_id(member.id)

            if balance < role_cost:
                he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Спасибо за покупку!',
                            value="Хотелось бы так сказать, но у вас не хватило средств :(.",
                            inline=False)
                await ctx.send(embed=he1)
            
            elif discord_id in member.roles:
                he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Спасибо за покупку!',
                            value="Хотелось бы так сказать, но у вас уже есть эта роль :)   .",
                            inline=False)
                await ctx.send(embed=he1)
            else:
                user: discord.Member = ctx.author
                Request.Update.balance(member.id, -role_cost)
                role = discord.utils.get(ctx.guild.roles, id=discord_id)
                await user.add_roles(role)
                
                he1 = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                he1.add_field(name='Вниание!', value="Система искренне завидует вашей покупке.", inline=False)
                await ctx.send(embed=he1)

    @commands.command(aliases=['role', 'roles', 'роль', 'роли'])  # создание роли
    async def _role(self, ctx, move:str = None):
        
        moves = ['купить', 'покупка', 'buy', 'shop', 'магазин']
        
        if move is None:

            async def custom_role_shop():

                await ctx.send('Введите "/custom {имя роли} {Цвет Роли}" чтобы создать свою роль.')

            async def existing_role_shop():
                embi = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
                embi.add_field(name='', value="Выберите интересующую вас роль.", inline=False)
                cursor.execute(f'SELECT id FROM roles_shop')
                choise_ids = cursor.fetchall()

                for item in choise_ids:
                    choise_cost = Request.Get.role_cost(item[0])
                    name = Request.Get.role_name(item[0])

                    embi.add_field(name=f'Роль №{item[0]} - {name}', value=f'Цена - {choise_cost} SH',
                                   inline=False)
                embi.add_field(name='Для покупки напишите', value='/rolebuy [id роли]')
                await ctx.send(embed=embi)

            # Ответы от нажатий кнопок

            async def custom_role_call(inter):
                await inter.response.defer()
                await custom_role_shop()

            async def buyrole_call(inter):
                await inter.response.defer()
                await existing_role_shop()

            emb = discord.Embed(title='[RoleShop]',
                                description="Тут вы можете купить индивидуальную роль с помощью виртуальной "
                                            "валюты.", colour=discord.Colour.purple())
            emb.add_field(name='RoleShop', value='Все категории представлены ниже', inline=False)
            roles_b = Button(label='Досупные роли', style=discord.ButtonStyle.primary, emoji='👑')
            custom_role_b = Button(label='Личная роль', style=discord.ButtonStyle.primary,
                                   emoji='<:booster:1029482318118797412>')

            custom_role_b.callback = custom_role_call
            roles_b.callback = buyrole_call
            view = View()
            view.add_item(custom_role_b)
            view.add_item(roles_b)

            await ctx.send(embed=emb, view=view)

    @commands.command(aliases=['customize', 'custom', 'кастом', 'customise'])
    async def _custom(self, ctx, role_name:str = None, role_colour:discord.Color = None):
        member: discord.Member = ctx.author

        FORBIDDEN = ['staff', 'dev', 'developer', 'devops', 'admin', 'admins', 'moderator', 'mods', 'moder', 'mod', 'owner', 'robot',
                    'headquaters', 'event mod', 'booster', 'the chosen one [Tier-5]', 'protector [Tier-4], duelist [Tier-3]']

        if role_colour is None:

            role_colour = member.color

        colours = ['red', 'purple', 'green', 'blue']

        balance = Request.Get.balance_by_id(member.id)

        if (role_name is None or role_colour is None or role_colour not in colours) or len(role_name) >= 16 or role_name.lower in FORBIDDEN:

            embi = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
            embi.add_field(name='', value="Неправильно указаны цвет или имя роли!.", inline=False)
            embi.add_field(name='Пример', value="/custom {Имя роли} {Цвет Роли}!.", inline=False)
            embi.add_field(name='Цвета', value="красный - red\n\nфиолетовый - purple\nСиний -  blue\nЗеленый - green.", inline=False)
            await ctx.send(embed=embi)

        elif balance < 500_000:

            embi = discord.Embed(title="[RoleShop]", colour=discord.Colour(0x3e038c))
            embi.add_field(name='Недостаточно средств!', value=f"Не хватает - {500_000 - balance}", inline=False)
            await ctx.send(embed=embi)
        
        else:

            guild = ctx.guild
            Request.Update.balance(member.id, -500000)
            role = await guild.create_role(name=role_name, colour=role_colour, hoist=True, mentionable=True)
            await member.add_roles(role)
            emb=discord.Embed(
                title='Создание Личной Роли',
                description=f'{ctx.author.mention}, вы успешно **создали** роль {role.mention}.'
            )
            emb.set_thumbnail(url=ctx.author.avatar.url)
            await ctx.send(embed=emb)
            positions = {
                role: 11
            }
            await guild.edit_role_positions(positions=positions)



# noinspection PyShadowingNames
async def setup(bot):
    await bot.add_cog(Roles())

import os
import discord
from tools.logs import Log as logger


async def manage_plugins(ctx, bot, move) -> bool | Exception:
    try:
        directory = os.listdir("./cogs")
        logger.debug(f'Found cogs - {directory}')
        moves = ['-l', '-r', '-u']
        if move is None:

            for filename in os.listdir("./cogs"):  # перебирает все файлы в выбранной папке

                if filename.endswith(".py"):

                    await ctx.send(f'Плагин - {filename[:-3]} существует!')

            await ctx.send('/plugin -l чтобы загрузить')
            return True

        if move is not None and move not in moves:

            emb = discord.Embed(title='[ERROR] plugin', description=f'{ctx.author.mention}, Укажите приемлемое действие',
                                colour=discord.Colour(0xe73c3c))
            emb.add_field(name='Действия:', value='-r - restart, -l - load, -u - unload', inline=False)
            emb.add_field(name='Пример :', value='/plugin -r')
            await ctx.send(embed=emb)
            return True

        elif move == '-l':

            for filename in directory:  # перебирает все файлы в выбранной папке

                if filename.endswith(".py"):

                    await bot.load_extension(f"cogs.{filename[:-3]}")  # загрузка КОГов в основной файл
                    logger.info(f'Extension {filename} loaded')
            await ctx.send('Plugins loaded')
            return True

        elif move == '-u':

            for filename in directory:

                if filename.endswith(".py"):

                    await bot.unload_extension(f"cogs.{filename[:-3]}")

            await ctx.send('Plugins unloaded')
            logger.info(f'Extension {filename} unloaded')
            return True

        elif move == '-r':

            for filename in directory:

                if filename.endswith(".py"):

                    await bot.reload_extension(f"cogs.{filename[:-3]}")
                    
            logger.info(f'Extension {filename} reloaded')
            await ctx.send('Plugins reloaded')
            return True

    except Exception as _ex:
        return _ex
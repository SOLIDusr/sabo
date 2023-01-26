from tools.db_connect import cursor
import psycopg2 as sql
from datetime import datetime, timedelta
from discord.ext import commands
import discord
import random

class Request():

    """The system of calls and queries to the database.

    In case of Exceptions and errors, any function will return :class:`Exception`

    Sub-classes
    -----------
    Get():
        Any function of this class will Fetch and get 
        any Information from the Database 
        selected column and from selected table.
        Returns an object :type:`Any:...` from the Database. 
        In case of errors, will return :class:`Exception`
    Set():
        Any function of this class will Set selected column 
        from selected table to any Value you write in.
        Returns an object :type:`bool` if succeed. 
        In case of errors, will return :class:`Exception`
    Insert():
        Any function of this class will Insert selected column
        and value to selected table you write in.
        Returns an object :type:`bool` if succeed. 
        In case of errors, will return :class:`Exception`
    Remove():
        Any function of this class will Remove
        selected row from selected table  you write in.
        Returns an object :type:`bool` if succeed. 
        In case of errors, will return :class:`Exception`
    Update():
        Any function of this class will Update selected row
        from selected table to any Value you write in.
        Update - add to existing Value.
        Returns an object :type:`bool` if succeed. 
        In case of errors, will return :class:`Exception`
    """



    def __init__(self) -> None:
        pass
    
    def get_bot() -> commands.Bot | Exception:
        prefix = Request.Get.any('prefix', 'guilds', 'id', '780063558482001950')
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)
        return bot

    class Get():

        """Helps getting any Value from the Database

        In case of Exceptions and errors, any function will return :class:`Exception`

        Unclassified methods
        -----------
        any()

        User methods
        -----------
        balance_by_id() - User's balance by his Discord ID

        balance_by_nickname() - User's balance by his Database Nickname

        name() - User's nickname by his Discord ID

        keys() - User's case's keys by his Discord ID

        voicetime() - User's voicetime variable by his Discord ID

        casepets() - Amount of User's pets' cases by his Discord ID

        pets() - The list of User's pets by his Discord ID

        pet_active - User's active pet by his Discord ID

        Casino methods
        -----------

        jackpot() - Server's jackpot amound by it's Discord ID

        Roles methods
        -----------

        role_cost() - Role's cost by it's generated ID

        role_discord() - Role's discord Id by it's generated ID

        role_name() - Role's name by it's generated ID

        Channels methods
        -----------

        channel_account() - Channel's balance by owner's Discord ID

        channel_discordid() - Channel's Discord ID by owner's Discord ID

        channel_id() - Channel's generated ID by owner's Discord ID

        channel_ownerid() - Channel's owner Discord Id by it's generated ID

        channel_payment_ownerid() - Channel's last payment date by it's owner's Discord ID
        
        """
        
        def __init__(self) -> None:
            pass
        
        def any(column: str, table: str, indexer: str, value):
            """
            Arguments
            ---------
            column :type:`str`- Existing Column in the Table

            table :type:`str` - Existing table in the Database

            indexer :type:`str` - indexer of the row

            value :type:`None` - Any type value of indexer

            Returns
            --------
            cursor.fetchone()[0] or :type:`Exception`
            
            """
            try:
                cursor.execute(f"SELECT {column} FROM {table} WHERE {indexer} = {value}")
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex

# --------------------------------------Users---------------------------------------------

        def balance_by_id(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's balance :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT money FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def balance_by_nickname(name: str) -> int | Exception:
            """
            Arguments
            ---------
            name :type:`str` - Username of a Member

            Returns
            --------
            User's balance :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT money FROM users WHERE nickname = {name}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def name(id: int) -> str | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's nickname :type:`str` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT nickname FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex

        def keys(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's keys value :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT keys FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def voicetime(id: int):
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's time in the voice :type:`timedelta` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT voicetime FROM users WHERE id = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def casepets(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's amunt of pets' case :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT casepets FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pets(id: int) -> list | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            List of user's pets :type:`list` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT pet_has FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pet_active(id: int) -> str | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's active pet :type:`str` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT pet_has FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def lvl(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's lvl :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT lvl FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex

        def exp(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Discord ID of a Member

            Returns
            --------
            User's exp :type:`str` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT exp FROM users WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
#  -------------------------------Casino----------------------------------------------------------

        def jackpot(server_id: int) -> int | Exception:
            """
            Arguments
            ---------
            server_id :type:`int` - Server discord ID 

            Returns
            --------
            Amount of jackpot :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT jackpot FROM guilds WHERE id = {server_id}')
                jackpot_mid = cursor.fetchone()[0]
                jackpot_min = jackpot_mid * 0.5
                jackpot_max = jackpot_mid * 1.5
                jackpot = random.randint(jackpot_min, jackpot_max)
                return jackpot

            except (Exception, sql.Error) as _ex:
                return _ex

#  --------------------------Roles-----------------------------------------------------------------

        def  role_cost(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Generated Role ID

            Returns
            --------
            Role's cost :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT role_cost FROM roles_shop WHERE id = {id}')
                return cursor.fetchone()[0]

            except(Exception, sql.Error) as _ex:
                return _ex
        
        def  role_discord(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Generated Role ID

            Returns
            --------
            Role's Discord ID :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT discord_id FROM roles_shop WHERE id = {id}')
                return cursor.fetchone()[0]

            except(Exception, sql.Error) as _ex:
                return _ex
        
        def  role_name(id: int) -> str | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Generated Role ID

            Returns
            --------
            Role's name :type:`str` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT role_name FROM roles_shop WHERE id = {id}')
                return cursor.fetchone()[0]

            except(Exception, sql.Error) as _ex:
                return _ex

#  --------------------------Channels-------------------------------------------------------------- 
       
        def channel_account(ownerid: int) -> int | Exception:
            """
            Arguments
            ---------
            ownerid :type:`int` - Channel's owner ID

            Returns
            --------
            Channel's balance :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT account FROM channels WHERE ownerid = {ownerid}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        def channel_discordid(ownerid: int) -> int | Exception:
            """
            Arguments
            ---------
            ownerid :type:`int` - Channel's owner ID

            Returns
            --------
            Channel's Discord ID :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT discord_id FROM channels WHERE ownerid = {ownerid}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex

        def channel_id(ownerid: int) -> int | Exception:
            """
            Arguments
            ---------
            ownerid :type:`int` - Channel's owner ID

            Returns
            --------
            Channel's generated ID :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT id FROM channels WHERE ownerid = {ownerid}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex

        def channel_ownerid(id: int) -> int | Exception:
            """
            Arguments
            ---------
            id :type:`int` - Channel's generated ID

            Returns
            --------
            Channel's owner ID :type:`int` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT ownerid FROM channels WHERE id = {id}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def channel_payment_ownerid(ownerid: int) -> datetime | Exception:
            """
            Arguments
            ---------
            ownerid :type:`int` - Channel's owner ID

            Returns
            --------
            Channel's time of last payment :type:`datetime` or :type:`Exception`
            """
            try:
                cursor.execute(f'SELECT last_payment FROM channels WHERE ownerid={ownerid}')
                return cursor.fetchone()[0]

            except (Exception, sql.Error) as _ex:
                return _ex
                        

    class Set():
        """Helps Setting completely new Value into the Database

        In case of Exceptions and errors, any function will return :class:`Exception`

        Methods
        -----------
        any() - Set anything into anywhere
        
        """

        def __init__(self) -> None:
            pass

        def any(table: str, column: str, value, indexer: str, var) -> bool | Exception:
            """
            Arguments
            ---------
            table :type:`str` - Database table
            column :type:`str` - Database column
            value :type:`Any:...` - Value to put into column
            indexer :type:`str` - Identificator of a row
            var :type:`Any:...` - Value of an Identificator

            Returns
            --------
            :type:`bool` or :type:`Exception`
            """
            try:
                cursor.execute(f'UPDATE {table} SET {column} = {value} WHERE {indexer} = {var}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

# ------------------------------------Users-----------------------------------------------------------------

        def balance_by_id(id: int, value: int) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE users SET money = {value} WHERE id = {id}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def balance_by_nickname(name: str, value: int) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE users SET money = {value} WHERE nickname = {name}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        def keys(id: int, value: int) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE users SET keys = {value} WHERE id = {id}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def voicetime(id: int, value: timedelta) -> bool | Exception:
            try:
        
                cursor.execute('UPDATE users SET voicetime = (%s) WHERE id = %s', (value, id))
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def casepets(id: int, value: int) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE users SET casepets = {value} WHERE id = {id}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pets(id: int, value: list) -> bool | Exception:
            try:
                cursor.execute('UPDATE users SET pet_has = \'{{{}}}\' WHERE id = {}'.format(','.join(value), id))
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pet_active(id: int, value: str) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE users SET pet_active = {value} WHERE id = {id}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

    class Insert():

        def __init__(self) -> None:
            pass
            
        def any(table, column, value) -> bool | Exception:
            try:
                cursor.execute(
                        f"INSERT INTO {table} ({column}) VALUES ({value}),")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
    
    class Remove():

        def __init__(self) -> None:
            pass
    
        def any(table, indexer, value) -> bool | Exception:
            try: 
                cursor.execute(f'DELETE FROM {table} WHERE {indexer} = {value}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
    
    class Update():
        
        def __init__(self) -> None:
            pass

        def any(table, column, adding, indexer, value) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE {table} SET {column} = {column} + {adding} WHERE {indexer} = {value}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
# ------------------------------------Users-----------------------------------------------------------------
        def balance(id: int, adding: int) -> bool | Exception:
            try:
                cursor.execute(f"UPDATE users SET money = money + {adding} WHERE id = {id}")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        def keys(id: int, adding: int) -> bool | Exception:
            try:
                cursor.execute(f"UPDATE users SET keys = keys + {adding} WHERE id = {id}")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        def casepets(id: int, adding:int) -> bool | Exception:
            try:
                cursor.execute(f"UPDATE users SET casepets = casepets + {adding} WHERE id = {id}")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        def pet_has(id: int, adding:list) -> bool | Exception:
            try:
                cursor.execute('UPDATE users SET pet_has = \'{{{}}}\' WHERE id = {}'.format(','.join(adding), id))
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        def pet_active(id: int, adding:str) -> bool | Exception:
            try:
                cursor.execute(f"UPDATE users SET pet_active = '{adding}' WHERE id = {id}")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        def lvl(id: int, adding:int) -> bool | Exception:
            try:
                cursor.execute(f"UPDATE users SET lvl = '{adding}' WHERE id = {id}")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def exp(id: int, adding:str) -> bool | Exception:
            try:
                cursor.execute(f"UPDATE users SET exp = '{adding}' WHERE id = {id}")
                return True

            except (Exception, sql.Error) as _ex:
                return _ex
        
        def voicetime(id: int, value: timedelta) -> bool | Exception:
            try:
        
                cursor.execute('UPDATE users SET voicetime = voicetime + (%s) WHERE id = %s', (value, id))
                return True

            except (Exception) as _ex:
                return _ex
        
# ------------------------------------channels------------------------------------------------

        def channel_account_by_ownerid(ownerid: int, adding:int) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE channels SET account = account + {adding}')
                return True

            except (Exception, sql.Error) as _ex:
                return _ex

        
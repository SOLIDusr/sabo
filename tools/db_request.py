from tools.db_connect import cursor
import psycopg2 as sql
from datetime import datetime


class Request():
    
    def __init__(self) -> None:
        pass

    class Get():
        
        def __init__(self) -> None:
            pass
        
        def any(column:str, table:str, indeficator:str, value):
            try:
                cursor.execute(f'SELECT {column} FROM {table} WHERE {indeficator} = {value}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex

        def balance_by_id(id: int) -> int | Exception:
            try:
                cursor.execute(f'SELECT balance FROM users WHERE id = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def balance_by_nickname(name: str) -> int | Exception:
            try:
                cursor.execute(f'SELECT balance FROM users WHERE nickname = {name}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def name(id: int) -> str | Exception:
            try:
                cursor.execute(f'SELECT nickname FROM users WHERE id = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex

        def keys(id: int) -> int | Exception:
            try:
                cursor.execute(f'SELECT keys FROM users WHERE nickname = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def voicetime(id: int) -> datetime | Exception:
            try:
                cursor.execute(f'SELECT voicetime FROM users WHERE nickname = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def casepets(id: int) -> datetime | Exception:
            try:
                cursor.execute(f'SELECT casepets FROM users WHERE nickname = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pets(id: int) -> datetime | Exception:
            try:
                cursor.execute(f'SELECT pet_has FROM users WHERE nickname = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pet_active(id: int) -> datetime | Exception:
            try:
                cursor.execute(f'SELECT pet_has FROM users WHERE nickname = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex

        def channel_discord_by_owner(id: int) -> int | Exception:
            try:
                cursor.execute(f'SELECT discord_id FROM users WHERE ownerid = {id}')
                return cursor.fetchone()[0]
            except (Exception, sql.Error) as _ex:
                return _ex

    class Set():

        def __init__(self) -> None:
            pass

        def any(table, column, value, indeficator, var) -> bool | Exception:
            try:
                cursor.execute(f'UPDATE {table} SET {column} = {value} WHERE {indeficator} = {var}')
                return True
            except (Exception, sql.Error) as _ex:
                return _ex

        def balance_by_id(id, value) -> int | Exception:
            try:
                cursor.execute(f'UPDATE users SET money = {value} WHERE id = {id}')
                return True
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def balance_by_nickname(name, value) -> int | Exception:
            try:
                cursor.execute(f'UPDATE users SET money = {value} WHERE nickname = {name}')
                return True
            except (Exception, sql.Error) as _ex:
                return _ex

        def keys(id, value) -> int | Exception:
            try:
                cursor.execute(f'UPDATE users SET keys = {value} WHERE id = {id}')
                return True
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def voicetime(id, value) -> int | Exception:
            try:
                insert_query = """ INSERT INTO users (voicetime)
                                              VALUES (%s) WHERE id = {%s}"""
                item_tuple = (value, id)
                cursor.execute(insert_query, item_tuple)
                return True
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def casepets(id, value) -> int | Exception:
            try:
                cursor.execute(f'UPDATE users SET casepets = {value} WHERE id = {id}')
                return True
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pets(id, value) -> int | Exception:
            try:
                cursor.execute('UPDATE users SET pet_has = \'{{{}}}\' WHERE id = {}'.format(','.join(value), id))
                return True
            except (Exception, sql.Error) as _ex:
                return _ex
        
        def pet_active(id, value) -> int | Exception:
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
    
        def any(table, indeficator, value) -> bool | Exception:
            try: 
                cursor.execute(f'DELETE FROM {table} WHERE {indeficator} = {value}')
                return True
            except (Exception, sql.Error) as _ex:
                return _ex

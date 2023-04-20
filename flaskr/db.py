import pymysql
import logging


def query(conn, qry: str):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        logging.info(qry)
        cursor.execute(qry)
        rows = cursor.fetchall()
        return rows


def update(conn, table: str, columns: list, values: list, where_str: str):
    set_str = ', '.join([f'{c} = {v}' for c, v in zip(columns, values)])
    with conn.cursor() as cursor:
        qry = f'''
            UPDATE {table}
            SET {set_str}
            WHERE {where_str}
        '''
        logging.info(qry)
        cursor.execute(qry)
        conn.commit()
        return cursor.rowcount


def insert(conn, table: str, columns: list, values: list, ignore = False):
    with conn.cursor() as cursor:
        col_str = ', '.join(columns)
        val_str = ', '.join(values)
        ignore = 'IGNORE' if ignore else ''
        qry = f'''
            INSERT {ignore} INTO {table} ({col_str})
            VALUES ({val_str})
        '''
        logging.info(qry)
        cursor.execute(qry)
        conn.commit()
        return cursor.rowcount
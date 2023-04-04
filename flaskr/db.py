import pymysql

def query(conn, qry: str):
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        print(qry) 
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
        print(qry) 
        cursor.execute(qry)
        conn.commit()
        return cursor.rowcount

def insert(conn, table: str, columns: list, values: list):
    with conn.cursor() as cursor:
        col_str = ', '.join(columns)
        val_str = ', '.join(values)
        qry = f'''
            INSERT INTO {table} ({col_str})
            VALUES ({val_str})
        '''
        print(qry) 
        cursor.execute(qry)
        conn.commit()
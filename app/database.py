from typing import Any

from jinjasql import JinjaSql
from psycopg2 import pool, connect


class Database():
    """
    Простейшая обертка над psycopg2
    """
    host: str = None
    port: int = 5432
    dbname: str = 'postgres'
    user: str = 'postgres'
    password: str = 'postgres'

    pool: Any = None
    jsql: JinjaSql = JinjaSql(param_style='pyformat')

    def __init__(self, host: str, port: int = 5432, db_name: str = 'postgres',
                 user: str = 'postgres', password: str = 'postgres'):
        self.host = host
        self.port = port
        self.dbname = db_name
        self.user = user
        self.password = password
        self.conn = None
        self.pool = pool.ThreadedConnectionPool(2, 10, dbname=self.dbname, user=self.user,
                                                host=self.host, password=self.password, port=self.port)

    def get_connection(self) -> Any:
        if self.conn is None:
            try:
                self.conn = connect(dbname=self.dbname, user=self.user,
                                    host=self.host, password=self.password, port=self.port)
            except Exception as e: # TODO: переделать
                print(e)
        return self.conn

    def get_pool_connection(self) -> Any:
        """
        Возвращает новое соединение с БД, либо существующее, если открыто
        """
        if self.pool is None:
            try:
                self.pool = pool.ThreadedConnectionPool(2, 10, dbname=self.dbname, user=self.user,
                                                        host=self.host, password=self.password, port=self.port)
            except Exception as e: # TODO: переделать
                print(e)

        return self.pool.getconn()

    def fetch_scalar(self, sql_template: str, params: dict) -> Any:
        """
        По переданному шаблону и параметрам возвращает первую ячейку
        первой строки результата выполнения запроса. 
        В случае ошибки - текстовое представление в JSON
        """
        result = None
        conn = self.get_pool_connection()
        with conn.cursor() as cursor:
            query, bind_params = self.jsql.prepare_query(sql_template, params)
            try:
                cursor.execute(query % bind_params)
                result = cursor.fetchone()[0]
            finally:
                self.close(conn)
        
        return result

    def close(self, conn: Any) -> None:
        """
        Возвращает переданное соединение обратно в пул
        """
        if conn is not None and self.pool is not None:
            self.pool.putconn(conn)

    def closeall(self) -> None:
        """
        Закрывает все текущие соединения
        """
        if self.pool is not None:
            self.pool.closeall()

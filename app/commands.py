import sqlalchemy
import pandas as pd
import os


import raw_sql


PG_USERNAME = os.getenv("PG_USERNAME")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_DATABASE = os.getenv("PG_DATABASE")

engine = sqlalchemy.create_engine(
    f"postgresql://{PG_USERNAME}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
)


# Создание таблицы balance_d 
def create_balance():
    engine.execute(raw_sql.create_table_balance)


# Создание таблицы personal_account
def create_personal_account():
    engine.execute(raw_sql.create_table_personal_account)


# Заливка аккаунтов из файла .csv
#
# id,
# area,
# city,
# street,
# house,
# apartament,
# code_account,
# fio,
# contract_name,
# house_type,
# date_from,
# date_by,
# date_create,
# date_update,
# user_id,
# contract_id,
# rkc
def upload_personal_account(filename: str):
    try:
        personal_account = pd.read_csv(filename, sep=";", low_memory=False, dtype=str)
        personal_account.to_sql(
            "raw_personal_account", con=engine, chunksize=10000, index=False
        )
        # engine.execute('''ALTER TABLE account ADD PRIMARY KEY ("ID");''')
        engine.execute(raw_sql.upload_personal_account)
        engine.execute(raw_sql.drop_raw_personal_account)
        return f"OK : {filename} : {personal_account.count()}"

    except Exception as e:
        # Удаление временной таблицы raw_balance
        engine.execute(raw_sql.drop_raw_personal_account)
        return f"Error : {filename} : {e}"


# Загрузка из файлов, соответствующих структуре "большого .csv"
#
# id;
# account_id;
# balance_date;
# type_accrual;
# saldo_n;
# accrual;
# recalc;
# payment;
# saldo_k;
# date_create;
# date_update;
# user_id;
# code_account;
def upload_balance_from_large_csv(filename: str):
    try:
        balance = pd.read_csv(filename, sep=";", low_memory=False, dtype=str)
        balance.to_sql("raw_balance", engine, chunksize=10000, index=False)
        engine.execute(raw_sql.upload_balance_from_large_csv)
        engine.execute(raw_sql.drop_raw_balance)
        return f"OK : {filename} : {balance.count()}"
    except Exception as e:
        # Удаление временной таблицы raw_balance
        engine.execute(raw_sql.drop_raw_balance)
        return f"Error : {filename} : {e}"


# Загрузка из файлов, соответствующих структуре "малого .csv"
#
# account_id;
# balance_date;
# saldo_n;
# accrual;
# recalc;
# payment;
# saldo_k;
# code_account
def upload_balance_from_short_csv(filename: str):
    try:
        balance = pd.read_csv(filename, sep=";", low_memory=False, dtype=str)
        balance.to_sql("raw_balance", engine, chunksize=10000, index=False)
        engine.execute(raw_sql.upload_balance_from_short_csv)
        engine.execute(raw_sql.drop_raw_balance)
        return f"OK : {filename} : {balance.count()}"
    except Exception as e:
        # Удаление временной таблицы raw_balance
        engine.execute(raw_sql.drop_raw_balance)
        return f"Error : {filename} : {e}"

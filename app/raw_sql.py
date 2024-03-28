create_table_balance = """create table BALANCE
    (
        id           SERIAL PRIMARY KEY,
        account_id   INT,
        balance_date TIMESTAMP(6) WITH TIME ZONE default CURRENT_TIMESTAMP,
        type_accrual VARCHAR(1),
        saldo_n      DECIMAL(8,2),
        accrual      DECIMAL(8,2),
        recalc       DECIMAL(8,2),
        payment      DECIMAL(8,2),
        saldo_k      DECIMAL(8,2),
        date_create  TIMESTAMP(6) WITH TIME ZONE default CURRENT_TIMESTAMP,
        date_update  TIMESTAMP(6) WITH TIME ZONE default CURRENT_TIMESTAMP,
        user_id      SMALLINT,
        code_account VARCHAR(15)
    );

    create index IDX_CODE_ACCOUNT2 on BALANCE (ACCOUNT_ID, BALANCE_DATE);
    
    create index IDX_CODE_ACCOUNT2_DESC on BALANCE (ACCOUNT_ID ASC NULLS LAST, BALANCE_DATE DESC NULLS LAST);"""


create_table_personal_account = """create table PERSONAL_ACCOUNT
    (
        id            INT PRIMARY KEY,
        area          VARCHAR(50),
        city          VARCHAR(50),
        street        VARCHAR(100),
        house         VARCHAR(10),
        apartament    VARCHAR(30),
        code_account  VARCHAR(15),
        fio           VARCHAR(100),
        contract_name VARCHAR(20),
        house_type    VARCHAR(3),
        date_from     DATE,
        date_by       DATE,
        date_create   TIMESTAMP(6) WITH TIME ZONE default CURRENT_TIMESTAMP,
        date_update   TIMESTAMP(6) WITH TIME ZONE default CURRENT_TIMESTAMP,
        user_id       SMALLINT,
        contract_id   INT,
        rkc           SMALLINT
    );"""


# Загрузка из файлов, соответствующих структуре "большого .csv"
#
# id;
# account_id;
# balance_date;
# type_accrual;
# saldo_n;accrual;
# recalc;payment;
# saldo_k;
# date_create;
# date_update;
# user_id;
# code_account
upload_balance_from_large_csv = """INSERT INTO balance(
            account_id,
            balance_date,
            type_accrual,
            saldo_n,
            accrual,
            recalc,
            payment,
            saldo_k,
            date_create,
            date_update,
            user_id,
            code_account
        )
    SELECT  account_id::int,
            TO_TIMESTAMP(balance_date, 'YY-MM-DD HH24:MI:SSTZH')::timestamp with time zone,
            type_accrual,
            saldo_n::numeric,
            accrual::numeric,
            recalc::numeric,
            payment::numeric,
            saldo_k::numeric,
            TO_TIMESTAMP(date_create, 'DD.MM.YY HH24:MI:SSTZH')::timestamp with time zone,
            TO_TIMESTAMP(date_update, 'DD.MM.YY HH24:MI:SSTZH')::timestamp with time zone,
            user_id::smallint,
            code_account::text
    FROM raw_balance;"""


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
upload_balance_from_short_csv = """INSERT INTO balance(
            account_id,
            balance_date,
            saldo_n,
            accrual,
            recalc,
            payment,
            saldo_k,
            code_account
        )
    SELECT  account_id::int,
            TO_TIMESTAMP(balance_date, 'DD.MM.YY HH24:MI:SSTZH')::timestamp with time zone,
            saldo_n::numeric,
            accrual::numeric,
            recalc::numeric,
            payment::numeric,
            saldo_k::numeric,
            code_account::text
    FROM raw_balance;"""


upload_personal_account = """INSERT INTO personal_account(
            id,
            area,
            city,
            street,
            house,
            apartament,
            code_account,
            fio,
            contract_name,
            house_type,
            date_from,
            date_by,
            date_create,
            date_update,
            user_id,
            contract_id,
            rkc
        )
    SELECT id::int,
        area,
        city,
        street,
        house,
        apartament,
        code_account,
        fio,
        contract_name,
        house_type,
        TO_DATE(date_from::text, 'DD.MM.YY'), /* 01.07.2018 */
        TO_DATE(date_by::text, 'DD.MM.YY'), /* 01.07.2018 */
        TO_TIMESTAMP(date_create, 'DD-MON-YY HH12.MI.SS.US am')::timestamp with time zone, /* 16-DEC-21 08.43.40.000000 AM */
        TO_TIMESTAMP(date_update, 'DD-MON-YY HH12.MI.SS.US am')::timestamp with time zone, /* 16-DEC-21 08.43.40.000000 AM */
        user_id::smallint,
        contract_id::int,
        rkc::smallint
    FROM raw_personal_account;"""


drop_raw_balance = """DROP TABLE raw_balance"""


drop_raw_personal_account = """DROP TABLE raw_personal_account"""

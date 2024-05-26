{% extends "base_agg.sql" %}

{% block res %}
    SELECT
        to_char(pa.date_update AT TIME ZONE 'MST', 'YYYY-MM-DD"T"HH24:MI:SS"Z"') correct_date,
        pa.*,
        b.saldo_k,
        b.kol_month,
        b.payment,
        b.recalc,
        b.accrual,
        b.balance_date::DATE
    FROM
        personal_account pa
    CROSS JOIN LATERAL(
        SELECT
            b.saldo_k::REAL,
            CASE 
                WHEN 
                    b.accrual IS NOT NULL 
                THEN 
                    (b.saldo_n / nullif(b.accrual, 0))::int 
                ELSE 
                    0 
            END kol_month,
            b.payment::REAL,
            b.recalc::REAL,
            b.accrual::REAL,
            b.balance_date
        FROM
            balance_d b
        WHERE
            b.account_id = pa.id
        ORDER BY
            b.balance_date DESC NULLS LAST
        LIMIT
            1
    ) b
    WHERE
        pa.id > {{ offset }}
    ORDER
        BY pa.id
    LIMIT
        {{ limit }}
{% endblock %}

{% block agg_fields %}
'id', res.id,
'area', res.area,
'city', res.city,
'street', res.street,
'house', res.house,
'apartament', res.apartament,
'code_account', res.code_account,
'fio', res.fio,
'contract_name', res.contract_name,
'house_type', res.house_type,
'date_from', res.date_from,
'date_by', res.date_by,
'date_create', res.date_create,
'date_update', res.correct_date,
'user_id', res.user_id,
'contract_id', res.contract_id,
'rkc', res.rkc,
'saldo_k', res.saldo_k,
'kol_month', res.kol_month,
'payment', res.payment,
'recalc', res.recalc,
'accrual', res.accrual,
'balance_date', res.balance_date
{% endblock %}

{% block stats %}
SELECT max(id) max,
    (
    SELECT
        reltuples::BIGINT estimate
    FROM 
        pg_class
    WHERE 
        oid = 'public.personal_account'::REGCLASS
    ) count
FROM personal_account
LIMIT 1
{% endblock %}

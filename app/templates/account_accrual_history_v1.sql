{% extends "base_agg.sql" %}

{% block res %}
SELECT
    b.account_id id,
    b.code_account,
    b.balance_date::date,
    b.saldo_n,
    b.accrual,
    b.recalc,
    b.payment,
    b.saldo_k
FROM
    balance b
WHERE
    b.account_id = {{ p_account_id }}
ORDER BY
    b.balance_date
LIMIT
    {{ limit }}
OFFSET
    {{ offset }}
{% endblock %}

{% block agg_fields %}
'account_id', res.id,
'code_account', res.code_account,
'balance_date', res.balance_date,
'saldo_n', res.saldo_n,
'accrual', res.accrual,
'recalc', res.recalc,
'payment', res.payment,
'saldo_k', res.saldo_k 
{% endblock %}

{% block stats %}
SELECT 
    NULL::int max,
    count(1) count
FROM 
    balance b
WHERE
    b.account_id = {{ p_account_id }}

LIMIT 1
{% endblock %}

WITH res AS (
   {% block res %}{% endblock %}
),
res_json AS (
    SELECT coalesce(
            json_agg(
                json_build_object(
                    {% block agg_fields %}{% endblock %}
                )
            ),
            '[]'::json
        ) items,
        max(id) max,
        count(1) count
    FROM res
)
SELECT json_build_object(
        'items', rj.items,
        'hasMore', ({{ offset }} + rj.count < coalesce(stats.max, stats.count) AND rj.max <> coalesce(stats.max, rj.max)),
        'limit', {{ limit }},
        'offset', {{ offset }},
        'count', rj.count,
        'links', json_build_array(json_build_object(
            'rel', 'next', 'href',
            CASE
                WHEN 
                    {{ offset }} + rj.count < coalesce(stats.max, stats.count) AND rj.max <> coalesce(stats.max, rj.max)
                THEN
                    '{{ base_url }}'::text || '?limit=' || '{{ limit }}'::text || '&offset=' || rj.count + {{ offset }}::int
                ELSE
                    NULL
            END)),
        'allCount', stats.count,
        'maxId', stats.max
    )
FROM res_json rj
    CROSS JOIN (
        {% block stats %}{% endblock %}
    ) stats
LIMIT 1

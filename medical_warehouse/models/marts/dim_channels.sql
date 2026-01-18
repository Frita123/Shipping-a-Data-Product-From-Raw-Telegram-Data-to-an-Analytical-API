WITH base AS (
    SELECT
        channel_name,
        message_date,
        views
    FROM raw.telegram_messages
    WHERE channel_name IS NOT NULL
)

SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) AS channel_key,
    channel_name,
    'Medical' AS channel_type,
    MIN(message_date) AS first_post_date,
    MAX(message_date) AS last_post_date,
    COUNT(*) AS total_posts,
    AVG(views) AS avg_views
FROM base
GROUP BY channel_name

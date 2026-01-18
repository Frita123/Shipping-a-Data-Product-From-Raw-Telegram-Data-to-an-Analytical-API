WITH summary AS (
    SELECT
        CAST(message_id AS BIGINT) AS message_id,
        image_category
    FROM raw.yolo_detections
    WHERE detected_class = 'SUMMARY'
),

detections AS (
    SELECT
        CAST(message_id AS BIGINT) AS message_id,
        detected_class,
        confidence_score
    FROM raw.yolo_detections
    WHERE detected_class != 'SUMMARY'
)

SELECT
    d.message_id,
    m.channel_key,
    m.date_key,
    d.detected_class,
    d.confidence_score,
    s.image_category
FROM summary s
LEFT JOIN detections d
    ON s.message_id = d.message_id
LEFT JOIN {{ ref('fct_messages') }} m
    ON s.message_id = m.message_id

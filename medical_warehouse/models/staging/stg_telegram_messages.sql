with raw_messages as (
    select
        message_id,
        channel_name,
        message_date::timestamp as message_date,
        message_text,
        has_media,
        image_path,
        views::int as view_count,
        forwards::int as forward_count,
        length(message_text) as message_length,
        case when has_media then true else false end as has_image
    from raw.telegram_messages
    where message_id is not null
      and message_date is not null
)

select * from raw_messages

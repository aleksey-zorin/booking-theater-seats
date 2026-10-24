-- ============================================
-- Система бронирования мест в театре: запросы
-- ============================================

-- 1. Список всех спектаклей (LIST)
SELECT id, title, genre, duration_min
FROM plays
ORDER BY title;

-- 2. Список всех показов с названием спектакля (LIST + JOIN)
SELECT shows.id, shows.datetime, shows.hall, plays.title AS play_title
FROM shows
JOIN plays ON shows.play_id = plays.id
ORDER BY shows.datetime;

-- 3. Спектакли жанра «Драма» (WHERE)
SELECT id, title, duration_min
FROM plays
WHERE genre = 'Драма'
ORDER BY duration_min;

-- 4. Спектакли длиннее 150 минут (WHERE)
SELECT title, duration_min
FROM plays
WHERE duration_min > 150
ORDER BY duration_min DESC;

-- 5. Активные бронирования (WHERE по состоянию)
SELECT id, show_id, user_id, row, seat
FROM bookings
WHERE is_cancelled = 0
ORDER BY id;

-- 6. Полная информация о бронировании (JOIN трёх таблиц)
SELECT
    bookings.id,
    plays.title AS play_title,
    shows.datetime AS show_datetime,
    users.name AS user_name,
    bookings.row,
    bookings.seat,
    bookings.is_cancelled
FROM bookings
JOIN shows ON bookings.show_id = shows.id
JOIN plays ON shows.play_id = plays.id
JOIN users ON bookings.user_id = users.id
ORDER BY bookings.id;

-- 7. Свободные места на конкретном показе (параметризованный запрос для Django)
-- Значение ? подставляется из Python
SELECT row, seat FROM bookings
WHERE show_id = ? AND is_cancelled = 0;

-- 8. Количество спектаклей (COUNT)
SELECT COUNT(*) AS plays_count FROM plays;

-- 9. Количество активных бронирований (COUNT + WHERE)
SELECT COUNT(*) AS active_bookings
FROM bookings
WHERE is_cancelled = 0;

-- 10. Количество броней по каждому спектаклю (GROUP BY + JOIN)
SELECT
    plays.title AS play_title,
    COUNT(bookings.id) AS bookings_count
FROM plays
LEFT JOIN shows ON shows.play_id = plays.id
LEFT JOIN bookings ON bookings.show_id = shows.id
    AND bookings.is_cancelled = 0
GROUP BY plays.id, plays.title
ORDER BY bookings_count DESC;

-- 11. Спектакли с более чем одной бронью (HAVING)
SELECT
    plays.title AS play_title,
    COUNT(bookings.id) AS bookings_count
FROM plays
JOIN shows ON shows.play_id = plays.id
JOIN bookings ON bookings.show_id = shows.id
WHERE bookings.is_cancelled = 0
GROUP BY plays.id, plays.title
HAVING COUNT(bookings.id) > 1
ORDER BY bookings_count DESC;

-- 12. Спектакли, у которых нет ни одного показа (LEFT JOIN + IS NULL)
SELECT plays.title
FROM plays
LEFT JOIN shows ON shows.play_id = plays.id
WHERE shows.id IS NULL;

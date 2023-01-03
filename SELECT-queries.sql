SELECT name, edition_year FROM albums
WHERE edition_year = '2018-01-01';

SELECT name, duration FROM tracks
ORDER BY duration desc
LIMIT 1;

SELECT name, duration FROM tracks
WHERE duration >= 3.5 * 60;

SELECT name FROM collection
WHERE edition_year BETWEEN '2018-01-01' AND '2020-01-01';

SELECT name FROM authors
WHERE name NOT LIKE '% %';

SELECT name FROM tracks
WHERE name LIKE '%МОЙ%' OR name LIKE '%мой%' OR name LIKE '%my%' OR name LIKE '%MY%';
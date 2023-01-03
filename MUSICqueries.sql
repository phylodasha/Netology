-- количество исполнителей в каждом жанре;
SELECT genre_id, COUNT(*)
FROM authors_genres
GROUP BY genre_id;

-- количество треков, вошедших в альбомы 2019-2020 годов;

SELECT COUNT(*)
from (SELECT t.name
      FROM tracks t
               JOIN albums a on t.album_id = a.id
      WHERE a.edition_year BETWEEN '2019-01-01' AND '2020-12-31'
      GROUP BY t.name) AS subquery;

-- средняя продолжительность треков по каждому альбому;
SELECT a.name, AVG(t.duration)
FROM tracks t
         JOIN albums a on a.id = t.album_id
GROUP BY a.name;

-- все исполнители, которые не выпустили альбомы в 2020 году;

SELECT authors.name
FROM authors
         JOIN albums_authors aa on authors.id = aa.author_id
         JOIN albums a on a.id = aa.album_id
WHERE a.edition_year NOT BETWEEN '2020-01-01' AND '2020-12-31';

-- названия сборников, в которых присутствует конкретный исполнитель (Lady Gaga);
SELECT DISTINCT(collection.name)
from collection
         JOIN collection_tracks ct ON ct.collection_id = collection.id
         JOIN tracks t on ct.track_id = t.id
         JOIN albums a on t.album_id = a.id
         JOIN albums_authors aa on a.id = aa.album_id
         JOIN authors a2 on aa.author_id = a2.id
WHERE a2.name = 'Lady Gaga';

-- название альбомов, в которых присутствуют исполнители более 1 жанра;
SELECT *
FROM (SELECT COUNT(*), author_id
      FROM authors_genres
      GROUP BY author_id
      HAVING COUNT(*) > 1) as diff_g
         JOIN albums_authors aa on aa.author_id = diff_g.author_id
         JOIN albums a on aa.author_id = a.id;

-- наименование треков, которые не входят в сборники;
SELECT tracks.name
FROM tracks
         LEFT JOIN collection_tracks ct on tracks.id = ct.track_id
WHERE ct.track_id IS NULL;

-- исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
SELECT authors.name
FROM authors
         JOIN albums_authors aa on authors.id = aa.author_id
         JOIN tracks t on aa.album_id = t.album_id
WHERE t.duration = (SELECT MIN(duration) from tracks);

-- название альбомов, содержащих наименьшее количество треков.

SELECT albums.name as cnt FROM albums
JOIN tracks t on albums.id = t.album_id
GROUP BY albums.name
HAVING Count(*) = (SELECT min(cnt) FROM (SELECT albums.name, COUNT(*) AS cnt
                         FROM albums
                         JOIN tracks t ON albums.id = t.album_id
                         GROUP BY albums.name) AS foo);

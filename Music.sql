CREATE TABLE genres(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) 
);

CREATE TABLE authors(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60) 
);

CREATE TABLE authors_genres(
    author_id INTEGER REFERENCES Authors(id),
    genre_id INTEGER REFERENCES Genres(id),
    CONSTRAINT pk_authors_genres PRIMARY KEY (author_id, genre_id)

);

CREATE TABLE albums(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60),
    edition_year DATE
);

CREATE TABLE albums_authors(
    author_id INTEGER REFERENCES Authors(id),
    album_id INTEGER REFERENCES Albums(id),
    CONSTRAINT pk_albums_authors PRIMARY KEY (author_id, album_id)
);

CREATE TABLE tracks(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60),
    duration INTEGER,
    album_id SERIAL REFERENCES Albums(id)
);

CREATE TABLE collection(
    id SERIAL PRIMARY KEY,
    name VARCHAR(60),
    edition_year DATE
);

CREATE TABLE collection_tracks(
    collection_id INTEGER REFERENCES collection(id),
    track_id INTEGER REFERENCES tracks(id),
    CONSTRAINT pk_collection_tracks PRIMARY KEY (collection_id, track_id)

);
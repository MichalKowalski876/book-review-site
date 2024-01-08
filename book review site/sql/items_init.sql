CREATE TABLE "items" (
    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
    "name"	TEXT NOT NULL,
    "author"	TEXT,
    "year_published"	INTEGER,
    "score"   FLOAT,
    "status" INTEGER,
    "cover_url" TEXT
);

INSERT INTO "items"
VALUES
    (NULL, 'No Longer Human', 'Osamu Dazai', 1948, 0, 0,'https://cdn.kobo.com/book-images/6963d990-cef3-4c05-8709-a6e79c4a0967/1200/1200/False/no-longer-human.jpg'),
    (NULL, 'Horus rising', 'Dan Abnett', 2006, 0, 0, 'https://m.media-amazon.com/images/I/81XH8U96LIL._AC_UF894,1000_QL80_.jpg'),
    (NULL, 'The Infinite and the Divine', 'Robert Rath', 2020, 0, 1, 'https://m.media-amazon.com/images/I/71Pg78scUML._AC_UF894,1000_QL80_.jpg'),
    (NULL, 'Beast in the Shadows', 'Edogawa Ranpo', 1928, 0, 2, 'https://ecsmedia.pl/c/beast-in-the-shadows-b-iext139488479.jpg'),
    (NULL, 'Pride and prejudice', 'Jane Austen', 1813 , 0, 0, 'https://m.media-amazon.com/images/I/61nqj+gg4fL._AC_UF894,1000_QL80_.jpg')
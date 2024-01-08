CREATE TABLE "reviews"
(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "item_id" INTEGER,
    "user_id" INTEGER,
    "score" INTEGER,
    FOREIGN KEY ("item_id") REFERENCES "items" ('id'),
    FOREIGN KEY ("user_id") REFERENCES "users" ('id')

);
INSERT INTO "reviews"
VALUES (NULL,2,2,5)
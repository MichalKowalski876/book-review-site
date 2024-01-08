CREATE TABLE "reports"
(
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "item_id" INTEGER,
    "desc" TEXT,
    FOREIGN KEY ("item_id") REFERENCES "items" ("id")
);
INSERT INTO "reports"
VALUES (NULL, 4, "wrong author");
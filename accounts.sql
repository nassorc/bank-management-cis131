DROP TABLE IF EXISTS accounts;

CREATE TABLE accounts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password CHAR(3),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    balance INT DEFAULT 0
);

INSERT INTO accounts (email, password, first_name, last_name, balance)
VALUES
    ('mat@gmail.com', '123', 'Matthew', 'Crossan', 17),
    ('tam@gmail.com', '123', 'Tam', 'Nassorc', 10);
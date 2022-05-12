DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS transfers;

create TABLE transactions (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    dt datetime DEFAULT (datetime(current_timestamp)),
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
);
create TABLE transfers (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    from_account INTEGER NOT NULL,
    to_account INTEGER NOT NULL,
    dt datetime default (datetime(current_timestamp)),
    FOREIGN KEY (from_account) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (to_account) REFERENCES accounts(id) ON DELETE CASCADE
);
CREATE TABLE accounts (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password CHAR(60),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    balance INT DEFAULT 0
);

INSERT INTO accounts (id, email, password, first_name, last_name, balance)
VALUES
    ('1000','mat@gmail.com', '123', 'Matthew', 'Crossan', 17);



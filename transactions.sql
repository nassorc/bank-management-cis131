INSERT INTO transactions (account_id, amount)
VALUES 
    (1000, 10);
-- ALTER TABLE transfers ADD COLUMN ammount REAL NOT NULL;
ALTER TABLE transfers RENAME COLUMN ammount TO amount;
INSERT INTO transfers (from_account, to_account, amount)
VALUES 
    (1001, 1000, 5);
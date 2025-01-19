CREATE TABLE IF NOT EXISTS log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    datetime VARCHAR(255),
    host VARCHAR(255),
    program VARCHAR(255),
    message TEXT,
    log_group INT,
    label INT
);


ALTER TABLE log
ADD COLUMN IF NOT EXISTS log_group INT;

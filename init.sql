CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price INTEGER
);

INSERT INTO products (title, price) VALUES
('computer', 15000),
('table', 2000),
('chair', 1000),
('pot', 300),
('curtains', 800),
('piano', 10000),
('tv', 6000),
('book', 100),
('lamp', 300);

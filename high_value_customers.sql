CREATE TABLE customers_test (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50),
  email VARCHAR(100)
);

CREATE TABLE orders_test (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  amount DECIMAL(8, 2),
  FOREIGN KEY (customer_id) REFERENCES customers_test(customer_id)
);

INSERT INTO customers_test (name, email) VALUES
('Alice Smith', 'alice@example.com'),
('Bob Johnson', 'bob@example.com');

INSERT INTO orders_test (customer_id, amount) VALUES
(1, 300.00),
(1, 250.00),
(2, 150.00);

CREATE VIEW high_value_customers AS
SELECT 
  c.customer_id,
  c.name,
  SUM(o.amount) AS total_order_amount
FROM 
  customers_test c
JOIN 
  orders_test o ON c.customer_id = o.customer_id
GROUP BY 
  c.customer_id, c.name
HAVING 
  total_order_amount > 500;

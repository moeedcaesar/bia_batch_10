# Question 5.1 (8 points)
# Write a MySQL query to create two tables:
# customers with columns: customer_id (int, primary key, auto-increment), name (varchar, 50), email (varchar, 100)
# orders with columns: order_id (int, primary key, auto-increment), customer_id (int, foreign key referencing customers ), amount (decimal, 8,2)
# Insert 2 customers and 3 orders (at least one customer with multiple orders).
create table customers (
customer_id int auto_increment primary key,
name varchar(50),
email varchar(100)
);

CREATE TABLE orders (
order_id INT AUTO_INCREMENT PRIMARY KEY,
customer_id INT,
amount DECIMAL(8, 2),
FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

INSERT INTO customers (name, email) VALUES
('Alice', 'alice@gmail.com'),
('Bob', 'bob@gmail.com');

INSERT INTO orders (customer_id, amount) VALUES
(1, 150.00),
(2, 100.90),
(1, 199.99);

# Question 5.2 (7 points)
# Assume tables products (columns: product_id , name , price ) and order_details (columns: order_id , product_id , quantity ). Write a MySQL query to:
# Join the tables to calculate the total cost ( price * quantity ) per order.
# Group by order_id and sum the total cost.
# Filter for orders with total cost greater than 200.
# Order by total cost in descending order.

CREATE TABLE products (
product_id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50),
price DECIMAL(8, 2)
);

CREATE TABLE order_details(
order_id INT AUTO_INCREMENT PRIMARY KEY,
product_id INT,
quantity INT,
FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO products (product_id, name, price) VALUES
(1, 'Laptop', 99.99),
(2, 'Smart Phone', 57.50),
(3, 'Table', 15.00),
(4, 'Makeup kit', 12.10),
(5, 'Laptop', 79.80),
(6, 'Smart Phone', 120.40),
(7, 'Makeup kit', 29.99);

INSERT INTO order_details (order_id, product_id, quantity) VALUES
(1, 7, 3),
(2, 5, 1),
(3, 2, 2),
(4, 6, 5),
(5, 3, 8),
(6, 4, 12),
(7, 1, 3),
(8, 4, 1),
(9, 7, 3),
(10, 3, 8);

# Join the tables to calculate the total cost ( price * quantity ) per order.
SELECT od.order_id, SUM(p.price * od.quantity) as total_cost
FROM bia_batch4.order_details od
JOIN products p on od.product_id = p.product_id
GROUP BY
od.order_id
HAVING
total_cost > 200
ORDER BY
total_cost desc;

# Question 5.3 (5 points)
# Write a MySQL query to create a view called high_value_customers based on the customers and orders tables (from Question 5.1).
# The view should show:
# customer_id , name , and total order amount for customers whose total orders exceed 500.

CREATE VIEW high_value_products AS
SELECT 
  o.order_id,
  p.name,
  sum(p.price * o.quantity) as total_purchase
  FROM bia_batch4.order_details o
  join bia_batch4.products p on o.product_id = p.product_id
  GROUP BY o.product_id
  HAVING total_purchase > 500;

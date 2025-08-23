create table shop_db (
id int primary key,
name varchar(50),
email varchar(50),
city varchar(50)
);

insert into shop_db (id, name, email, city) values
(1, 'Ali', 'ali@gmail.com', 'Karachi'),
(2, 'Fatima', 'fatima@yahoo.com', 'Lahore'),
(3, 'Ahmed', 'ahmed@outlook.com', 'Karachi'),
(4, 'Sana', 'sana@gmail.com', 'Islamabad');

create table orders (
id int,
customer_id int,
order_date date,
amount int
);

insert into orders (id, customer_id, order_date, amount) values
(1, 1, '2024-10-01', 5000),
(2, 2, '2024-10-03', 3000),
(3, 1, '2024-10-07', 7000),
(4, 3, '2024-10-10', 2000),
(5, 2, '2024-10-11', 1000),
(6, 4, '2024-10-12', 8000);

# 3. Write a query to fetch names and emails of customers from Karachi.
select name, email from bia_batch4.shop_db
where city = 'Karachi';

# 4. List all orders placed after 2024-10-05.
select * from bia_batch4.orders
where order_date > '2024-10-05';

# 5. Show the order details for customers who live in Lahore.
select * from bia_batch4.orders
join shop_db on orders.customer_id = shop_db.id
where shop_db.city = 'Lahore';

# 6. Show all orders where the amount is between 2000 and 7000.
select * from bia_batch4.orders
where amount between 2000 and 7000;

# 7. Find the total amount spent by each customer.
select shop_db.name, sum(orders.amount) as total_spent from bia_batch4.shop_db
join bia_batch4.orders on shop_db.id = orders.customer_id
group by shop_db.name;

# 8. Count how many orders each customer has placed.
select shop_db.name, count(orders.id) as order_count from bia_batch4.shop_db
join bia_batch4.orders on shop_db.id = orders.customer_id
group by shop_db.name;

# 9. Drop duplicate orders table
drop table bia_batch4.orders_new_dup;

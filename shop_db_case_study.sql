create schema shop_db;
create table shop_db.customers(
id int primary key,
name varchar(50),
email varchar(50),
city varchar(50)
);
insert into shop_db.customers (id, name, email, city)
values (1, 'Ali', 'ali@gmail.com', 'Karachi'),
(2, 'Fatima', 'fatima@yahoo.com', 'Lahore'),
(3, 'Ahmed', 'ahmed@outlook.com', 'Karachi'),
(4, 'Sana', 'sana@gmail.com', 'Islamabad');

create table shop_db.orders as select * from bia_batch4.orders;

# 3. Write a query to fetch names and emails of customers from Karachi.
select name from shop_db.customers
where city = 'Karachi';

# 4. List all orders placed after 2024-10-05.
select * from shop_db.orders
where order_date > '2024-10-05';

# 5. Show the order details for customers who live in Lahore.
select o.id, o.customer_id, o.order_date, o.amount from shop_db.orders o
join shop_db.customers c on o.customer_id = c.id
where c.city = 'Lahore';

# 6. Show all orders where the amount is between 2000 and 7000.
select * from shop_db.orders
where amount between 2000 and 7000;

# 7. Find the total amount spent by each customer.
select c.name, sum(o.amount) total_amount_spent from shop_db.orders o
join shop_db.customers c on c.id = o.customer_id
group by c.name
order by total_amount_spent desc;

# 8. Count how many orders each customer has placed.
select c.name, count(o.id) total_orders from shop_db.customers c
join shop_db.orders o on c.id = o.customer_id
group by c.name
order by total_orders desc;

# 9. Show the average order amount per city (based on customer city).
select c.city, sum(o.amount) amount_per_city from shop_db.customers c
join shop_db.orders o on c.id = o.customer_id
group by c.city
order by amount_per_city desc;

# 10. Find the customer(s) who placed more than one order.
select c.name, count(o.id) total_orders from shop_db.customers c
join shop_db.orders o on c.id = o.customer_id
group by c.name
order by total_orders desc;

# 11. Show names and cities of customers who spent more than 5000 in total.
select c.name, c.city, sum(o.amount) total_spent from shop_db.customers c
join shop_db.orders o on c.id = o.customer_id
group by c.name, c.city, o.customer_id
having total_spent > 5000;

# 12. List customers who have not placed any orders.
select c.name from shop_db.customers c
left join shop_db.orders o on c.id = o.customer_id
where o.id = null;

# 13. Show the customer name and amount of their most recent order.
select c.name, o.amount from shop_db.customers c
join shop_db.orders o on c.id = o.customer_id
where o.order_date = (
select max(o.order_date) from shop_db.orders o
where c.id = o.customer_id);

# 14. Find the name of the customer who placed the highest single order.
select c.name, o.amount amount from shop_db.customers c
join shop_db.orders o on c.id = o.customer_id
where amount = (
select max(amount) from shop_db.orders
);

# 15. Write a query to calculate total sales made on each day.
select o.order_date, sum(o.amount) as total_sales from shop_db.orders o
group by order_date
order by order_date;

# 16. List all customers who placed an order within the last 5 days from 2024-10-15.
select c.name, o.order_date from shop_db.customers c 
join shop_db.orders o on c.id = o.customer_id
where o.order_date between '2024-10-10' and '2024-10-15';

# 17. Write a query to update Ahmed’s email to ahmed123@gmail.com.
update shop_db.customers
set email = 'ahmed123@gmail.com'
where id = '3';

# 18. Delete all orders placed before 2024-10-05.
SET SQL_SAFE_UPDATES = 0;
delete from shop_db.orders
where order_date < '2024-10-05';

# 19. Insert a new customer named "Zara" from "Multan" with email zara@gmail.com.
INSERT INTO shop_db.customers (id, name, email, city)
VALUES (5, 'Zara', 'zara@gmail.com', 'Multan');
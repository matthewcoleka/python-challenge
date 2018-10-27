use sakila;
-- 1a. Display the first and last names of all actors from the table actor.
select first_name, last_name
from actor;
-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
select upper(concat(first_name,' ',last_name)) as 'Actor Name'
from actor;
-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
select actor_id, first_name, last_name
from actor
where first_name = 'Joe';
-- 2b. Find all actors whose last name contain the letters GEN: 
select actor_id, first_name, last_name
from actor
where last_name like '%GEN%';
-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
select first_name, last_name
from actor
where last_name like '%LI%'
order by last_name, first_name;
-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
select country_id, country
from country
where country in ('Afghanistan','Bangladesh','China');
-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, so create a column in the table actor named description and use the data type BLOB (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).
alter table actor
add column description blob;
-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
alter table actor
drop column description;
-- 4a. List the last names of actors, as well as how many actors have that last name.
select last_name, count(last_name) as LastNameCount
from actor
group by last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
select distinct last_name, count(last_name) as LastNameCount
from actor
group by last_name
having count(last_name) > 1;
-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record. 
Update actor
set first_name = 'HARPO'
where first_name = 'GROUCHO' and last_name = 'WILLIAMS';
-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.
Update actor
set first_name = 'GROUCHO'
where first_name = 'HARPO';
-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
-- Hint: https://dev.mysql.com/doc/refman/5.7/en/show-create-table.html 
SHOW CREATE TABLE address;
-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address
select s.first_name, s.last_name, a.address
from staff as s
join address as a on a.address_id = s.address_id;
-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.

select s.first_name, s.last_name, sum(p.amount) as August_2015_Transactions
from payment as p
join staff as s on s.staff_id = p.staff_id
where cast(p.payment_date as Date) >= '2005-08-01' and cast(p.payment_date as Date) < '2005-09-01' 
group by s.staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join. 
select f.title, count(a.actor_id) as Actor_Count
from film_actor as a
inner join film as f on f.film_id = a.film_id
group by f.title;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system? Answer = 6
select f.title, count(i.inventory_id) as Hunchback_Impossible_Copies
from inventory as i
inner join film as f on f.film_id = i.film_id
where f.title = 'HUNCHBACK IMPOSSIBLE';
-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:  ![Total amount paid](Images/total_payment.png) 
select c.first_name, c.last_name, sum(p.amount) as Total_Paid
from payment as p
inner join customer as c on c.customer_id = p.customer_id
group by c.customer_id
order by c.last_name, c.first_name;
-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the 
-- letters K and Q have also soared in popularity. Use subqueries to display the titles of movies 
-- starting with the letters K and Q whose language is English.

select title
from film
where language_id in
(
	SELECT language_id
    FROM language
    where name = 'English')
AND title like "K%" or title like "Q%";
 
-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
select first_name, last_name
from actor
where actor_id in
(
	SELECT actor_id
    From film_actor
    where film_id in
	(
		SELECT film_id
        FROM film
        where title = 'ALONE TRIP'
        )
	);
-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers.
--  Use joins to retrieve this information.
select cust.first_name, cust.last_name, cust.email
from customer as cust
INNER JOIN address as a ON
	a.address_id = cust.address_id
INNER JOIN city as c ON
	c.city_id = a.city_id
INNER JOIN country ON
	country.country_id = c.country_id
WHERE country.country = 'CANADA';

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
select f.title, cat.name as category
from film as f
JOIN film_category as filmcat on
	filmcat.film_id = f.film_id
JOIN category as cat on
	cat.category_id = filmcat.category_id
WHERE cat.name = 'Family';
-- 7e. Display the most frequently rented movies in descending order.
select f.title, count(rent.rental_id) as Times_Rented
from film as f
JOIN inventory as i on
	i.film_id = f.film_id
JOIN rental as rent on
	rent.inventory_id = i.inventory_id
GROUP by f.title
Order by count(rent.rental_id) DESC;
-- 7f. Write a query to display how much business, in dollars, each store brought in.
Select a.address, sum(p.amount) as Store_GrossRevenue
FROM address as a
JOIN store as s ON
	s.address_id = a.address_id
JOIN staff on
	staff.store_id = s.store_id
JOIN payment as p on
	p.staff_id = staff.staff_id
group by a.address
Order by sum(p.amount) DESC;
-- 7g. Write a query to display for each store its store ID, city, and country.
select s.store_id, c.city, country.country
from store as s
join address as a on
	a.address_id = s.address_id
join city as c on
	c.city_id = a.city_id
join country on
	country.country_id = c.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
Select cat.name, sum(p.amount) as Gross_Revenue
from film_category as filmcat
join inventory as i on
	filmcat.film_id = i.film_id
join rental as rent on
	i.inventory_id = rent.inventory_id
join payment as p on
	p.rental_id = rent.rental_id
join category as cat on
	filmcat.category_id = cat.category_id
group by cat.name
order by sum(p.amount) DESC
limit 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
-- Use the solution from the problem above to create a view. 
-- If you haven't solved 7h, you can substitute another query to create a view.
create view Top_5_Genres_GrossRev as
Select cat.name, sum(p.amount) as Gross_Revenue
from film_category as filmcat
join inventory as i on
	filmcat.film_id = i.film_id
join rental as rent on
	i.inventory_id = rent.inventory_id
join payment as p on
	p.rental_id = rent.rental_id
join category as cat on
	filmcat.category_id = cat.category_id
group by cat.name
order by sum(p.amount) DESC
limit 5;
-- 8b. How would you display the view that you created in 8a?
SELECT * from top_5_genres_grossrev;
-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
drop view top_5_genres_grossrev;


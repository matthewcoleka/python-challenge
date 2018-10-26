use sakila;
-- Question 1a
select first_name, last_name
from actor;
-- Question 1b
select upper(concat(first_name,' ',last_name)) as 'Actor Name'
from actor;
-- Question 2a
select actor_id, first_name, last_name
from actor
where first_name = 'Joe';
-- Question 2b
select actor_id, first_name, last_name
from actor
where last_name like '%GEN%';


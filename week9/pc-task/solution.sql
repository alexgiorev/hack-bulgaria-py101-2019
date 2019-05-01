-- Напишете заявка, която извежда средната скорост на компютрите
-- first solution
select cast(laptop_sum + pc_sum as float) / (laptop_count + pc_count) as average_speed
from (select sum(speed) as laptop_sum, count(*) as laptop_count from laptop)
     join (select sum(speed) as pc_sum, count(*) as pc_count from pc);

-- Напишете заявка, която извежда средната скорост на компютрите
-- second solution
select avg(speed) as [average speed] from (select speed from laptop union all select speed from pc);

-- Напишете заявка, която извежда средния размер на екраните на лаптопите за всеки производител.
select maker, avg(screen) as [screen size] from product natural join laptop group by maker;

-- Напишете заявка, която извежда средната скорост на лаптопите с цена над 1000.
select avg(speed) as average_speed
from laptop where price > 1000;

-- Напишете заявка, която извежда средната цена на компютрите според различните им hd
select hd, avg(price) as `average price` from pc group by hd;

-- Напишете заявка, която извежда средната цена на компютрите за всяка скорост по-голяма от 500.
-- solution1, using a WHERE clause
select speed, avg(price) as [average price]
from (select speed, price from laptop union all select speed, price from pc)
where speed > 500 group by speed;

-- Напишете заявка, която извежда средната цена на компютрите за всяка скорост по-голяма от 500.
-- solution2, using a HAVING clause
select speed, avg(price) as [average price]
from (select speed, price from laptop union all select speed, price from pc)
group by speed having speed > 500;

-- Напишете заявка, която извежда средната цена на компютрите произведени от производител ‘A’.
select avg(price) as [average price]
from  (select model from product where maker = 'A')
      natural join (select model, price from laptop union all select model, price from pc);

-- Напишете заявка, която извежда производителите, които са произвели поне по 3 различни модела компютъра.
-- solution1, using a where clause
select maker, total from (select maker, count(*) as total
       	       	    	  from product where [type] in ('PC', 'Laptop') group by maker)
where total >= 3;

-- Напишете заявка, която извежда производителите, които са произвели поне по 3 различни модела компютъра.
-- solution2, using a group by clause
select maker, total from (select maker, count(*) as total
       	      	    	  from product where [type] in ('PC', 'Laptop')
			  group by maker having count(*) >= 3);


-- Напишете заявка, която извежда производителите на компютрите с най-висока цена.
-- this can be done in a single query, but i am not sure how readable it would be.
create temp table computers as
    select model, speed, ram, hd, price from laptop
    union all
    select model, speed, ram, hd, price from pc;

create temp table max_price as select max(price) as price from computers;

create temp table most_expensive_models as
select model from computers natural join max_price;

select maker from product natural join most_expensive_models;

-- Напишете заявка, която извежда средния размер на диска на тези компютри
-- произведени от производители, които произвеждат и принтери.
create temp table printer_makers as
select distinct maker from product where type = 'Printer';

select maker, avg(cast(cd as int)) as [avg cd]
from (select * from (select * from product natural join printer_makers where type = 'PC')
     	       	     natural join pc)
group by maker;

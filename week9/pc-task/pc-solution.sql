-- Напишете заявка, която извежда средната скорост на компютрите
-- first solution
create temp table result1_1 as
select cast(laptop_sum + pc_sum as float) / (laptop_count + pc_count) as average_speed
from (select sum(speed) as laptop_sum, count(*) as laptop_count from laptop)
     join (select sum(speed) as pc_sum, count(*) as pc_count from pc);

-- Напишете заявка, която извежда средната скорост на компютрите
-- second solution
create temp table result1_2 as
select avg(speed) as [average speed] from (select speed from laptop union all select speed from pc);

-- Напишете заявка, която извежда средния размер на екраните на лаптопите за всеки производител.
create temp table result2 as
select maker, avg(screen) as [screen size] from product natural join laptop group by maker;

-- Напишете заявка, която извежда средната скорост на лаптопите с цена над 1000.
create temp table result3 as
select avg(speed) as average_speed
from laptop where price > 1000;

-- Напишете заявка, която извежда средната цена на компютрите според различните им hd
create temp table result4 as
select hd, avg(price) as `average price` from pc group by hd;

-- Напишете заявка, която извежда средната цена на компютрите за всяка скорост по-голяма от 500.
-- solution1, using a WHERE clause
create temp table result5_1 as
select speed, avg(price) as [average price]
from (select speed, price from laptop union all select speed, price from pc)
where speed > 500 group by speed;

-- Напишете заявка, която извежда средната цена на компютрите за всяка скорост по-голяма от 500.
-- solution2, using a HAVING clause
create temp table result5_2 as
select speed, avg(price) as [average price]
from (select speed, price from laptop union all select speed, price from pc)
group by speed having speed > 500;

-- Напишете заявка, която извежда средната цена на компютрите произведени от производител ‘A’.
create temp table result6 as
select avg(price) as [average price]
from  (select model from product where maker = 'A')
      natural join (select model, price from laptop union all select model, price from pc);

-- Напишете заявка, която извежда производителите, които са произвели поне по 3 различни модела компютъра.
-- solution1, using a where clause
create temp table result7_1 as
select maker, total from (select maker, count(*) as total
       	       	    	  from product where [type] in ('PC', 'Laptop') group by maker)
where total >= 3;

-- Напишете заявка, която извежда производителите, които са произвели поне по 3 различни модела компютъра.
-- solution2, using a group by clause
create temp table result7_2 as
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

create temp table result8 as
select maker from product natural join most_expensive_models;

-- Напишете заявка, която извежда средния размер на диска на тези компютри
-- произведени от производители, които произвеждат и принтери.
create temp table printer_makers as
select distinct maker from product where type = 'Printer';

create temp table result9 as
select maker, avg(cast(cd as int)) as [avg cd]
from (select * from (select * from product natural join printer_makers where type = 'PC')
     	       	     natural join pc)
group by maker;

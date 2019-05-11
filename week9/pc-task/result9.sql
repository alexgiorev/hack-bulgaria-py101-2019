-- Напишете заявка, която извежда средния размер на диска на тези компютри
-- произведени от производители, които произвеждат и принтери.
create temp table printer_makers as
select distinct maker from product where type = 'Printer';

select maker, avg(cast(cd as int)) as [avg cd]
from (select * from (select * from product natural join printer_makers where type = 'PC')
     	       	     natural join pc)
group by maker;

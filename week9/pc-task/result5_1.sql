-- Напишете заявка, която извежда средната цена на компютрите за всяка скорост по-голяма от 500.
select speed, avg(price) as [average price]
from (select speed, price from laptop union all select speed, price from pc)
where speed > 500 group by speed;


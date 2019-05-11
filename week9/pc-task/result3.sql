-- Напишете заявка, която извежда средната скорост на лаптопите с цена над 1000.
select avg(speed) as average_speed
from laptop where price > 1000;

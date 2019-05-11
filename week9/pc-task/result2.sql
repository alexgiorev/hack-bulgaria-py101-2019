-- Напишете заявка, която извежда средния размер на екраните на лаптопите за всеки производител.
select maker, avg(screen) as [screen size] from product natural join laptop group by maker;

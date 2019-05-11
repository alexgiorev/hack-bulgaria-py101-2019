-- Напишете заявка, която извежда средната скорост на компютрите
select avg(speed) as [average speed] from (select speed from laptop union all select speed from pc);

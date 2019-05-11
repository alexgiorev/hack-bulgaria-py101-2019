-- Напишете заявка, която извежда средната цена на компютрите според различните им hd
select hd, avg(price) as `average price` from pc group by hd;

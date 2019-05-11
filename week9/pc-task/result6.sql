-- Напишете заявка, която извежда средната цена на компютрите произведени от производител ‘A’.
select avg(price) as [average price]
from  (select model from product where maker = 'A')
      natural join (select model, price from laptop union all select model, price from pc);

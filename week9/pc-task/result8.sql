-- Напишете заявка, която извежда производителите на компютрите с най-висока цена.
create temp table computers as
    select model, speed, ram, hd, price from laptop
    union all
    select model, speed, ram, hd, price from pc;

create temp table max_price as select max(price) as price from computers;

create temp table most_expensive_models as
select model from computers natural join max_price;

select maker from product natural join most_expensive_models;

-- За всяка страна изведете имената на корабите,
-- които никога не са участвали в битка.
select country, ships.name as ship from classes join ships using (class);

create temp table ships_in_battle as select distinct ship from outcomes;

select * from country_ship where (ship) not in ships_in_battle;

-- Напишете заявка, която за всеки кораб извежда името му,
-- държавата, броя оръдия и годината на пускане (launched).

create temp table result1 as
select name, country, numguns, launched
from classes join ships using (class);

-- Повторете горната заявка като този път включите в резултата
-- и класовете, които нямат кораби, но съществуват кораби със
-- същото име като тяхното.

create temp table result2 as
select name, country, numguns, launched
from classes join ships on classes.class = ships.name
union select * from result1;

-- Напишете заявка, която извежда имената на корабите,
-- участвали в битка от 1942г.

create temp table result3 as
select ship from outcomes join
       	    	 (select name from battles where date like '1942-%') as battles1942
		 on outcomes.battle = battles1942.name;

-- За всяка страна изведете имената на корабите,
-- които никога не са участвали в битка.

create temp table country_ship as
select country, ships.name as ship from classes join ships using (class);

create temp table ships_in_battle as select distinct ship from outcomes;

create temp table result4 as
select * from country_ship where (ship) not in ships_in_battle;


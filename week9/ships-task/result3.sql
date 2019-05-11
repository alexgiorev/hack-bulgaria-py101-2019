-- Напишете заявка, която извежда имената на корабите,
-- участвали в битка от 1942г.
select ship from outcomes join
       	    	 (select name from battles where date like '1942-%') as battles1942
		 on outcomes.battle = battles1942.name;

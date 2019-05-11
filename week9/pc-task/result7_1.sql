-- Напишете заявка, която извежда производителите, които са произвели поне по 3 различни модела компютъра.
select maker, total from (select maker, count(*) as total
       	       	    	  from product where [type] in ('PC', 'Laptop') group by maker)
where total >= 3;

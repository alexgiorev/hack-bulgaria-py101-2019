-- Напишете заявка, която за всеки кораб извежда името му,
-- държавата, броя оръдия и годината на пускане (launched).

-- Повторете горната заявка като този път включите в резултата
-- и класовете, които нямат кораби, но съществуват кораби със
-- същото име като тяхното.
select name, country, numguns, launched
from classes join ships on classes.class = ships.name
union select * from result1;

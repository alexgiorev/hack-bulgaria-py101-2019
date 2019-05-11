-- Напишете заявка, която за всеки кораб извежда името му,
-- държавата, броя оръдия и годината на пускане (launched).
select name, country, numguns, launched
from classes join ships using (class);

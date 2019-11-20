-- SQLite
SELECT COALESCE(soc2, 'unknown') as soc2, COUNT() as count
FROM `listings`
GROUP BY soc2;
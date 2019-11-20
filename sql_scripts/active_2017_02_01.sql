-- SQLite
SELECT COUNT() as 'active on Feb 1 2017' 
FROM `listings`
WHERE '2017-02-01' BETWEEN posted AND expired
ORDER BY posted;
SELECT b.id,count(b.id)as num from
(SELECT * FROM nodes_tags  UNION ALL SELECT * FROM ways_tags )b
WHERE b.id in(SELECT a.id
FROM (SELECT * FROM nodes_tags  UNION ALL SELECT * FROM ways_tags )a
WHERE a.key ='shop')
GROUP by b.id
ORDER by num desc
;


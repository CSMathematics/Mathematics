SELECT Content,count(Subject_Number) FROM Contents_per_Subject 
--WHERE Subject_Number = 'Θεμα Β'
GROUP BY Content
ORDER BY 2 DESC
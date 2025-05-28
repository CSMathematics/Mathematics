SELECT Content AS 'Ζητούμενο',group_concat(concat(Year,' - ',Subject_Number),',') AS 'Επαναληψεις' ,count(Content) AS 'Φορές'
FROM Contents_per_Subject cs
GROUP BY Content
ORDER BY 3 DESC
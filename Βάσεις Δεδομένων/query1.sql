SELECT Year,Subject_Number ,group_concat(Content,',')
FROM Contents_per_Subject cs
GROUP BY Year,Subject_Number
ORDER BY 1 DESC
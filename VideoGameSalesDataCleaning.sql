--videogameDatabase Data cleaning
Select *
from VideogameDatabse.dbo.SalesTest
order by RANK



--Some games have sales broken down by region whereas other do not. Make a column that has total Sales
--Create a cloumn for Total_Sales
Alter Table SalesTest
Add Total_Sales float;


-- The sales columns need to be converted to floats before they can be combined
--Also not all games have sales data. These games will be given Total_Sales = 0
Update SalesTest
set Total_Sales = isnull(convert(float,Total_Shipped),0)+isnull(convert(float,global_sales),0);

-- Assign Critic_Score to names that previouslly did not have them Based on Scores from other platforms
--test query
select a.name, a.Platform, b.Platform, a.Critic_Score, isnull(a.Critic_Score, b.Critic_Score)
from SalesTest a
join SalesTest b
	on a.Name = b.Name
where a.Platform != b.Platform
order by name;

--udpate query
Update a
Set Critic_Score = isnull(a.Critic_Score, b.Critic_Score)
from SalesTest a
join SalesTest b
	on a.Name = b.Name
where a.Platform != b.Platform
--This method of updating will slightly inflate the critic scores of games, but some samples I took have only a small change

--Delete games that have no sales data
--(unlike the critic scores above oit makes no sense to compares sales on one platform to another)
delete from SalesTest
where Total_Sales = 0

--The User_Score column goes mostly unused and will be deleted
ALTER TABLE Sales_Test
DROP COLUMN User_Score


--doing the lords work myself
update SalesTest
set Critic_Score = 10
where Name = 'Minecraft'
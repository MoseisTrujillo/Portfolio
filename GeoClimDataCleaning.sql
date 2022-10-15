-- Begin by inpecting and cleaning each data set
select *
from GeoClim.dbo.capital_cities
order by continent desc
-- There does not appear to be any inconsisencies within this table
--(altough upon further review some of the populations are different than what I found)
------------------------------------------------------------------------------------------------------------------------------------------
select *
from GeoClim.dbo.greenhouse_emission
-- Columns have units in each cell, these should be removed (As well as any commas) and the numbers all to be converted to tones


--Starting with co2: seperate the number from the unit
SELECT substring(total_co2, 1, charindex(' ', total_co2)-1) as co2,
substring(total_co2,charindex(' ', total_co2)+1, len(total_co2)) as co2Unit
from GeoClim.dbo.greenhouse_emission


--remove the commas from the numbers
UPDATE GeoClim.dbo.greenhouse_emission
SET total_co2 = REPLACE(total_co2, ',','')


--Make new columns to put in seperated data
ALTER TABLE GeoClim.dbo.greenhouse_emission
Add Co2float float
ALTER TABLE GeoClim.dbo.greenhouse_emission
Add Co2Unit nvarchar(15)


-- Populate each new column with respective data
UPDATE GeoClim.dbo.greenhouse_emission
SET Co2float = convert(float,substring(total_co2, 1, charindex(' ', total_co2)-1))

UPDATE GeoClim.dbo.greenhouse_emission
SET Co2Unit = substring(total_co2,charindex(' ', total_co2)+1, len(total_co2))

--Repeat the process above for the Methane cloumns---
SELECT substring(total_methane, 1, charindex(' ', total_methane)-1) as methane,
substring(total_methane,charindex(' ', total_methane)+1, len(total_methane)) as methaneUnit 
from GeoClim.dbo.greenhouse_emission


--remove the commas from the numbers
UPDATE GeoClim.dbo.greenhouse_emission
SET total_methane = REPLACE(total_methane, ',','')


--Make new columns to put in seperated data
ALTER TABLE GeoClim.dbo.greenhouse_emission
Add Methanefloat float
ALTER TABLE GeoClim.dbo.greenhouse_emission
Add MethaneUnit nvarchar(15)


-- Populate each new column with respective data
UPDATE GeoClim.dbo.greenhouse_emission
SET Methanefloat = convert(float,substring(total_methane, 1, charindex(' ', total_methane)-1))

UPDATE GeoClim.dbo.greenhouse_emission
SET MethaneUnit = substring(total_methane,charindex(' ', total_methane)+1, len(total_co2))




--Now convert both the CO2 and Methane cloumns into tonnes by using the new column made

UPDATE GeoClim.dbo.greenhouse_emission
SET  Co2float =	case
				when Co2Unit = 'm t' THEN Co2float*1000000
				when Co2Unit = 'bn t' THEN Co2float*1000000000
				when Co2Unit = 't' THEN Co2float
			end

UPDATE GeoClim.dbo.greenhouse_emission
SET  Methanefloat =	case
				when MethaneUnit = 'm t' THEN Methanefloat*1000000
				when MethaneUnit = 'bn t' THEN Methanefloat*1000000000
				when MethaneUnit = 't' THEN Methanefloat
			end


--Finish formating and renaming remaining columns. Also drop old co2 and methane columns


ALTER TABLE GeoClim.dbo.greenhouse_emission
DROP COLUMN total_co2, total_methane, Co2Unit, MethaneUnit

--removes the t from each column
UPDATE GeoClim.dbo.greenhouse_emission
SET co2_per_capita = convert(float,substring(co2_per_capita, 1, charindex(' ', co2_per_capita)-1))
UPDATE GeoClim.dbo.greenhouse_emission
SET methane_per_capita = convert(float,substring(methane_per_capita, 1, charindex(' ', methane_per_capita)-1))

--convert each column to float
ALTER TABLE GeoClim.dbo.greenhouse_emission
ALTER COLUMN co2_per_capita float
ALTER TABLE GeoClim.dbo.greenhouse_emission
ALTER COLUMN methane_per_capita float

--apply a unifed naming system
EXEC sp_rename 'GeoClim.dbo.greenhouse_emission.Co2float','total_co2_tons','COLUMN'
EXEC sp_rename 'GeoClim.dbo.greenhouse_emission.Methanefloat','total_methane_tons','COLUMN'
EXEC sp_rename 'GeoClim.dbo.greenhouse_emission.co2_per_capita','co2_per_capita_tons','COLUMN'
EXEC sp_rename 'GeoClim.dbo.greenhouse_emission.methane_per_capita','methane_per_capita_tons','COLUMN'


--Finished table now has floats instead of nvarchars, is all in the same unit, and is ready for analysis/visualization
---------------------------------------------------------------------------------------------------------------------------------


select *
from GeoClim.dbo.mega_cities
--Similar to the capital_cities this table has nothing needing of altering or cleaning.

----------------------------------------------------------------------------------------------------------------------------------
SELECT *
from GeoClim.dbo.mountain_ranges
--provide units for height cloumn name (meters)

EXEC sp_rename 'GeoClim.dbo.mountain_ranges.height','height_m','COLUMN'

--to maintaine some semblance of order; the mountain ranges with mutiple countries will have another column titled 'country2'
ALTER TABLE GeoClim.dbo.mountain_ranges
Add Country2 nvarchar(50)

UPDATE GeoClim.dbo.mountain_ranges
	SET Country2 =  case
						when charindex(',', countries) >2 THEN SUBSTRING(countries, charindex(',', countries)+2, LEN(countries))
					end

update GeoClim.dbo.mountain_ranges
	SET countries	=   case
						when charindex(',', countries) >2 THEN SUBSTRING(countries, 1,charindex(',', countries)-1)
						else countries
					end


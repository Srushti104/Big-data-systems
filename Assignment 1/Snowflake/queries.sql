select f.FATALITY_TYPE, count(f.EVENT_YEARMONTH) as Count
from STORM_FATALITIES as f 
join STORM_DETAILS as d on d.event_id = f.event_id
group by f.FATALITY_TYPE;

select f.EVENT_YEARMONTH,f.FATALITY_TYPE, f.FATALITY_SEX, f.FATALITY_AGE 
from STORM_FATALITIES as f 
join STORM_DETAILS as d on d.event_id = f.event_id;

select (BEGIN_YEARMONTH), sum(INJURIES_INDIRECT) 
from  STORM_DETAILS 
group by BEGIN_YEARMONTH;

select (EVENT_YEARMONTH), avg(FATALITY_AGE) 
from  STORM_FATALITIES 
group by EVENT_YEARMONTH;


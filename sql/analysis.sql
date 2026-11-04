select treatment,count(*) as n_cust 
from customers
group by treatment;
--Q2: 
select avg(recency),avg(history),
round((select count(*) from customers c2 where c2.treatment=c1.treatment and c2.newbie='1')*1.0/count(*),10) as new_bie_share
from  
customers c1
group by treatment;
--Q3
select treatment, round(avg(visit),2)*100 as visit_rate,round(avg(conversion),5)*100 as conversion_rate from customers group by treatment;
--Q4
select avg(case when treatment =1 then visit end)*100 as treated_visit_rate,
 avg(case when treatment =0 then visit end )*100 as control_visit_rate ,
(avg(case when treatment = 1 then visit end) - avg(case when treatment = 0 then visit end)) * 100 as visit_uplift_pp
 
from customers;
--Q5(channel_part)
select channel,avg(case when treatment =1 then visit end)*100 as treated_visit_rate,
 avg(case when treatment =0 then visit end )*100 as control_visit_rate ,
(avg(case when treatment = 1 then visit end) - avg(case when treatment = 0 then visit end)) * 100 as visit_uplift_pp
 
from customers
group by channel;
--Q5(newbie_part)


select newbie,avg(case when treatment =1 then visit end)*100 as treated_visit_rate,
 avg(case when treatment =0 then visit end )*100 as control_visit_rate ,
(avg(case when treatment = 1 then visit end) - avg(case when treatment = 0 then visit end)) * 100 as visit_uplift_pp
 
from customers
group by newbie;
--Q5(recency_part)


with rb as(select *,case
when recency  between 1 and 4 then 'band 1-4'
when recency between 5 and 8 then 'band 5-8'
when recency between 9 and 12 then 'band 9-12'
else 'band >1year' end
 as recency_band

from customers


)

select recency_band,avg(case when treatment =1 then visit end)*100 as treated_visit_rate,
 avg(case when treatment =0 then visit end )*100 as control_visit_rate ,
(avg(case when treatment = 1 then visit end) - avg(case when treatment = 0 then visit end)) * 100 as visit_uplift_pp
 
from rb
group by recency_band
order by recency_band;
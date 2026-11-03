select treatment,count(*) as n_cust 
from customers
group by treatment;
--Q2: 
select avg(recency),avg(history),
(select count(*) from customers c2 where c2.treatment=c1.treatment and newbie=1)/count(*) as new_bie_share
from  
customers c1
group by treatment
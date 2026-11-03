select treatment,count(*) as n_cust 
from customers
group by treatment
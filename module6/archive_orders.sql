begin;

create table "Orders_may"
as table "Orders"
with no data;

insert into "Orders_may"
select * from "Orders"
where order_date >= '2025-05-01' and order_date < '2025-06-01';

delete from "Orders"
where order_date >= '2025-05-01' and order_date < '2025-06-01';

commit;
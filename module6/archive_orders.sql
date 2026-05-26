begin;

create table "Orders_may"
as table "Orders"
with no data;

insert into "Orders_may"
select * from "Orders"
where order_date between '2026-05-01' and '2026-06-01';

delete from "OrdersItems"
where order_id in (
	select id from "Orders"
	where order_date between '2026-05-01' and '2026-06-01'
);

delete from "Orders"
where order_date between '2026-05-01' and '2026-06-01';

commit;
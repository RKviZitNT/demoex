create or replace function get_order_report(
	p_start_date timestamp,
	p_end_date timestamp	
)
returns table (
	customer_name varchar,
    total_orders bigint,
    total_products numeric,
    total_amount numeric
)
as $$
begin
	return query

	select
		c.name,
		count(distinct o.id),
		sum(oi.quantity),
		sum(o.amount)
	from "Orders" o
	join "Customers" c
		on c.id = o.customer_id
	join "OrdersItems" oi
		on oi.order_id = o.id
	where o.order_date between p_start_date and p_end_date
	group by c.name;
end;
$$ language plpgsql;

SELECT *
FROM get_orders_report(
    '2025-01-01',
    '2025-12-31'
);
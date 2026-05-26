create or replace function max_orders_info(
	start_date timestamp,
	end_date timestamp
)
returns table (
	client_name varchar,
	orders_count bigint,
	products_quantity numeric,
	total_amount numeric
)
language plpgsql
as $$
begin
	
	return query
	
	select
		c.name,
		count(distinct o.id),
		sum(oi.quantity),
		sum(distinct o.total_amount)
	from "Orders" o
	join "Clients" c
		on c.id = o.client_id
	join "OrdersItems" oi
		on oi.order_id = o.id
	where o.order_date between start_date and end_date
	group by c.name
	order by sum(distinct o.total_amount) desc
	limit 1;

end;
$$;


select * from max_orders_info('2026-05-01', '2026-06-01')
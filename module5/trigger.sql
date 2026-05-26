create or replace function calc_order_total_amount()
returns trigger
language plpgsql
as $$

declare product_cost numeric;

begin

	select
		sum(sm.quantity * mp.price * new.quantity)
	into product_cost
	from "Specifications" s
	join "SpecificationsMaterials" sm
		on sm.specification_id = s.id
	join "MaterialsPrices" mp
		on mp.material_id = sm.material_id
	where s.product_id = new.product_id;

	update "Orders"
	set total_amount = coalesce(total_amount, 0) + coalesce(product_cost, 0)
	where id = new.order_id;

	return new;

end;
$$;

create trigger trg_calc_order_total_amount
after insert on "OrdersItems"
for each row
execute function calc_order_total_amount();
create or replace function calculate_order_amount()
returns trigger
as $$
declare
	product_cost numeric(12,2);
begin
	select
		sum(sm.quantity * mp.price)
	into product_cost
	from "Specifications" s
	join "SpecificationsMaterials" sm
		on sm.specification_id = s.id
	join "MaterialsPrices" mp
		on mp.material_is = sm.material_id
	where s.product_id = NEW.product_id;

	update "OrdersItems"
	set amount = NEW.quantity * product_cost,
		price_per_unit = product_cost
	where id = NEW.id;

	update "Orders"
	set amount = (
		select sum(amount)
		from "OrdersItems"
		where order_id = NEW.order_id
	)
	where id = NEW.order_id;

	return NEW;
end;
$$ language plpgsql;

CREATE TRIGGER trg_calculate_order_amount
AFTER INSERT ON "OrdersItems"
FOR EACH ROW
EXECUTE FUNCTION calculate_order_amount();
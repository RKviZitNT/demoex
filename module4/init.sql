BEGIN;


CREATE TABLE IF NOT EXISTS public."Clients"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    phone character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT "Clients_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Manufacturers"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    phone character varying(20) COLLATE pg_catalog."default",
    email character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT "Manufacturers_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Materials"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    article_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    unit character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Materials_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."MaterialsPrices"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    material_id integer NOT NULL,
    price numeric(12, 2) NOT NULL,
    CONSTRAINT "MaterialsPrices_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Orders"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    manufacturer_id integer NOT NULL,
    client_id integer NOT NULL,
    total_amount numeric(12, 2),
    order_date timestamp(0) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Orders_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."OrdersItems"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    quantity numeric(12, 3) NOT NULL,
    CONSTRAINT "OrdersItems_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Productions"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    product_id integer NOT NULL,
    quantity numeric(12, 3) NOT NULL,
    production_date timestamp(0) with time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "Productions_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Products"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    article_code character varying(20) COLLATE pg_catalog."default" NOT NULL,
    unit character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "Products_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."ProductsPrices"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    product_id integer NOT NULL,
    price numeric(12, 2) NOT NULL,
    CONSTRAINT "ProductsPrices_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Specifications"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    product_id integer NOT NULL,
    manufacturer_id integer NOT NULL,
    quantity numeric(12, 3) NOT NULL,
    CONSTRAINT "Specifications_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."SpecificationsMaterials"
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    specification_id integer NOT NULL,
    material_id integer NOT NULL,
    quantity numeric(12, 3) NOT NULL,
    CONSTRAINT "SpecificationsMaterials_pkey" PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public."MaterialsPrices"
    ADD CONSTRAINT material_id FOREIGN KEY (material_id)
    REFERENCES public."Materials" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Orders"
    ADD CONSTRAINT client_id FOREIGN KEY (client_id)
    REFERENCES public."Clients" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Orders"
    ADD CONSTRAINT manufacturer_id FOREIGN KEY (manufacturer_id)
    REFERENCES public."Manufacturers" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."OrdersItems"
    ADD CONSTRAINT order_id FOREIGN KEY (order_id)
    REFERENCES public."Orders" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Productions"
    ADD CONSTRAINT product_id FOREIGN KEY (product_id)
    REFERENCES public."Products" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public."ProductsPrices"
    ADD CONSTRAINT product_id FOREIGN KEY (product_id)
    REFERENCES public."Products" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Specifications"
    ADD CONSTRAINT manufacturer_id FOREIGN KEY (manufacturer_id)
    REFERENCES public."Manufacturers" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Specifications"
    ADD CONSTRAINT product_id FOREIGN KEY (product_id)
    REFERENCES public."Products" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."SpecificationsMaterials"
    ADD CONSTRAINT material_id FOREIGN KEY (material_id)
    REFERENCES public."Materials" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."SpecificationsMaterials"
    ADD CONSTRAINT specification_id FOREIGN KEY (specification_id)
    REFERENCES public."Specifications" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;
--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2 (Debian 17.2-1.pgdg120+1)
-- Dumped by pg_dump version 17.2 (Debian 17.2-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: products; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL,
    price numeric(10,2) NOT NULL
);


ALTER TABLE public.products OWNER TO "user";

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO "user";

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    role character varying(255) NOT NULL
);


ALTER TABLE public.roles OWNER TO "user";

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO "user";

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role_id integer
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO "user";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.products (id, name, description, price) FROM stdin;
1	Laptop	High-performance laptop with 16GB RAM and 512GB SSD.	1200.99
2	Smartphone	Latest smartphone with 5G connectivity and 128GB storage.	799.49
3	Wireless Headphones	Noise-cancelling over-ear headphones.	199.99
4	Gaming Chair	Ergonomic gaming chair with adjustable armrests.	259.99
5	Mechanical Keyboard	RGB backlit mechanical keyboard with Cherry MX switches.	129.99
18	4K Monitor lyalya	27-inch 4K UHD monitor with HDR support. Sales! Hurry up!	369.01
19	4K Monitor pupupu	27-inch 4K UHD monitor with HDR support. Sales! Hurry up!	270.00
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.roles (id, role) FROM stdin;
1	user
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.users (id, username, email, password, role_id) FROM stdin;
7	aleksei	aleksei.petrov123@mail.ru	$2b$12$sEbClVJbMGzrxOHUEB3onuhAtCHdbKR0q6snoTtZevzRgg3oFeXj2	1
8	ivan8	ivan.kuznetsov2@mail.ru	$2b$12$3GCiLiF8CBsGO71/59YHkOafjL2wemhbT6vzdPw4K3qltP7m9ki4m	1
\.


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.products_id_seq', 19, true);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users fk_role; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--


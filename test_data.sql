--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: test_data; Type: SCHEMA; Schema: -; Owner: mkenny
--

CREATE SCHEMA test_data;


ALTER SCHEMA test_data OWNER TO mkenny;

--
-- Name: test_geoms; Type: SCHEMA; Schema: -; Owner: mkenny
--

CREATE SCHEMA test_geoms;


ALTER SCHEMA test_geoms OWNER TO mkenny;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: mkenny
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO mkenny;

SET search_path = test_data, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: test_lines; Type: TABLE; Schema: test_data; Owner: mkenny; Tablespace: 
--

CREATE TABLE test_lines (
    gid integer NOT NULL,
    id numeric(10,0),
    name character varying(10),
    geom public.geometry(MultiLineString,4326),
    topogeoms topology.topogeometry,
    CONSTRAINT check_topogeom_topogeoms CHECK (((((topogeoms).topology_id = 1) AND ((topogeoms).layer_id = 2)) AND ((topogeoms).type = 2)))
);


ALTER TABLE test_data.test_lines OWNER TO mkenny;

--
-- Name: test_lines_gid_seq; Type: SEQUENCE; Schema: test_data; Owner: mkenny
--

CREATE SEQUENCE test_lines_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_data.test_lines_gid_seq OWNER TO mkenny;

--
-- Name: test_lines_gid_seq; Type: SEQUENCE OWNED BY; Schema: test_data; Owner: mkenny
--

ALTER SEQUENCE test_lines_gid_seq OWNED BY test_lines.gid;


--
-- Name: test_points; Type: TABLE; Schema: test_data; Owner: mkenny; Tablespace: 
--

CREATE TABLE test_points (
    gid integer NOT NULL,
    id numeric(10,0),
    name character varying(10),
    geom public.geometry(Point,4326),
    topogeoms topology.topogeometry,
    CONSTRAINT check_topogeom_topogeoms CHECK (((((topogeoms).topology_id = 1) AND ((topogeoms).layer_id = 1)) AND ((topogeoms).type = 1)))
);


ALTER TABLE test_data.test_points OWNER TO mkenny;

--
-- Name: test_points_gid_seq; Type: SEQUENCE; Schema: test_data; Owner: mkenny
--

CREATE SEQUENCE test_points_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_data.test_points_gid_seq OWNER TO mkenny;

--
-- Name: test_points_gid_seq; Type: SEQUENCE OWNED BY; Schema: test_data; Owner: mkenny
--

ALTER SEQUENCE test_points_gid_seq OWNED BY test_points.gid;


--
-- Name: test_polygons; Type: TABLE; Schema: test_data; Owner: mkenny; Tablespace: 
--

CREATE TABLE test_polygons (
    gid integer NOT NULL,
    id numeric(10,0),
    name character varying(10),
    geom public.geometry(MultiPolygon,4326),
    topogeoms topology.topogeometry,
    CONSTRAINT check_topogeom_topogeoms CHECK (((((topogeoms).topology_id = 1) AND ((topogeoms).layer_id = 3)) AND ((topogeoms).type = 3)))
);


ALTER TABLE test_data.test_polygons OWNER TO mkenny;

--
-- Name: test_polygons_gid_seq; Type: SEQUENCE; Schema: test_data; Owner: mkenny
--

CREATE SEQUENCE test_polygons_gid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_data.test_polygons_gid_seq OWNER TO mkenny;

--
-- Name: test_polygons_gid_seq; Type: SEQUENCE OWNED BY; Schema: test_data; Owner: mkenny
--

ALTER SEQUENCE test_polygons_gid_seq OWNED BY test_polygons.gid;


SET search_path = test_geoms, pg_catalog;

--
-- Name: edge_data; Type: TABLE; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE TABLE edge_data (
    edge_id integer NOT NULL,
    start_node integer NOT NULL,
    end_node integer NOT NULL,
    next_left_edge integer NOT NULL,
    abs_next_left_edge integer NOT NULL,
    next_right_edge integer NOT NULL,
    abs_next_right_edge integer NOT NULL,
    left_face integer NOT NULL,
    right_face integer NOT NULL,
    geom public.geometry(LineString,4326)
);


ALTER TABLE test_geoms.edge_data OWNER TO mkenny;

--
-- Name: edge; Type: VIEW; Schema: test_geoms; Owner: mkenny
--

CREATE VIEW edge AS
 SELECT edge_data.edge_id,
    edge_data.start_node,
    edge_data.end_node,
    edge_data.next_left_edge,
    edge_data.next_right_edge,
    edge_data.left_face,
    edge_data.right_face,
    edge_data.geom
   FROM edge_data;


ALTER TABLE test_geoms.edge OWNER TO mkenny;

--
-- Name: VIEW edge; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON VIEW edge IS 'Contains edge topology primitives';


--
-- Name: COLUMN edge.edge_id; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.edge_id IS 'Unique identifier of the edge';


--
-- Name: COLUMN edge.start_node; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.start_node IS 'Unique identifier of the node at the start of the edge';


--
-- Name: COLUMN edge.end_node; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.end_node IS 'Unique identifier of the node at the end of the edge';


--
-- Name: COLUMN edge.next_left_edge; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.next_left_edge IS 'Unique identifier of the next edge of the face on the left (when looking in the direction from START_NODE to END_NODE), moving counterclockwise around the face boundary';


--
-- Name: COLUMN edge.next_right_edge; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.next_right_edge IS 'Unique identifier of the next edge of the face on the right (when looking in the direction from START_NODE to END_NODE), moving counterclockwise around the face boundary';


--
-- Name: COLUMN edge.left_face; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.left_face IS 'Unique identifier of the face on the left side of the edge when looking in the direction from START_NODE to END_NODE';


--
-- Name: COLUMN edge.right_face; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.right_face IS 'Unique identifier of the face on the right side of the edge when looking in the direction from START_NODE to END_NODE';


--
-- Name: COLUMN edge.geom; Type: COMMENT; Schema: test_geoms; Owner: mkenny
--

COMMENT ON COLUMN edge.geom IS 'The geometry of the edge';


--
-- Name: edge_data_edge_id_seq; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE edge_data_edge_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.edge_data_edge_id_seq OWNER TO mkenny;

--
-- Name: edge_data_edge_id_seq; Type: SEQUENCE OWNED BY; Schema: test_geoms; Owner: mkenny
--

ALTER SEQUENCE edge_data_edge_id_seq OWNED BY edge_data.edge_id;


--
-- Name: face; Type: TABLE; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE TABLE face (
    face_id integer NOT NULL,
    mbr public.geometry(Polygon,4326)
);


ALTER TABLE test_geoms.face OWNER TO mkenny;

--
-- Name: face_face_id_seq; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE face_face_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.face_face_id_seq OWNER TO mkenny;

--
-- Name: face_face_id_seq; Type: SEQUENCE OWNED BY; Schema: test_geoms; Owner: mkenny
--

ALTER SEQUENCE face_face_id_seq OWNED BY face.face_id;


--
-- Name: layer_id_seq; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE layer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.layer_id_seq OWNER TO mkenny;

--
-- Name: node; Type: TABLE; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE TABLE node (
    node_id integer NOT NULL,
    containing_face integer,
    geom public.geometry(Point,4326)
);


ALTER TABLE test_geoms.node OWNER TO mkenny;

--
-- Name: node_node_id_seq; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE node_node_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.node_node_id_seq OWNER TO mkenny;

--
-- Name: node_node_id_seq; Type: SEQUENCE OWNED BY; Schema: test_geoms; Owner: mkenny
--

ALTER SEQUENCE node_node_id_seq OWNED BY node.node_id;


--
-- Name: relation; Type: TABLE; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE TABLE relation (
    topogeo_id integer NOT NULL,
    layer_id integer NOT NULL,
    element_id integer NOT NULL,
    element_type integer NOT NULL
);


ALTER TABLE test_geoms.relation OWNER TO mkenny;

--
-- Name: topogeo_s_1; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE topogeo_s_1
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.topogeo_s_1 OWNER TO mkenny;

--
-- Name: topogeo_s_2; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE topogeo_s_2
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.topogeo_s_2 OWNER TO mkenny;

--
-- Name: topogeo_s_3; Type: SEQUENCE; Schema: test_geoms; Owner: mkenny
--

CREATE SEQUENCE topogeo_s_3
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE test_geoms.topogeo_s_3 OWNER TO mkenny;

SET search_path = test_data, pg_catalog;

--
-- Name: gid; Type: DEFAULT; Schema: test_data; Owner: mkenny
--

ALTER TABLE ONLY test_lines ALTER COLUMN gid SET DEFAULT nextval('test_lines_gid_seq'::regclass);


--
-- Name: gid; Type: DEFAULT; Schema: test_data; Owner: mkenny
--

ALTER TABLE ONLY test_points ALTER COLUMN gid SET DEFAULT nextval('test_points_gid_seq'::regclass);


--
-- Name: gid; Type: DEFAULT; Schema: test_data; Owner: mkenny
--

ALTER TABLE ONLY test_polygons ALTER COLUMN gid SET DEFAULT nextval('test_polygons_gid_seq'::regclass);


SET search_path = test_geoms, pg_catalog;

--
-- Name: edge_id; Type: DEFAULT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data ALTER COLUMN edge_id SET DEFAULT nextval('edge_data_edge_id_seq'::regclass);


--
-- Name: face_id; Type: DEFAULT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY face ALTER COLUMN face_id SET DEFAULT nextval('face_face_id_seq'::regclass);


--
-- Name: node_id; Type: DEFAULT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY node ALTER COLUMN node_id SET DEFAULT nextval('node_node_id_seq'::regclass);


SET search_path = test_data, pg_catalog;

--
-- Data for Name: test_lines; Type: TABLE DATA; Schema: test_data; Owner: mkenny
--

COPY test_lines (gid, id, name, geom, topogeoms) FROM stdin;
1	3	Neptune	0105000020E61000000100000001020000000400000098C2ADCC7F1D554040219BB878B54B406005545D8AC8544000D42B0BAB6A43C0402FA6BA0188604020DFC44DD51642C068AC8B4838675F40F063314876BE4340	(1,2,1,2)
2	2	Venus	0105000020E610000001000000010200000002000000A8432722957849C0A043B6BAA53F34C0B06370CF66F24E40A043B6BAA53F34C0	(1,2,2,2)
3	1	Mars	0105000020E6100000010000000102000000020000000C543800B3915FC0C08B052FB8D20F40FC53E4BE220756C0A0426680F7B94740	(1,2,3,2)
\.


--
-- Name: test_lines_gid_seq; Type: SEQUENCE SET; Schema: test_data; Owner: mkenny
--

SELECT pg_catalog.setval('test_lines_gid_seq', 3, true);


--
-- Data for Name: test_points; Type: TABLE DATA; Schema: test_data; Owner: mkenny
--

COPY test_points (gid, id, name, geom, topogeoms) FROM stdin;
1	3	Red	0101000020E6100000F8B241BE55764BC0E87BB330078F2AC0	(1,1,1,1)
2	2	Green	0101000020E6100000F28AE4BE22075640CCA65F59873A4740	(1,1,2,1)
3	1	Blue	0101000020E61000004FC3429B66ED59C0A89B3E9656BD4440	(1,1,3,1)
\.


--
-- Name: test_points_gid_seq; Type: SEQUENCE SET; Schema: test_data; Owner: mkenny
--

SELECT pg_catalog.setval('test_points_gid_seq', 3, true);


--
-- Data for Name: test_polygons; Type: TABLE DATA; Schema: test_data; Owner: mkenny
--

COPY test_polygons (gid, id, name, geom, topogeoms) FROM stdin;
1	3	Pie	0106000020E6100000010000000103000000010000000500000076A4CF5EC47260C0989C8ED0044331C01306A5EBEDAF57C0C8701AEEDCE22BC061757B472BC557C02B3835E5478D4AC076A4CF5EC47260C0C716E29CC2B74AC076A4CF5EC47260C0989C8ED0044331C0	(1,3,1,3)
2	2	Cookie	0106000020E6100000010000000103000000010000000500000078DDD21FEEB43C403C7A63CDCA16414068F45533A6F44C40ACF416ACB5C0414054421D87E11C4F4000A237B40C2B0D4070FF56F4BC2D40408022649C66C9FF3F78DDD21FEEB43C403C7A63CDCA164140	(1,3,2,3)
3	1	Mint	0106000020E6100000010000000103000000010000000500000043E7DBCF93FA62C09C3775465DD75040F6A1BB136BD15FC08685F859151751402106B5ECFA515FC0B09BC6165D8E4840F577057456E562C08437CD3DCD0D494043E7DBCF93FA62C09C3775465DD75040	(1,3,3,3)
\.


--
-- Name: test_polygons_gid_seq; Type: SEQUENCE SET; Schema: test_data; Owner: mkenny
--

SELECT pg_catalog.setval('test_polygons_gid_seq', 3, true);


SET search_path = test_geoms, pg_catalog;

--
-- Data for Name: edge_data; Type: TABLE DATA; Schema: test_geoms; Owner: mkenny
--

COPY edge_data (edge_id, start_node, end_node, next_left_edge, abs_next_left_edge, next_right_edge, abs_next_right_edge, left_face, right_face, geom) FROM stdin;
1	4	5	-1	1	1	1	0	0	0102000020E61000000400000098C2ADCC7F1D554040219BB878B54B406005545D8AC8544000D42B0BAB6A43C0402FA6BA0188604020DFC44DD51642C068AC8B4838675F40F063314876BE4340
2	6	7	-2	2	2	2	0	0	0102000020E610000002000000A8432722957849C0A043B6BAA53F34C0B06370CF66F24E40A043B6BAA53F34C0
3	8	9	-3	3	3	3	0	0	0102000020E6100000020000000C543800B3915FC0C08B052FB8D20F40FC53E4BE220756C0A0426680F7B94740
4	10	10	4	4	-4	4	0	1	0102000020E61000000500000076A4CF5EC47260C0989C8ED0044331C01306A5EBEDAF57C0C8701AEEDCE22BC061757B472BC557C02B3835E5478D4AC076A4CF5EC47260C0C716E29CC2B74AC076A4CF5EC47260C0989C8ED0044331C0
5	11	11	5	5	-5	5	0	2	0102000020E61000000500000078DDD21FEEB43C403C7A63CDCA16414068F45533A6F44C40ACF416ACB5C0414054421D87E11C4F4000A237B40C2B0D4070FF56F4BC2D40408022649C66C9FF3F78DDD21FEEB43C403C7A63CDCA164140
6	12	12	6	6	-6	6	0	3	0102000020E61000000500000043E7DBCF93FA62C09C3775465DD75040F6A1BB136BD15FC08685F859151751402106B5ECFA515FC0B09BC6165D8E4840F577057456E562C08437CD3DCD0D494043E7DBCF93FA62C09C3775465DD75040
\.


--
-- Name: edge_data_edge_id_seq; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('edge_data_edge_id_seq', 6, true);


--
-- Data for Name: face; Type: TABLE DATA; Schema: test_geoms; Owner: mkenny
--

COPY face (face_id, mbr) FROM stdin;
0	\N
1	0103000020E6100000010000000500000076A4CF5EC47260C0C716E29CC2B74AC076A4CF5EC47260C0C8701AEEDCE22BC01306A5EBEDAF57C0C8701AEEDCE22BC01306A5EBEDAF57C0C716E29CC2B74AC076A4CF5EC47260C0C716E29CC2B74AC0
2	0103000020E6100000010000000500000078DDD21FEEB43C408022649C66C9FF3F78DDD21FEEB43C40ACF416ACB5C0414054421D87E11C4F40ACF416ACB5C0414054421D87E11C4F408022649C66C9FF3F78DDD21FEEB43C408022649C66C9FF3F
3	0103000020E6100000010000000500000043E7DBCF93FA62C0B09BC6165D8E484043E7DBCF93FA62C08685F859151751402106B5ECFA515FC08685F859151751402106B5ECFA515FC0B09BC6165D8E484043E7DBCF93FA62C0B09BC6165D8E4840
\.


--
-- Name: face_face_id_seq; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('face_face_id_seq', 3, true);


--
-- Name: layer_id_seq; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('layer_id_seq', 3, true);


--
-- Data for Name: node; Type: TABLE DATA; Schema: test_geoms; Owner: mkenny
--

COPY node (node_id, containing_face, geom) FROM stdin;
1	0	0101000020E6100000F8B241BE55764BC0E87BB330078F2AC0
2	0	0101000020E6100000F28AE4BE22075640CCA65F59873A4740
3	0	0101000020E61000004FC3429B66ED59C0A89B3E9656BD4440
4	\N	0101000020E610000098C2ADCC7F1D554040219BB878B54B40
5	\N	0101000020E610000068AC8B4838675F40F063314876BE4340
6	\N	0101000020E6100000A8432722957849C0A043B6BAA53F34C0
7	\N	0101000020E6100000B06370CF66F24E40A043B6BAA53F34C0
8	\N	0101000020E61000000C543800B3915FC0C08B052FB8D20F40
9	\N	0101000020E6100000FC53E4BE220756C0A0426680F7B94740
10	\N	0101000020E610000076A4CF5EC47260C0989C8ED0044331C0
11	\N	0101000020E610000078DDD21FEEB43C403C7A63CDCA164140
12	\N	0101000020E610000043E7DBCF93FA62C09C3775465DD75040
\.


--
-- Name: node_node_id_seq; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('node_node_id_seq', 12, true);


--
-- Data for Name: relation; Type: TABLE DATA; Schema: test_geoms; Owner: mkenny
--

COPY relation (topogeo_id, layer_id, element_id, element_type) FROM stdin;
1	1	1	1
2	1	2	1
3	1	3	1
1	2	1	2
2	2	2	2
3	2	3	2
1	3	1	3
2	3	2	3
3	3	3	3
\.


--
-- Name: topogeo_s_1; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('topogeo_s_1', 3, true);


--
-- Name: topogeo_s_2; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('topogeo_s_2', 3, true);


--
-- Name: topogeo_s_3; Type: SEQUENCE SET; Schema: test_geoms; Owner: mkenny
--

SELECT pg_catalog.setval('topogeo_s_3', 3, true);


SET search_path = topology, pg_catalog;

--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: mkenny
--

COPY topology (id, name, srid, "precision", hasz) FROM stdin;
1	test_geoms	4326	0	f
\.

--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: mkenny
--

COPY layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
1	1	test_data	test_points	topogeoms	1	0	\N
1	2	test_data	test_lines	topogeoms	2	0	\N
1	3	test_data	test_polygons	topogeoms	3	0	\N
\.


SET search_path = test_data, pg_catalog;

--
-- Name: test_lines_pkey; Type: CONSTRAINT; Schema: test_data; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY test_lines
    ADD CONSTRAINT test_lines_pkey PRIMARY KEY (gid);


--
-- Name: test_points_pkey; Type: CONSTRAINT; Schema: test_data; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY test_points
    ADD CONSTRAINT test_points_pkey PRIMARY KEY (gid);


--
-- Name: test_polygons_pkey; Type: CONSTRAINT; Schema: test_data; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY test_polygons
    ADD CONSTRAINT test_polygons_pkey PRIMARY KEY (gid);


SET search_path = test_geoms, pg_catalog;

--
-- Name: edge_data_pkey; Type: CONSTRAINT; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT edge_data_pkey PRIMARY KEY (edge_id);


--
-- Name: face_primary_key; Type: CONSTRAINT; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY face
    ADD CONSTRAINT face_primary_key PRIMARY KEY (face_id);


--
-- Name: node_primary_key; Type: CONSTRAINT; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY node
    ADD CONSTRAINT node_primary_key PRIMARY KEY (node_id);


--
-- Name: relation_layer_id_topogeo_id_element_id_element_type_key; Type: CONSTRAINT; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

ALTER TABLE ONLY relation
    ADD CONSTRAINT relation_layer_id_topogeo_id_element_id_element_type_key UNIQUE (layer_id, topogeo_id, element_id, element_type);


--
-- Name: edge_end_node_idx; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX edge_end_node_idx ON edge_data USING btree (end_node);


--
-- Name: edge_gist; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX edge_gist ON edge_data USING gist (geom);


--
-- Name: edge_left_face_idx; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX edge_left_face_idx ON edge_data USING btree (left_face);


--
-- Name: edge_right_face_idx; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX edge_right_face_idx ON edge_data USING btree (right_face);


--
-- Name: edge_start_node_idx; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX edge_start_node_idx ON edge_data USING btree (start_node);


--
-- Name: face_gist; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX face_gist ON face USING gist (mbr);


--
-- Name: node_gist; Type: INDEX; Schema: test_geoms; Owner: mkenny; Tablespace: 
--

CREATE INDEX node_gist ON node USING gist (geom);


--
-- Name: edge_insert_rule; Type: RULE; Schema: test_geoms; Owner: mkenny
--

CREATE RULE edge_insert_rule AS
    ON INSERT TO edge DO INSTEAD  INSERT INTO edge_data (edge_id, start_node, end_node, next_left_edge, abs_next_left_edge, next_right_edge, abs_next_right_edge, left_face, right_face, geom)
  VALUES (new.edge_id, new.start_node, new.end_node, new.next_left_edge, abs(new.next_left_edge), new.next_right_edge, abs(new.next_right_edge), new.left_face, new.right_face, new.geom);


--
-- Name: relation_integrity_checks; Type: TRIGGER; Schema: test_geoms; Owner: mkenny
--

CREATE TRIGGER relation_integrity_checks BEFORE INSERT OR UPDATE ON relation FOR EACH ROW EXECUTE PROCEDURE topology.relationtrigger('1', 'test_geoms');


--
-- Name: end_node_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT end_node_exists FOREIGN KEY (end_node) REFERENCES node(node_id);


--
-- Name: face_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY node
    ADD CONSTRAINT face_exists FOREIGN KEY (containing_face) REFERENCES face(face_id);


--
-- Name: left_face_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT left_face_exists FOREIGN KEY (left_face) REFERENCES face(face_id);


--
-- Name: next_left_edge_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT next_left_edge_exists FOREIGN KEY (abs_next_left_edge) REFERENCES edge_data(edge_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: next_right_edge_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT next_right_edge_exists FOREIGN KEY (abs_next_right_edge) REFERENCES edge_data(edge_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: right_face_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT right_face_exists FOREIGN KEY (right_face) REFERENCES face(face_id);


--
-- Name: start_node_exists; Type: FK CONSTRAINT; Schema: test_geoms; Owner: mkenny
--

ALTER TABLE ONLY edge_data
    ADD CONSTRAINT start_node_exists FOREIGN KEY (start_node) REFERENCES node(node_id);


--
-- PostgreSQL database dump complete
--


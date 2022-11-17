CREATE DATABASE if not exists skanestas on cluster skanestas
 
 CREATE TABLE IF NOT EXISTS skanestas.skanestas_tests_queue ON CLUSTER skanestas(
   `timestamp` Float64,
   `bid_01` Float64,
   `bid_02` Float64,
   `bid_50` Float64,
   `ask_01` Float64,
   `ask_02` Float64,
   `ask_50` Float64,
   `stats` Array(Float64),
   `ask_01_bid_01_avg` Float64
  ) ENGINE = Kafka
  SETTINGS kafka_broker_list = 'kafka:9092',
           kafka_topic_list = 'skanestas',
           kafka_group_name = 'skanestas_tests',
           kafka_format = 'JSONEachRow',
           kafka_num_consumers = 1;
                           
CREATE TABLE IF NOT EXISTS skanestas.skanestas_tests_sharded ON CLUSTER skanestas AS skanestas.skanestas_tests_queue
ENGINE=ReplicatedReplacingMergeTree('/clickhouse/tables/{shard_id}/skanestas/skanestas_tests_sharded', '{replica_id}')
ORDER BY (`timestamp`)

CREATE TABLE IF NOT EXISTS skanestas.skanestas_tests ON CLUSTER skanestas AS skanestas.skanestas_tests_queue
ENGINE = Distributed(skanestas, skanestas, skanestas_tests_sharded, rand())

CREATE MATERIALIZED VIEW IF NOT EXISTS skanestas.skanestas_tests_mv ON CLUSTER skanestas 
TO skanestas.skanestas_tests AS SELECT * FROM skanestas.skanestas_tests_queue


drop table if exists skanestas.skanestas_tests_queue ON CLUSTER skanestas
drop table if exists skanestas.skanestas_tests_sharded ON CLUSTER skanestas
drop table if exists skanestas.skanestas_tests ON CLUSTER skanestas
drop table if exists skanestas.skanestas_tests_mv ON CLUSTER skanestas


select * from  skanestas.skanestas_tests
select * from  skanestas.skanestas_tests_mv
select * from  skanestas.skanestas.skanestas_tests_queue

select JSONExtractRaw("[{'timestamp': '1668658915439.2131', 'bid_01': '7.7316928783884', 'bid_02': '16.510998445009285', 'bid_50': '111.05872161430167', 'ask_01': '6.865211039748251', 'ask_02': '8.85504272178183', 'ask_50': '50.16157154222556', 'stats': '22'}]")

{'timestamp': 1668653837608.18, 'bid_01': 8.562168544648383, 'bid_02': 10.220734729662782, 'bid_50': 204.5408395811982, 'ask_01': 2.1456252023244424, 'ask_02': 12.365048307709852, 'ask_50': 206.00781894193764, 'stats': {'bidavg': 74.44124761850313, 'askavg': 73.50616415065731}}

{"timestamp": "unix timestamp",
"bid_01":   "float",
"bid_02":   "float",
"bid_50":   "float",
"ask_01":   "float",
"ask_02":   "float",
"ask_50":   "float",
"stats":    "json"}
# Skanestas_tests
if you clone project from non root user, before up and build project you have to create data directories:
 mkdir -p /path/to/project/ch/ch_data
 mkdir -p /path/to/project/kafka/kafka_data
or set proper rights
kafka catalog needs chown -R 1001:1001 /path/to/project/kafka
need to install pip install kafka-python, statistics
import clickhouse_connect
import datetime
import logging
import os,json

#client = clickhouse_connect.get_client(host='stage-dbs02.vprok.tech', port=8123, username='default', password='123qweasd')
#result = client.query("select host_name, host_address from system.clusters where cluster='skanestas'")
#result = client.query("select bid_01, ask_01 from  skanestas.skanestas_tests_mv")
#host_name=result.result_set
#if host_name.__str__() != '[]':
#    print(host_name[1])
ch_addr='stage-dbs02.vprok.tech'
ch_port=8123
ch_user='default'
ch_pass='123qweasd'
ch_cluster='skanestas'
ch_db='skanestas'

def main():
    check_db()

def clickhouse(host, port, user, passwd, query):
    try:    
        with clickhouse_connect.get_client(host=host, port=port, username=user, password=passwd) as connect:
            res=connect.query(query)
        return res.result_set
    except Exception as e:
        logging.error(e)

def cluster(): #Собираем все ноды кластера
    query='%s%s%s' %("select host_name, host_address from system.clusters where cluster='",ch_cluster,"'" )
    res=clickhouse(ch_addr, ch_port, ch_user, ch_pass, query)
    return res

def check_db():
    nodes=cluster()
    query='%s%s%s' %("select name from system.databases where name='",ch_db,"'" )
    for i in nodes:
        ch_addr=i[0]
        res=clickhouse(ch_addr, ch_port, ch_user, ch_pass, query) #Проверяем есть ли БД на ноде
        if res.__str__() == "[]":
            query='%s%s%s%s' %("CREATE DATABASE if not exists ",ch_db," on cluster ", ch_cluster )
            clickhouse(ch_addr, ch_port, ch_user, ch_pass, query)#Создаем БД на ноде с он кластер
    
def check_table():
    query='%s%s%s' %("select name from system.tables where database='",ch_db,"'" )


main()    
    
 

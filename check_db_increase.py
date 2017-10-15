import re
import MySQLdb
import socket
import time
import sys
import getopt
import yaml

from base.connect import ConnnectMysql
from base.listhost import Hostlist


MYSQL_SIZE = {
    'TABLENAME',
    'DATALENGTH',
    'INDEXLENGTH',
    'FREELENGTH'
    }


def fetch_db_size(conn):
    variables = {}
    connectmysql = ConnnectMysql() 
    result = connectmysql.mysql_query(conn, "select concat (table_schema , "." ,TABLE_NAME) TABLENAME , "+
											" Round( DATA_LENGTH) as DATALENGTH, "+
											" round(INDEX_LENGTH) as INDEXLENGTH ," +
											" round(DATA_FREE) as FREELENGTH "+
											" from information_schema.tables "+
											" order by 2 desc ")
    for r in result:
    	if r in MYSQL_SIZE:
    		variables[r] =  i[r]
    return variables


def main():
    error = 0
    try:
        hostlist = Hostlist()
        for v in hostlist.set_hosts_list():
            connectmysql = ConnnectMysql() 
            conn = connectmysql.get_mysql_conn(v)
            mysql_size  = fetch_db_size(conn)

            print mysql_size;

        if error == 0:
            print "Successfull"
        else:
            print str(error) + " errors found"
    except Exception as e:
        print str(e)

if __name__ == "__main__":
    main()

import re
import MySQLdb
import socket
import time
import sys
import getopt
import yaml

from base.connect import ConnnectMysql
from base.listhost import Hostlist


MYSQL_SLAVE_STATUS = {
    'Slave_IO_Running',
    'Seconds_Behind_Master',
    'Slave_SQL_Running',
    }


def fetch_all_slave_status(conn):
    connectmysql = ConnnectMysql() 
    result = connectmysql.mysql_query(conn, "SHOW ALL SLAVES STATUS")
    variables = {}
    if result:
        try:
            for row in result.fetchall():
                for i in row:
                    if i in MYSQL_SLAVE_STATUS:
                        variables[i] =  row[i]
        except Exception as e:
            print str(e)
    return variables


def parse_all_slave_status():
    error = 0
    try:
        hostlist = Hostlist()
        for v in hostlist.set_hosts_list():
            print "Checking server: " + v
            connectmysql = ConnnectMysql() 
            conn = connectmysql.get_mysql_conn(v)
            slave_status  = fetch_all_slave_status(conn)
            if not slave_status["Slave_IO_Running"]:
                print "server: " + v + " has Slave_IO_Running " + str( slave_status["Slave_IO_Running"]) 
                error += error
            if slave_status["Seconds_Behind_Master"] > 15:
                print "server: " + v + " has Seconds_Behind_Master: " + str(slave_status["Seconds_Behind_Master"]) 
                error += error
            if not slave_status["Slave_SQL_Running"]:
                print "server: " + v + " Slave_SQL_Running" + slave_status["Slave_SQL_Running"]
                error += error

        if error == 0:
            print "Successfull"
        else:
            print str(error) + " errors found"

    except Exception as e:
        print str(e)


if __name__ == "__main__":
    parse_all_slave_status()

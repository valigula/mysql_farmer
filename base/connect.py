import re
import MySQLdb
import socket
import time
import sys
import getopt
import yaml

class ConnnectMysql:

	@staticmethod	
	def get_mysql_conn(host):
		mysql_config = {
		'Host': 'local',
		'Port': 3306,
		'User': '',
		'Password': '',
		'Db': '',
		}

		try:
			ConnnectMysql.set_mysql_config(mysql_config)

			return MySQLdb.connect(
				host=host,
	            port=mysql_config["Port"],
	            passwd=mysql_config["Password"],
	            db=mysql_config["Db"],
	            user=mysql_config["User"],
	            )
			print  "get_mysql_conn successfull"
		except Exception as e:
			print "Error get_mysql_conn: " + str(e)


	@staticmethod	
	def set_mysql_config(mysql_config):
	    try:
	        stream = open("config.yml", "r")
	        docs = yaml.load_all(stream)
	        for doc in docs:
	            for section, parameter in doc.items():
	                mysql_config["Port"] = doc['security']["port"]
	                mysql_config["User"] = doc['security']["user"]
	                mysql_config["Password"] = doc['security']["password"]
	                mysql_config["Db"] = doc['security']["db"]
	        #return mysql_config
	    except Exception as e :
	        print "Error >>> set_mysql_config param not found "
	        print "Exception " + str(e)
	        sys.exit(2)


	def mysql_query(self, conn, query):
		cur = conn.cursor(MySQLdb.cursors.DictCursor)
		cur.execute(query)
        	return cur
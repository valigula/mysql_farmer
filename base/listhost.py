import re
import MySQLdb
import socket
import time
import sys
import getopt
import yaml

class Hostlist():
	def set_hosts_list(self):
	    stream = open("config.yml", "r")
	    docs = yaml.load_all(stream)
	    host_var = {}
	    for doc in docs:
	        for section, parameter in doc.items():
	            host_var = doc['host']
	    return host_var
#
# pip install mysql.connector.python
# and: https://dev.mysql.com/doc/connector-python/en/
# and: https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html
#
# docker API:
# https://docker-py.readthedocs.io/en/stable/index.html
#

import docker
import mysql.connector
import time
from datetime import datetime

def get_container(container_name):
    return client.containers.get(container_name)

def get_status(container_name):
    return get_container(container_name).status

def log(msg):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + ' - ' + msg)

client = docker.from_env()
container_name = 'imdb_test'

print('')
log('starting container ' + container_name)

get_container(container_name).start()
while get_status(container_name) != 'running':
    log('waiting for container')
    time.sleep(1)

log('container started')
mysqld_is_running = False

while not mysqld_is_running:
    # get a JSON object with running process info:
    result = get_container(container_name).top(ps_args='-o pid,comm')
    # see if mysqld is in the list:
    for proc in result["Processes"]:
        # proc example: ['8949', 'mysqld']
        if proc[1] == 'mysqld':
            mysqld_is_running = True
        else:
            log('waiting for mysqld')
        time.sleep(1)
log('mysqld is running')

connect_args = {
    'user': 'user', 
    'password': 'pass',
    'host': 'localhost',
    'port': 3376,
    'database': 'imdb'
}

cnx = mysql.connector.connect(**connect_args)
cursor = cnx.cursor(prepared=True)
log('fetching query results:\n')
sql = "SELECT * FROM imdb.language WHERE language_name like %s"
cursor.execute(sql, ("F%",)) # comma needed for 1-item tuple

for (language_id, language_name) in cursor:
    print(language_id + " - " + language_name)


#with open('step_2_insert_master_data.sql', encoding='utf-8', mode='r') as f:
#    cursor.execute(f.read(), multi=True)


cursor.close()
cnx.close()

print('')
log('finished')
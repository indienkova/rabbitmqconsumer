#! /usr/bin/python

import pika
import pandas as pd
import json
import subprocess

credentials = pika.PlainCredentials(username='indienkovaa', password='123456')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='84.201.161.33', port=5672, credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='demo-queue')

file_name = 'demo.parquet'
path = '/home/hadoopuser/hdfs/namenode/parquet/'
global count
count = 0


def run_cmd(args_list):
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return = proc.returncode
    return s_return, s_output, s_err


def callback(ch, method, properties, body):
    global count
    json_data = json.loads(body.decode("utf-8"))
    df = pd.DataFrame(json_data, index=[0])
    df.to_parquet(path + file_name + str(count))
    (ret, out, err) = run_cmd(['hdfs', 'dfs', '-put', '-f', path + file_name + str(count), '/user/hadoopuser/parquet'])
    print('done:' + str(count))
    count += 1


channel.basic_consume('demo-queue', callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

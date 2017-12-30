#!/usr/bin/python

from multiprocessing import Pool, TimeoutError
import multiprocessing
import subprocess

__author__ = 'perevera'

# hosts = ['www.elpais.es', 'www.perevera.cat', 'www.meteo.cat', 'www.linkedin.com', 'www.paypal.com', '232.22.31.123']
hosts = ['www.elpais.es', 'www.meteo.cat', 'www.linkedin.com', 'www.paypal.com', 'www.aiguesdebarcelona.cat',
         'lema.rae.es']

results = []

TIMEOUT_CONNECT = 10


def ping(h):

    # print "DEBUG: Pinging %s" % hosts[h]

    ret = 'nok'

    # cmd = ['ping', host, '-c', '1', '-W', '2']
    cmd = ['ping', hosts[h], '-c', '1', '-W', '20']
    # Linux Version p = subprocess.Popen(['ping', hosts[h], '-c', '1', '-W', '20'])
    # The -c means that the ping will stop afer 1 package is replied and the -W 20 is the timelimit
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # print stdout

    if 'bytes from' in stdout:
        ret = 'ok'

    return hosts[h], ret


def log_result(res):
    # This is called whenever ping(h) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    # print "DEBUG: I'm at the callback function"
    # print res
    results.append(res)


if __name__ == '__main__':

    print "DEBUG: Number of CPUs: %d" % multiprocessing.cpu_count()

    pool = Pool(processes=multiprocessing.cpu_count())
    # results = pool.map(ping, range(1, len(hosts)))

    tasks = []

    for i in range(len(hosts)):
        # pool.apply_async(ping, args=(i,), callback=log_result)
        tasks.append(pool.apply_async(ping, args=(i,), callback=log_result))

    for i in range(len(hosts)):
        try:
            tasks[i].get(timeout=TIMEOUT_CONNECT)
        except TimeoutError:
            results.append((hosts[i], 'Connection timeout'))
            # print '{0} timeout'.format(hosts[i])

    for r in results:
        print r

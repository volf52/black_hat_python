#!/usr/bin/env python
"""

@author : 'Muhammad Arslan <rslnrkmt2552@gmail.com>'

"""

import Queue
import threading
import os
import requests

THREADS = 10

target = "http://www.blackhatpython.com"
directory = "/root/Downloads/joomla"
filters = ['.jpg', '.gif', '.png', '.css']

os.chdir(directory)

web_paths = Queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        try:
            req = requests.get(url)
            content = req.content

            print "[%d] => %s" % (req.status_code, path)
        except requests.HTTPError as error:
            #print "Failed %s" % error
            pass

for i in range(THREADS):
    print "Spawning threads: %d" % (i+1)
    t = threading.Thread(target=test_remote)
    t.start()

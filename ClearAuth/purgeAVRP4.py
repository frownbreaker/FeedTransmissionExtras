#!/usr/bin/python

import sys, os
import feedparser
import transmissionrpc
import argparse
import datetime

# Read the torrents on the server...
kc=0
tc=transmissionrpc.Client('192.168.0.221', port=9091, user='fred', password='secret')
t=tc.get_torrents()
for key in t:
#for torrent in tc.items():
        if key.isFinished:
                print ('Removing Seed Complete', key.name)
                tc.remove_torrent(key.id)
        else:
                if key.percentDone == 1:
                        print ('Removing Download Complete', key.name)
                        kc=kc+1
                        tc.remove_torrent(key.id) #Retains data. Torrent is removed



if kc>0:
        sttime = datetime.datetime.now().strftime('%Y%m%d_%H:%M:%S - ')
        le = "Purge run. " + str(kc) +" file(s) removed."
        log = '/root/purgeavroomrp4.log'
        with open(log, 'a') as logfile:
                logfile.write(sttime + le + '\n')

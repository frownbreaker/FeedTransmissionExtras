# FeedTransmissionExtras

These are a few housekeeping scripts for Feedtransmission https://github.com/lupus78/feedtransmission/

List of scripts and use

## checknas.sh
bash script to check NAS mount point is up and remount / wait / reboot as required

## purgetvroom.py
python script to remove completed downloads

## getnewshows.sh
bash script that invokes feedtransmission and pulls down new content from the rss feed 

## Finally once the scripts are working the way you want you might want to setup cron jobs...

#Every 30 mins check the feed, remeber this is a low power SBC so a feed check can take a long time especially if the server is busy and the internet is slow due to active transfers
#Less than 30 mins might mean that a check has not completed before another one has started!
*/30 * * * * /root/getnewshows.sh | while IFS= read -r line; do echo "$(date) $line"; done >> /root/newshows.txt

#Every 15 minutes run a short Python scipt to close completed transfers, this frees up slots and bandwidth for new transfers
*/15 * * * * /usr/bin/python /root/purge-orange-pi.py
*/20 * * * * /usr/bin/python /root/purge-tvroom.py
*/05 * * * * /usr/bin/python /root/purge-loft.py
*/05 * * * * /root/checknas.sh | while IFS= read -r line; do echo "$(date) $line"; done >> /root/naslog.tx


#At 6am every 10 days keep only the most recent 100 lines of file automatically added by the call to feedtransmission
0 6 */10 * * tail -100 /root/addeditems.txt > /root/short.txt && rm /root/addeditems.txt && mv /root/short.txt /root/addeditems.txt

#At 6am every day keep only the most recent 1000 lines of file automatically added by the call to feedtransmission
00 06 * * * tail -1000 /root/newshows.txt > /root/shortdlp.txt && rm /root/newshows.txt && mv /root/shortdlp.txt /root/newshows.txt
30 09 * * * tail -1000 /root/purgeloft.log > /root/shortpll.txt && rm /root/purgeloft.log && mv /root/shortpll.txt /root/purgeloft.log

#Bounce the transmission server daily as it seems to go dead? Need for low memory system like the Orange Pi One 
#1 4 * * * sudo service transmission-daemon start
#0 4 * * * sudo service transmission-daemon stop
0 4   *   *   *    /sbin/reboot



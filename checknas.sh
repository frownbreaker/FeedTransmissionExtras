if [ ! -d "/media/windowsshare/recordings" ]; then
	# Control will enter here if $DIRECTORY doesn't exist.
	echo "Can't see Windows recording directory. Stopping Transmission.."
	sudo service transmission-daemon stop
	echo "Running mount -a .."
	sudo mount -a
	echo "Sleeping 20s"
	sleep 20
	if [ ! -d "/media/windowsshare/recordings" ]; then
		echo "mount -a did not work rebooting"
		reboot
	else
		echo "mount -a worked no need to reboot. Restarting Transmission.."
		sudo service transmission-daemon start
	fi
#else
#	echo "/media/windowsshare/recordings is mounted -Seems good"
fi


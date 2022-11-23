# nts-tracklist-pirate
NTS Radio tracklist for the pennyless

Depends on songrec (should be accessible globally). Only runs on linux. Uses /tmp.

Launch using ```python nts-tracklist-pirate.py```

To launch periodically, use a cron task (you could also start the script via systemd) :
```
* * * * * /usr/bin/python3 /home/.../nts-tracklist-pirate.py
```

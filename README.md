# kancolle-event-prep
Quite a bit late to release, but here's a quick script to see how prepared your fleet is for the upcoming winter 2018 event. 

Example output:

![Example Output](https://i.imgur.com/I3C1okQ.jpg)

# WARNING
This script was written very quickly and hasn't been thoroughly tested. I've ran it on a few KC3Kai exported profiles, but I make no guarantee that it'll work.

**If you plan to host the server and make it accessible for others to use (*bless your soul*) please keep this in mind!**

# REQUIREMENTS
Packages: `Pillow Flask`

`Flask` is only required if you're planning on running the web server.

# USAGE
First you need to export your KC3Kai profile. This can be done by visiting the strategy room and selecting "Export basic profile". After that you have two options.

1 - CLI:

`python event_prep.py "path_to_kc3kai_profile.kc3"`

The script will save the resulting image in the same directory as the kc3kai profile you provided.

2 - (Minimal) Web Interface:

`python web.py flask run`

After that you can access the web interface at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) Simply upload your KC3kai profile (the exported .kc3 file) to the server and you will be redirected to the exported image.

# NOTES
The script was written and tested using Python 3.6, but it *should (?)* run on some other Python 3.X versions.

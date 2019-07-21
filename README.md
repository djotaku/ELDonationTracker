If you find this useful, please consider donating to my Extra Life campagin: http://extralife.ericmesa.com -> I modify this each year to point to my latest campaign.


Note these videos are up to date for the master branch, not the devel branch. See the text instructions below

To watch a video of how to use this program on Linux: https://youtu.be/sKaFQPoQeJw otherwise read below

To watch a video of how to use this program on Windows: https://youtu.be/hN94aPcEFng 

# Setup
First you should edit the values in participant.conf

Note:

- The values to the right of the : should be in quotation marks.
- if you're not in a team, the TeamID should be set to null without quotation marks.

# To run

On Linux you should be able to either do ./extrlifedonations.py (although you may need to change the path in the #! line) or 

python3 extralifedonations.py

On Windows, see the video above for how to run it.

# Web GUI

If you want a webpage you can use as a GUI to do a sanity check on what should be in the donation files, first change the folder at the end in the __main__ section (this should be the same folder you're using for the text files). Then run

python createHTML.py 

Then open mainpage.html at the folder you told it to use. It should update every 15 seconds.

(Currently web page creation is still python 2)

tracker.html part still needs a little work.

# Support

If you want support for other configurations, please open an issue.

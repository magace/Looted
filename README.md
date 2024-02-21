**Looted.py**

Discord item logger for GIF BOT!

The base code was ripped from Tom and converted to Python.  Thanks, Tom!

The game assets were provided by Blizzhackers here: https://github.com/blizzhackers/d2data

The images are hosted here https://github.com/blizzhackers/ItemScreenshot/tree/master/assets/gfx

The goal is to attempt to find the gfx code for whatever items we find then match it to BH image repo and use that link as the image.


**How does it work?**
- Detect any new items in Looted folders.
- Extracts the item's name and attempts to match it for exact matches.  "uniques, gems, runes..."
- If it fails to detect by name it attempts to search by item type. "rares, magic items, runewords..."
- Checks if the item code is an exceptional or elite base if so it maps it down to the normal base (BH only has images for normal bases)
- One last check to see if the item code is on BH before posting to Discord.


**How to set up?**
- Install Python https://www.python.org/downloads/
- I highly recommend installing Visual Studio  Code and the MS Python extension too so you can run it from inside VC: https://code.visualstudio.com/download
- Open a new command prompt or terminal inside visual code and type "pip install requests".
- Download Looted.zip and extract the files somewhere.
- Open and edit config.json.  Here you will need to enter your discord webhook and D2RB path.  clear_logs will delete all the bot's logs on startup.  sleep_seconds is how long to wait before checking folders for new items.
- Run Looted.py I run it from inside visual code by hitting CTRL + f5  you can also install pyinstaller to create a .exe if you want.


**Known issues and what next?**
- Not all items are mapping.  I just started using this so I am still learning how everything works.
- Find new images for d2r uniques and sets.
- Finish detecting where items are found.  I will create a new branch for that.
- Finding pickit line for items found.  Like I said I'm new to GIF but at first glance, it looks like it could "possibly" be done.


**Images**

![image](https://github.com/magace/Looted/assets/7795098/1f72a0fa-8c16-44ad-8280-41bc0e985131)


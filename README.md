# Bad Apple Discord Bot

[![Bad Apple discord bot](https://img.youtube.com/vi/PLP9c0Z4Q3Y/0.jpg)](http://www.youtube.com/watch?v=PLP9c0Z4Q3Y)

This bot uses discord to display bad apple via text as seen in [this](https://www.youtube.com/watch?v=PLP9c0Z4Q3Y) youtube video.

Dependencies: 
- riposte==0.4.1
- discord==1.0.1
- Pillow==8.1.0

## Install

To install the  dependencies simply run: 
```
python3 -m pip install -r requirements.txt
```

To run the main python file, cd into your directory, then run:
```
python3 bad_apple.py
```

## Usage

NOTE: You need to have a discord bot token, please get this from (https://discord.com/developers/docs/topics/oauth2)[https://discord.com/developers/docs/topics/oauth2]
If you don't know how to add bot to server, refer to (this)[https://discordjs.guide/preparations/adding-your-bot-to-servers.html#bot-invite-links] article. 

After running `python3 bad_apple.py` you should be greated by the banner. 

Type `help` for the commands avalible.
Type `setup` to extract frames from `bad_apple.mp4`. NOTE: This only has to be done once. 
Type `run` to start the bot. 

## Developement 

If your are trying to add new features to this or you wish to not have to manully enter in the bot token, simply comment out line 64 - 68

```
try:
    Token = input("Discord Bot Token: ") # Remove this if you want to permanently add your token.
except:
    print("This is required, please refer to the readme for instructions.")
    exit()
```

and change line 119 from:

```
client.run(Token)#<--- replace Token with your bot token here
```
to
```
client.run(YOUR_DISCORD_BOT_TOKEN)#<--- replace Token with your bot token here
```
## Improvements Needed

- [ ] Fix openCV bug which causes error message when extracting frames 
- [ ] Inform user when `run()` has failed
- [ ] Store discord token in a seperate file (so it does not need to be asked everytime)
- [ ] Make compatible with any video
- [ ] Improve speed of discord messages sent



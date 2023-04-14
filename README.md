# RTN-Widgets-Addition
Add the basic RTN Widgets to another subreddit.  
The account that runs this script must be a moderator in the subreddit.  

### Instructions
- Ensure you have Python installed on your system. You can download it here https://www.python.org/downloads/ (Add to PATH during the installation).
- Download the ZIP file of this repo (Click on ```Code``` -> ```Download ZIP```).
- Open your command prompt and change your directory to where you unzipped the files.
- Install the PRAW package ```pip install praw```.
- Create a Reddit App (script) at https://www.reddit.com/prefs/apps/ and get your ```client_id``` and ```client_secret```.
- Edit the ```config.ini``` file with your details.
- Run the program ```python main.py```.

## Extra Info
Right now, you have to run the script twice to move the widget of links to the top of the widget list.  
If you don't mind where that widget is positioned, then run the script just once per sub.

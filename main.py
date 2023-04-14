import configparser
import praw
import prawcore
    
config = configparser.ConfigParser()
config.read('config.ini')

client_id = config['REDDIT']['CLIENT_ID']
client_secret = config['REDDIT']['CLIENT_SECRET']
password = config['REDDIT']['PASSWORD']
username = config['REDDIT']['USERNAME_REDDIT']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    username=username,
    user_agent='Subreddit Transfer Script v1.0 by ARandomBoiIsMe'
)

def main():
    to_subreddit_name = config['VARS']['TO_SUBREDDIT']

    to_subreddit = validate_subreddit(to_subreddit_name)
    if to_subreddit == None:
        print(f"This subreddit does not exist: r/{to_subreddit_name}")
        exit()

    if to_subreddit.user_is_moderator == False:
        print(f"You must be a mod in this sub to add widgets: r/{to_subreddit_name}")
        exit()

    add_widgets(to_subreddit)

    rearrange_widgets(to_subreddit)

def validate_subreddit(subreddit_name):
    if subreddit_name.strip() == '':
        return None
    
    try:
        return reddit.subreddits.search_by_name(subreddit_name, exact=True)[0]

    except prawcore.exceptions.NotFound:
        return None

def add_widgets(to_sub):
    widget_moderation = to_sub.widgets.mod

    #Gets main text widget from owner's sub and moves it immediately to the other sub.
    for widget in reddit.subreddit("PrivateVault2112").widgets.sidebar:
        if isinstance(widget, praw.models.TextArea) and widget.shortName == 'Part of the RisingTide Network':
            text = widget.text
            shortName = widget.shortName
            styles = {"backgroundColor": "", "headerColor": ""}

            if widget_exists_in_sub(to_sub, widget) == True:
                widget.mod.update(text=text)
                print(f'Widget content updated - {widget.shortName}')
                break

            widget_moderation.add_text_area(
                short_name=shortName, text=text, styles=styles
            )
            print(f'Widget added - {widget.shortName}')
            break

    widgets = to_sub.widgets.sidebar
    community_list_exists = False
    for widget in widgets:
        if widget.shortName == "A Few Other RisingTide Subs":
            community_list_exists = True
            print(f"The 'Other RisingTide Subs' community list already exists here - {to_sub.display_name}")
            break

    if community_list_exists == False:
        styles = {"backgroundColor": "", "headerColor": ""}
        widget_moderation.add_community_list(
            short_name="A Few Other RisingTide Subs", data=['CelebsWithPetiteTits'], styles=styles
        )
        print('Community list added - A Few Other RisingTide Subs')

def widget_exists_in_sub(subreddit, sub_widget):
    widgets = subreddit.widgets.sidebar
    for widget in widgets:
        if sub_widget.shortName == widget.shortName:
            return True
    
    return False

def rearrange_widgets(subreddit):
    widgets = list(subreddit.widgets.sidebar)
    widget_order = []

    #The for-loops below ensure that the 'Part of the RisingTide Network' TextArea Widget
    #appears on the first available space after the IDCard Widget on the sidebar at all times.
    for widget in widgets:
        if widget.shortName == 'Part of the RisingTide Network':
            widget_order.append(widget)
            break

    for widget in widgets:
        if widget.shortName == 'Part of the RisingTide Network':
            continue

        widget_order.append(widget)

    try:
        subreddit.widgets.mod.reorder(widget_order)
        print('Widgets rearranged. Links moved to the top.')
    except praw.exceptions.RedditAPIException:
        print('Please run the script again to move the links to the top.')

main()
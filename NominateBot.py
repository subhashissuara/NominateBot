# ------------------------------------------
# Writtern by Subhashis Suara / QuantumBrute
# ------------------------------------------

from psaw import PushshiftAPI
import praw
import time
import json
import re

# --------------------------------------------------------------------------------

subreddit_name = 'jschlatt' # Mention the subreddit that bot should work on
limitno = 30000 # Set the maximum number of posts to get in the given timeframe
end_epoch=int(time.time()) # Current time
start_epoch=int(end_epoch - (60*60*24*8)) # Current time - the amount you mention in seconds

#---------------------------------------------------------------------------------

print("Starting Bot...")

reddit = praw.Reddit(client_id= ' ',         
					 client_secret= ' ',
					 username= ' ',
					 password= ' ',
					 user_agent= 'Created by u/QuantumBrute') # Login to reddit API

api = PushshiftAPI() # Variable to use the PushShiftAPI
subreddit = reddit.subreddit(subreddit_name)

print("From: "+ str(start_epoch))
print("Till: "+ str(end_epoch))


result = list(api.search_submissions(after=start_epoch, 
                                    before=end_epoch,
                                    subreddit=subreddit_name,
                                    filter=['author', 'id'],
                                    limit=limitno)) # Gets the data with the parameters mentioned from PushShift and makes it into a list


def nominate():
    print("Opening database...")
    with open('UserDatabase.txt', 'r') as infile: # Opens the database
        info = json.load(infile,)
    
    print("Going through posts & comments for !nominate...")

    data = []

    for b in range(len(info)): # Copies the database to a list named data to make it easier to modify the elements of the database
        data.append(info[b])

    post_ids = []
    reply_to_nomination = "Nominated for +1 SchlattCoin!" # Reply that bot will post

    for i in range(len(result)): 
        post_ids.append(result[i].id) # Gathers the ids of all posts in given time frame

    post_ids_size = len(post_ids)
    template = '2d073f42-677a-11e9-8b58-0e9db0a8f550' # Template ID of custom flair

    for j in range(post_ids_size):
        submission = reddit.submission(post_ids[j])
        submission.comments.replace_more(limit=None)
        author = result[j].author

        for comment in submission.comments.list(): # Goes through comments of post; Note: .list() is used to flatten all hierarchy of comments into a single list
            if comment.author == author or comment.saved: # Checks for post author's comments and other saved comments to avoid re running of commands
                continue
            else:
                keyword = re.search("!nominate", comment.body) # Searches for !nominate in the comment
                if keyword: # Whole process of replying, saving and setting the flairs
                    print(str(comment.author) + " has nominated " + str(author) + "!")
                    comment.save()
                    comment.reply(reply_to_nomination)
                    flag = 0
                    for a in range(len(data)):
                        if author == data[a].get("Name"):
                            print(str(author) + " found in database!")
                            print("Sending reply and setting flair...")
                            flag = 1
                            coins = data[a].get("SchlattCoins") 
                            coins += 1
                            data[a].update({'SchlattCoins' : coins}) 
                            flair = next(reddit.subreddit(subreddit_name).flair(author))
                            if flair.get('flair_text') == None:
                                newflair = (str(coins) + " SchlattCoins")
                                subreddit.flair.set(author, newflair)
                            else:
                                flair_split = flair.get('flair_text').split()
                                for c in range(len(flair_split)):
                                    if flair_split[c] == "SchlattCoins":
                                        c -= 1
                                        flair_split[c] = str(coins)
                                        newflair = ' '.join(flair_split)
                                        if author == "jschlattAlt":
                                            subreddit.flair.set(author, text = newflair, flair_template_id = template)
                                        else:    
                                            subreddit.flair.set(author, newflair)
                                        break
                                    else:
                                        newflair = (str(flair.get('flair_text')) + " ( " + str(coins) + " SchlattCoins" + " )")
                                        subreddit.flair.set(author, newflair)   
                            break

                    if flag == 0:
                        flair = next(reddit.subreddit(subreddit_name).flair(author))
                        item_to_add = { "Name" : str(author), "SchlattCoins" : 1}
                        data.append(item_to_add)
                        if flair.get('flair_text') == None:
                                newflair = (str(1) + " SchlattCoin")
                                subreddit.flair.set(author, newflair)
                        else:
                            flair_split = flair.get('flair_text').split()
                            for c in range(len(flair_split)):
                                if flair_split[c] == "SchlattCoin":
                                    c -= 1
                                    flair_split[c] = str(1)
                                    newflair = ' '.join(flair_split)
                                    subreddit.flair.set(author, newflair)
                                else:
                                    newflair = (str(flair.get('flair_text')) + " ( " + str(1) + " SchlattCoin" + " )")
                                    subreddit.flair.set(author, newflair)
    
    with open('UserDatabase.txt', 'w') as outfile: # Overwites the JSON file with updated data
        json.dump(data, outfile, indent=2)
        print("Database updated successfully!")


    
def main():
    nominate()

if __name__ == '__main__':
    main()
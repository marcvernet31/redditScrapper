import praw
import pprint
import pandas as pd
from datetime import datetime

import argparse
import time

from auxiliar import toTimestamp, save, load_DataFrame
from secrets import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from redditScrap import retrieveComments, retrievePosts

"""
PER FER:
    - Comentar tot ben bonic
    
COSES DEL FUTUR:
    - Poder filtrar per temps, incorporar el temps al nom del fitxer
    - Permetre entrar un enllaç web i descarregar tots els comentaris del post
"""



# Flags for teriminal usage
parser = argparse.ArgumentParser()
parser.add_argument("-rl", "--replaceLimit", help="Number of returned batches for each comment forest")
parser.add_argument("-c", "--getComments", help="False: don't save the comments (True: default)")
parser.add_argument("-csort", "--commentSort", help="'best', 'new', 'controversial'; ways of sorting comments(default: best)")
parser.add_argument("-cret", "--commentsRetrieved", help="Number of root posts for retrieved for each submission")
parser.add_argument("-u", "--update", help="True to update a data file")
parser.add_argument("-sf", "--savingFrequency", help="Size of batches to be saved")


args = parser.parse_args()

# Parametres dels flags
def flag_parameters():
    if args.replaceLimit: replaceLimit = args.replaceLimit
    else: replaceLimit = 1

    if args.getComments:
        getComments = args.getComments
    else: getComments = 1

    if args.commentSort: commentSort = args.commentSort
    else: commentSort = "best"

    if args.commentsRetrieved: commentsRetrieved = args.commentsRetrieved
    else: commentsRetrieved = 500

    if args.update:
        update = args.update
    else: update = 0

    if args.savingFrequency: savingFrequency = args.savingFrequency
    else: savingFrequency = 10

    return replaceLimit, getComments, commentSort, commentsRetrieved, update, int(savingFrequency)


def main():

    replaceLimit, getComments, commentSort, commentsRetrieved, update, savingFrequency = flag_parameters()
    isRetrieved = dict()


    print("------------------------------------------")
    input_subreddit = input("Enter Subreddit to search: ")
    submissionsRetrieved = input("Enter number of Submissions to retireve: ")

    try:
        submissionsRetrieved = int(submissionsRetrieved)
    except ValueError:
        print("Error: Not a number")
        submissionsRetrieved = input("Enter number of Submissions to retireve: ")
        submissionsRetrieved = int(submissionsRetrieved)

    if update:
        postPath = input("Path of the post file: ")
        commentPath = input("Path of the comment file: ")

        try:
            tmp_dfPost = load_DataFrame(postPath, "posts")
            tmp_dfComment = load_DataFrame(commentPath, "comments")
            isRetrieved = dict.fromkeys(list(tmp_dfPost["ID"]), True)
        except:
            print("Error with file names")

    print("------------------------------------------")


    reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent= USER_AGENT, check_for_async=False)
    subreddit = reddit.subreddit(input_subreddit)


    start = time.time()
    dfPost, dfComment = retrievePosts(subreddit, submissionsRetrieved, isRetrieved, getComments, commentSort, commentsRetrieved, savingFrequency, replaceLimit)
    end = time.time()

    if update:
        dfPost = dfPost.append(tmp_dfPost)
        dfComment = dfComment.append(tmp_dfComment)

    save(dfPost, f"data/{subreddit.display_name}_posts.csv")
    if getComments: save(dfComment, f"data/{subreddit.display_name}_comments.csv")

    print("------------------------------------------")
    print("Extraction finished, result stored in: ")
    print(f"- Posts: data/{subreddit.display_name}_posts.csv")
    if getComments: print(f"- Comments: data/{subreddit.display_name}_comments.csv")
    if update:
        print(f"{len(dfPost.index)} posts stored, of which {len(dfPost.index) - len(tmp_dfPost.index)} are new")
        print(f"{len(dfComment.index)} comments stored, of which {len(dfComment.index) - len(tmp_dfComment.index)} are new")
    else:
        print(f"{len(dfPost.index)} posts stored")
        print(f"{len(dfComment.index)} comments stored")
    print(f"Execution time: {'%.3f'%(end-start)}s")

if __name__ == '__main__':
  main()

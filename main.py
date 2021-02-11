import praw
import pprint
import pandas as pd

import argparse
import time

from auxiliar import toTimestamp, save, load_DataFrame
from secrets import CLIENT_ID, CLIENT_SECRET, USER_AGENT
from redditScrap import retrieveComments, retrievePosts

"""
Main script for the Reddit Scrapper project.
--------------------------------------------------------------------------------
This script provides a way to download interactively from a terminal posts and
comments from Reddit submissions. The aim and vision of this project is to be
able to easily download massive quantities of text from Reddit for future ML and
data science analysis.


TO BE DONE:
    - Adding the capability to filter by timestamp and updating files by timestamp
    - Adding the capability of inputinc a web link of a Reddit post to download
    its comments.
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

# Definition of flag parameters
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

    # Retrieve values from flags
    replaceLimit, getComments, commentSort, commentsRetrieved, update, savingFrequency = flag_parameters()

    # Dictionary for storing submissions already uploaded
    # (for update functionality)
    isRetrieved = dict()

    # Ask and get user input.
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

    # Initialize Reddit object and specified subreddit
    reddit = praw.Reddit(client_id = CLIENT_ID, client_secret = CLIENT_SECRET, user_agent= USER_AGENT, check_for_async=False)
    subreddit = reddit.subreddit(input_subreddit)

    # Retrieve data from Reddit
    start = time.time()
    dfPost, dfComment = retrievePosts(subreddit, submissionsRetrieved, isRetrieved, getComments, commentSort, commentsRetrieved, savingFrequency, replaceLimit)
    end = time.time()

    # Append to old data in case of update
    if update:
        dfPost = dfPost.append(tmp_dfPost)
        dfComment = dfComment.append(tmp_dfComment)

    # Save final result
    save(dfPost, f"data/{subreddit.display_name}_posts.csv")
    if getComments: save(dfComment, f"data/{subreddit.display_name}_comments.csv")

    # Printing of final results and metrics
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

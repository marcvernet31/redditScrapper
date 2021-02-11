import praw
import pprint
import pandas as pd
from datetime import datetime



from auxiliar import toTimestamp, save, load_DataFrame
from userFunctions import commentSpecs

def retrieveComments(dfInternal, submission, replaceLimit, commentSort, commentsRetrieved):
    submission.comment_sort = commentSort
    submission.comments.replace_more(limit=replaceLimit)
    for comment in submission.comments.list():
        if commentSpecs(comment):
            dfInternal = dfInternal.append(
                pd.Series([
                    str(comment.id),
                    str(comment.body),
                    str(comment.score),
                    str(comment.author),
                    str(comment.is_root),
                    str(toTimestamp(comment.created_utc)),
                    str(submission.id)],
                index = list(dfInternal.columns)),
                ignore_index = True)
    return dfInternal

def retrievePosts(subreddit, submissionsRetrieved, isRetrieved, getComments, commentSort, commentsRetrieved, savingFrequency, replaceLimit):
    dfPost_columns = ['ID', 'Title', 'Text', 'Score', 'UpvoteRatio', 'NumberComents', 'Author', 'Timestamp']
    dfPost = pd.DataFrame(columns = dfPost_columns)

    dfComment_columns = ['ID', 'Text', 'Score',  'Author', 'isRoot', 'Timestamp', 'SubmissionID']
    dfComment = pd.DataFrame(columns = dfComment_columns)

    i = 0
    for submission in subreddit.hot(limit = submissionsRetrieved):
        if(str(submission.id) not in isRetrieved.keys()):
            isRetrieved[submission.id] = True
            dfPost = dfPost.append(
                pd.Series([
                    submission.id,
                    submission.title,
                    submission.selftext,
                    submission.score,
                    submission.upvote_ratio,
                    submission.num_comments,
                    submission.author,
                    toTimestamp(submission.created_utc)],
                index = dfPost_columns),
                ignore_index = True)
            if getComments: dfComment = dfComment.append(retrieveComments(dfComment, submission, replaceLimit, commentSort, commentsRetrieved))
        if i%savingFrequency == 0 and i!=0:
            save(dfPost, f"data/{subreddit.display_name}_posts.csv")
            save(dfComment, f"data/{subreddit.display_name}_comments.csv")
            print(f"Backup copy saved with {i} posts and {len(dfComment.index)} comments")
        i += 1


    return dfPost, dfComment

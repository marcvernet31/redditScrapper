
"""
User functions are functions that by default don't do anything, but can be
modifyed by the end-user.
"""

"""
Conditional value for retrieveComments() function, that decides whether a comment
has to be stored. Can be used for example to filter out very short or low effort
comments, or to just keep comments with a certain word in it.
"""
def commentSpecs(comment):
    # EX.: Just keep comments longer that 50 characters:
        # if len(str(comment.body)) > 50: return True
        # else: return False
    return True

"""
Conditional value for retrievePosts() function, that decides if a post has
to be saved and it's conments explored. Useful to filter posts with little
comments or filter based on the topic of the submission body.
"""
def postSpecs(submission):
    return True

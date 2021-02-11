import pandas as pd
from datetime import datetime


# Covert UNIX timestamp to regular timestamp
def toTimestamp(ts):
    ts = int(ts)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Save pd.DataFrame as .csv
def save(df, filepath):
    df.to_csv(filepath)

# Load stored dataframes (with specified structure)
def load_DataFrame(filepath, kind):
    df = pd.read_csv(filepath, index_col=False)
    del df['Unnamed: 0']

    if kind =="posts":
        if list(df.columns) == list(['ID', 'Title', 'Text', 'Score', 'UpvoteRatio', 'NumberComents', 'Author', 'Timestamp']):
            return df
    elif kind == "comments":
        if list(df.columns) == list(['ID', 'Text', 'Score',  'Author', 'isRoot', 'Timestamp', 'SubmissionID']):
            return df

    else:
        print("Error, structure not matching")

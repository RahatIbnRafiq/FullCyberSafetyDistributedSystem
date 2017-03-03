'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

import DatabaseCodes.mongoOperations as dc
from mediaSession import MediaSession as mediasession
import re
from SentimentExtraction import SentimentExtraction as st

rootpath = "C:\\Users\\RahatIbnRafiq\\workspace\\CyberSafetySystem\\"


def getNewPostsForPrediction():
    toBePredicted = []
    posts = dc.findAllDataFromCollection("CyberSafetyDatabase", "Posts")
    for post in posts:
        if str(post["isPredicted"]) == "no":
            dc.updateIsPredictedFieldPostCollection("yes", "CyberSafetyDatabase", "Posts", post["postId"])
            ms = mediasession(post["postId"],post["userId"])
            postDescription = str(post["description"].encode("utf8"))
            postDescription = re.sub(r'\W+', ' ', postDescription)
            ms.postDescription = postDescription
            ms.likeCount = float(post["likeCount"])
            ms.shareUrl = str(post["shareUrl"])
            toBePredicted.append(ms)
    return toBePredicted





def getUserDescriptionSentiment(userId):
    try:
        user = dc.findUserFromCollection("CyberSafetyDatabase", "Users", userId)[0]
        userDescription = str(user["description"])
        userDescription = re.sub(r'\W+', ' ', userDescription)
        userDescription = str(userDescription.encode("utf-8"))
        sentiment = st(userDescription)
        return sentiment.getSentimentPolarity()
    except Exception:
        return 0.0

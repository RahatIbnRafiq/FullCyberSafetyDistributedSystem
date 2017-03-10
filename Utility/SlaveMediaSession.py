'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

from datetime import datetime 

class SlaveMediaSession:
    def __init__(self,postId):
        self.postId = postId
        self.lastChecked = datetime.now()
        self.cameInTime = datetime.now()
        self.negativeCommentCount = 0.0
        self.negativeWordCount = 0.0
        self.totalCommentCount = 0.0
        self.alertnumber = 0
        #self.lastCheckedInterval = 0.0
        #self.commentsUntilNow = 0


'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

class MediaSession:
    def __init__(self,postId,description,likeCount):
        self.postId = postId
        self.postDescription = description
        self.likeCount = likeCount
        self.priority = -1


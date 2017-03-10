'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer
from numpy import array
from sklearn.utils.extmath import safe_sparse_dot




class CyberSafetyClassifier:
    
    def __init__(self):
        self.rootPath = "C:\\Users\\RahatIbnRafiq\\workspace\\CyberSafetySystem\\"
        #self.predictor = self.LoadPredictor()
        self.theta = array([0.00277109,2.07470053 ,2.06390136])
        self.intercept = array([-0.87839156])
        self.negativeWordDict = dict()
        self.loadNegativeWordList()
        
    def loadNegativeWordList(self):
        f = open("negative-words.txt","r")
        for line in f:
            line = line.strip().lower()
            self.negativeWordDict[line] = 1
        f.close()
    
    def classifyMediaSession(self,slaveMediaSession,commentList):
        featureDictionary =  self.FeatureExtractionIncrementalClassifier(slaveMediaSession,commentList)
        X= self.TransformIntoVectors([featureDictionary])
        score = safe_sparse_dot(X, self.theta.T,dense_output=True) + self.intercept
        if score > -0.5:
            return 1
        else:
            return 0
    
    def TransformIntoVectors(self,totalData):
        v = DictVectorizer(sparse=True)
        X =  v.fit_transform(totalData)
        return X
    
    def FeatureExtractionIncrementalClassifier(self,slaveMediaSession,commentList):
        
        negative_comment_count = 0
        negative_word_count = 0.0
        
        for comment in commentList:
            slaveMediaSession.totalCommentCount += 1
            is_negative_comment = 0
            comment = comment.strip().lower()
            words = comment.split(" ")
            for word in words:
                if word in self.negativeWordDict.keys():
                    is_negative_comment = 1
                    negative_word_count += 1
                negative_comment_count += is_negative_comment
        
        slaveMediaSession.negativeCommentCount += negative_comment_count
        if slaveMediaSession.totalCommentCount > 0:
            negativeCommentPercentage = (slaveMediaSession.negativeCommentCount / slaveMediaSession.totalCommentCount)
        else:
            negativeCommentPercentage = 0
        slaveMediaSession.negativeWordCount  += negative_word_count
        
        if slaveMediaSession.negativeCommentCount > 0:
            negativeWordPerNegativeComment = (slaveMediaSession.negativeWordCount/slaveMediaSession.negativeCommentCount)
        else:
            negativeWordPerNegativeComment = 0
        
        featureDictionary = defaultdict(int)
        featureDictionary["negativeCommentCount"] = slaveMediaSession.negativeCommentCount
        featureDictionary["negativeCommentPercentage"] = negativeCommentPercentage
        featureDictionary["negativeWordPerNegativeComment"] = negativeWordPerNegativeComment
        return featureDictionary
        
                    
            
            
        
    
    

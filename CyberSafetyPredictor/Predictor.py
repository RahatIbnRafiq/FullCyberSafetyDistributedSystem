'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

from collections import defaultdict
from csv import DictReader
from sklearn.feature_extraction import DictVectorizer
from numpy import array
from sklearn import linear_model
from sklearn import cross_validation
from Utility.SentimentExtraction import SentimentExtraction as st




class CyberSafetyPredcitor:
    
    def __init__(self):
        self.rootPath = "C:\\Users\\RahatIbnRafiq\\workspace\\CyberSafetySystem\\"
        #self.predictor = self.LoadPredictor()
        self.theta = array([-7.55733918e-01,1.57389476e-01,-2.14181572e-04])
        self.intercept = array([0.5678278])
        
        
        
    def getPriorityLabels(self,tag,confidence):
        if tag == "bullying":
            return 1
        elif tag == "noneBll":
            return 2
        return 1
    
    
    def FeatureExtractionPrediction(self,mediaSession):
        featureDictionary = defaultdict(int)
        sentiment = st(mediaSession.postDescription)
        featureDictionary["postDescriptionPolarity"] = float(1.0- float(sentiment.getSentimentPolarity()))
        featureDictionary["postDescriptionSubjectivity"] = float(1.0- float(sentiment.getSentimentSubjectivity()))
        featureDictionary["postLikeCount"] = float(mediaSession.likeCount)
        
        return featureDictionary
    
    
    def TransformIntoVectorsPrediction(self,totalData):
        v = DictVectorizer(sparse=True)
        
        X =  v.fit_transform(totalData)   
        
        return X
    
    def startPrediction(self,mediaSession):
        featureDictionary =  self.FeatureExtractionPrediction(mediaSession)
        X= self.TransformIntoVectorsPrediction([featureDictionary])
        h = X.dot(self.theta.T)+self.intercept
        return 1 if h < 0 else 2
        
    
    def FeatureExtraction(self,data):
        featureDictionary = defaultdict(int)
        featureDictionary["postDescriptionPolarity"] = float(1.0- float(data["postDescriptionPolarity"]))
        featureDictionary["postDescriptionSubjectivity"] = float(1.0- float(data["postDescriptionSubjectivity"]))
        featureDictionary["postLikeCount"] = float(float(data["postLikeCount"]))
        return featureDictionary
        
    def SplitIntoTestTrainingDataset(self,filename):
        total_data = DictReader(open(filename, 'Ur'))
        totalData = []
        totalLabel = []
        bullyCount = 0
        notBullyCount = 0
        for ii in total_data:
            tag = str(ii["question2"])
            confidence = float(str(ii["question2:confidence"]))
            if confidence <= 0.6:
                continue
            if tag == "noneBll":
                notBullyCount += 1
                if notBullyCount > 179:
                    continue
            else:
                bullyCount += 1
            featureDictionary = self.FeatureExtraction(ii)
            totalData.append(featureDictionary)
            totalLabel.append(self.getPriorityLabels(tag,confidence))
        return (totalData,totalLabel)
    
    def TransformIntoVectors(self,totalData,totalLabel):
        v = DictVectorizer(sparse=True)
        
        X =  v.fit_transform(totalData)   
        Y = array(totalLabel)
        
        return (X,Y)
    
    def fittingClassifier(self,classifier,X,Y,X_test,Y_test):
        clf = classifier[0]
        clf.fit(X, Y)
        return clf
        
    def LoadPredictor(self):
        totalData,totalLabel = self.SplitIntoTestTrainingDataset(self.rootPath+"Data\\vine_meta_data.csv")
        X,Y = self.TransformIntoVectors(totalData,totalLabel)
        X = X.todense()
        
        classifierList = []
        classifierList.append((linear_model.LogisticRegression(),"LogisticRegression"))
        
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.4, random_state=0)
    
        for classifier in classifierList:
            clf = self.fittingClassifier(classifier,X_train,y_train,X_test,y_test)
            return clf
        
    
    

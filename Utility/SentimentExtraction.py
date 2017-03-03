'''
Created on Nov 11, 2016

@author: RahatIbnRafiq
'''

from textblob import TextBlob


class SentimentExtraction:
    text = ""
    sentiment = None
    blob = None
    
    def __init__(self,text):
        self.text = text
        self.blob = TextBlob(self.text)
        
    def getSentimentPolarity(self):
        return self.blob.sentiment.polarity
    def getSentimentSubjectivity(self):
        return self.blob.sentiment.subjectivity

'''
Created on Mar 9, 2017

@author: RahatIbnRafiq
'''
from Classifier import CyberSafetyClassifier as Classifier
import databaseCodes.mongoOperations as mo
from datetime import datetime
import random

classifier = None
epoch = datetime.utcfromtimestamp(0)
neg_comments = ["you suck","what an idiot","i hope you die","what an idiot","stupid idiot","asshole"]
pos_comments = ["hello there", "how have you been", "nice one", " that was alright", "such a nice day"]


def classifyMediaSessions(list_of_monitoring_media_sessions):
    global classifier
    for media_session in list_of_monitoring_media_sessions:
        if classifier is None:
            classifier = Classifier()
        if random.randint(0,10) < 8:
            result = classifier.classifyMediaSession(media_session, pos_comments)
        else:
            result = classifier.classifyMediaSession(media_session, neg_comments)
        if result == 1:
            f = open("alertdata.txt","a")
            media_session.alertnumber += 1
            timeInterval = (datetime.now() - media_session.cameInTime).total_seconds() 
            f.write(str(media_session.postId)+","+str(media_session.alertnumber)+","+str(timeInterval)+"\n")
            f.close()
        
            
        
        

def gettingCommentsForMediaSession(postid_for_mongo,media_session):
    """global epoch
    before_time = media_session.lastCheckedInterval
    now = datetime.now()
    after_time = (now - epoch).total_seconds() 
    comment_data = mo.findCommentsFromVineSlaveComments("VineDatabase", "VineCommentsForSlaves", postid_for_mongo, before_time, after_time)
    media_session.lastCheckedInterval = after_time
    media_session.lastChecked =  now 
    return comment_data"""
    comment_data = mo.findAllCommentsFromCollection("VineDatabase", "VineCommentsForSlaves", postid_for_mongo)
    return comment_data
    



if __name__ == "__main__":
    print "can't run this script like this."
else:
    classifier = Classifier()
    
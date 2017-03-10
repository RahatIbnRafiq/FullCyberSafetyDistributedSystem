
#import sys
#from CyberSafetyPredictor.Predictor import CyberSafetyPredcitor as CyberSafetyPredictor
#import pika
#import time
import databaseCodes.mongoOperations as mo
#from Utility.mediaSession import MediaSession as MediaSession
from datetime import datetime
import time

import os
import psutil
# this file is for testing different codes

#import databaseCodes.mongoOperations as mo
#from Utility.mediaSession import MediaSession as MediaSession

#from CyberSafetyPredictor.Predictor import CyberSafetyPredcitor as CyberSafetyPredictor
"""


l
DATABASE_NAME = "VineDatabase"
POST_COLLECTION_NAME = "SampledASONAMPosts"

cybersafety_predictor = CyberSafetyPredictor()

slave_status_dictionary = {}

list_of_posts_to_be_predicted = []






databaseName = "VineDatabase"



def predictorTesting():
    cybersafety_predictor = CyberSafetyPredictor()
    postData = mo.findAllDataFromCollection("VineDatabase", "SampledASONAMPosts")
    count = 0
    
    list_of_posts_to_be_predicted = []
    for data in postData:
        try:
            list_of_posts_to_be_predicted.append(MediaSession(data["postId"],data["description"],data["likeCount"]))
            count +=1
        except Exception:
            continue
        
    for post_to_be_predicted in list_of_posts_to_be_predicted:
        post_to_be_predicted.priority =  cybersafety_predictor.startPrediction(post_to_be_predicted)
        
    list_of_posts_to_be_predicted = list_of_posts_to_be_predicted*((8233/len(list_of_posts_to_be_predicted))+1)
    
    print len(list_of_posts_to_be_predicted)
    



def convertDateToMilliseconds(date):
    
    epoch = datetime.utcfromtimestamp(0)
    date_format = "%Y-%m-%dT%H:%M:%S.%f"
    date = datetime.strptime( date, date_format)
    return (date - epoch).total_seconds() 


    
    
def createCommentCollection():
    postData = mo.findAllDataFromCollection(databaseName, "SampledASONAMPosts")
    count = 0
    for post in postData:
        postid = post["postId"]
        commentData =mo.findAllCommentsFromCollection(databaseName, "SampledASONAMComments", postid)
        
        for comment in commentData:
            seconds_passed_until_this_comment = convertDateToMilliseconds(comment["created"]) - convertDateToMilliseconds(post["created"])
            #print postid,comment["commentText"].encode("utf-8"),seconds_passed_until_this_comment
            data = {"postid":postid,
                    "commentText":comment["commentText"].encode("utf-8"),
                    "seconds_passed_until_this_comment":seconds_passed_until_this_comment}
            mo.insertDataInDatabase(databaseName, "VineCommentsForSlaves",data)
        count+=1
        print str(count)+" posts' comments have been inserted."
        


def getComputerStatistics():
    import psutil
    processes = psutil.process_iter()
    for process in processes:
        print process.name,process.memory_info()[0]/(1024.0*1024.0)
        


def cyberSafetyPredictorWorks():
    for post_to_be_predicted in list_of_posts_to_be_predicted:
        post_to_be_predicted.priority =  cybersafety_predictor.startPrediction(post_to_be_predicted)
        print post_to_be_predicted.priority
    return


def loadingMediaSessions():
    
    postData = mo.findAllDataFromCollection(DATABASE_NAME, POST_COLLECTION_NAME)
    for data in postData:
        try:
            list_of_posts_to_be_predicted.append(MediaSession(data["postId"],data["description"],data["likeCount"]))
        except Exception:
            continue


"""

"""def checkingTimeDifferenceCode():
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    return (now - epoch).total_seconds() """



"""def checkcommentIntervalCode():  
    comments = mo.findCommentsFromVineSlaveComments("VineDatabase", "VineCommentsForSlaves",  "1156467652974342144", 0, 100)  
    for comment in comments:
        print comment["commentText"].encode("utf-8")"""
        
if __name__ == "__main__":
    
    while True:
        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / float(2 ** 20)
        print mem
        time.sleep(10)
    print "done"


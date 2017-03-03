
# this file is for testing different codes

import databaseCodes.mongoOperations as mo
from Utility.mediaSession import MediaSession as MediaSession


databaseName = "VineDatabase"



#getting post data from VineDatabase's collection

"""postData = mo.findAllDataFromCollection("VineDatabase", "SampledASONAMPosts")
count = 0
for data in postData:
    try:
        count +=1
    except Exception:
        continue
    
print count  """






# checking if predictor is working

from CyberSafetyPredictor.Predictor import CyberSafetyPredcitor as CyberSafetyPredictor


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
    from datetime import datetime
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
        
if __name__ == "__main__":
    getComputerStatistics()
    print "done"


import sys


"""
variable to decide which system to run. 
0: round robin scheduler, everything in memory (default)
1: scheduler, everything in memory
"""
WHAT_SYSTEM_TO_RUN = 0
DATABASE_NAME = "VineDatabase"
POST_COLLECTION_NAME = "SampledASONAMPosts"

list_of_posts_to_be_predicted = []

def loadingCyberSafetyPredictor():
    return

def loadingMediaSessions():
    import databaseCodes.mongoOperations as mo
    from Utility.mediaSession import MediaSession as MediaSession
    postData = mo.findAllDataFromCollection(DATABASE_NAME, POST_COLLECTION_NAME)
    for data in postData:
        try:
            list_of_posts_to_be_predicted.append(MediaSession(data["postId"],data["description"],data["likeCount"]))
        except Exception:
            continue
    return list_of_posts_to_be_predicted
    
def startRunningMaster():
    loadingMediaSessions()
    print len(list_of_posts_to_be_predicted)
    return
        



if __name__ == "__main__":
    master_run_arguments = sys.argv
    if len(master_run_arguments) == 1:
        print "running default round robin everything in memory system"
        WHAT_SYSTEM_TO_RUN = 0
        startRunningMaster()
    else:
        if master_run_arguments[1] == "help":
            print "python master.py argument"
            print "0: round robin scheduler, everything in memory (default)"
            print "1: scheduler, everything in memory"
            
        else:
            if master_run_arguments[1] == '0':
                print "running round robin everything in memory system"
                WHAT_SYSTEM_TO_RUN = 0
            elif master_run_arguments[1] == '1':
                print "running scheduler, everything in memory"
                WHAT_SYSTEM_TO_RUN = 1
            startRunningMaster()
    print "master is exiting ..."
            
else:
    print "You can't run master as a module. Please run master.py help to check the usage of the master script."
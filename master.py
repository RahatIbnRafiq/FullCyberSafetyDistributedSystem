
import sys
from CyberSafetyPredictor.Predictor import CyberSafetyPredcitor as CyberSafetyPredictor
import pika
import time
import databaseCodes.mongoOperations as mo
from Utility.mediaSession import MediaSession as MediaSession

cybersafety_predictor = CyberSafetyPredictor()

slave_status_dictionary = {}

list_of_posts_to_be_predicted = []

"""
variable to decide which system to run. 
0: round robin scheduler, everything in memory (default)
1: scheduler, everything in memory
"""

WHAT_SYSTEM_TO_RUN = 0
DATABASE_NAME = "VineDatabase"
POST_COLLECTION_NAME = "SampledASONAMPosts"

USERNAME = "test"
PASSWORD = "test"
IP_LOCALHOST = "128.138.244.39"
STATUS_QUEUE = "status"
counter = 1




class CountCallback(object):
    def __init__(self, count,connection):
        self.count = count
        self.connection = connection

    def __call__(self, ch, method, properties, body):
        tokens = body.split(",")
        memory_usage = int(tokens[0])
        queue_for_this_slave = tokens[1]
        slave_id = int(tokens[2])
        slave_status_dictionary[slave_id] = (memory_usage,queue_for_this_slave)
        self.count -= 1
        if self.count < 0:
            print "done consuming messages present in the queue"
            ch.stop_consuming()
            self.connection.close()






def cyberSafetyPredictorWorks():
    for post_to_be_predicted in list_of_posts_to_be_predicted:
        post_to_be_predicted.priority =  cybersafety_predictor.startPrediction(post_to_be_predicted)
    return

def loadingMediaSessions():
    postData = mo.findAllDataFromCollection(DATABASE_NAME, POST_COLLECTION_NAME)
    for data in postData:
        try:
            list_of_posts_to_be_predicted.append(MediaSession(data["postId"],data["description"],data["likeCount"]))
        except Exception:
            continue






def checkStatusQueue():
    credentials = pika.PlainCredentials(USERNAME,PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    status_queue = channel.queue_declare(queue=STATUS_QUEUE) 
    if status_queue.method.message_count == 0:
        print "no messages currently in the status queue."
        connection.close()
        return "no status"
    callback = CountCallback(status_queue.method.message_count,connection)
    channel.basic_consume(callback,
                          queue=STATUS_QUEUE,
                          no_ack=True)
    
    print(' waiting to get statuses from the slaves')
    channel.start_consuming()
    
def selectQueueToSendMediaSessions():
    number_of_slaves = len(slave_status_dictionary)
    for i in range(1,number_of_slaves+1):
        if int(slave_status_dictionary[i][0]) < 500:
            print str(slave_status_dictionary[i][0]) +" has been selected"
            return slave_status_dictionary[i][1]
    return None 

def sendMediaSessionsToSlaveQueue(queue_to_send_media_sessions):
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_to_send_media_sessions)
    message = ""
    global counter
    for post in list_of_posts_to_be_predicted:
        message = message+str(post.postId+"-"+str(counter))+","
    channel.basic_publish(exchange='',
                      routing_key=queue_to_send_media_sessions,
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2,
                      ))
    connection.close()
     
    
def startRunningMaster():
    loadingMediaSessions()
    if WHAT_SYSTEM_TO_RUN == 1:
        cyberSafetyPredictorWorks()
    while True:
        global counter
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #time.sleep(60) # sleep for a minute and then check the status queue for current slave usage statuses 
        checkStatusQueue()
        queue_to_send_media_sessions = selectQueueToSendMediaSessions()
        if queue_to_send_media_sessions is None:
            if len(slave_status_dictionary) == 0:
                print "spawn out a slave.no slave is currently out there for work."
            else:
                print "All slaves are operating at the maximum. Spawn out another slave please."
        elif queue_to_send_media_sessions == "no status":
            print "status queue is empty"
        else:
            print "master is now sending media sessions to queue: "+str(queue_to_send_media_sessions)
            sendMediaSessionsToSlaveQueue(queue_to_send_media_sessions)
            counter += 1
        print "current status of the slaves: "
        print slave_status_dictionary
        print "master is going to sleep for 10 seconds"
        time.sleep(10)
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
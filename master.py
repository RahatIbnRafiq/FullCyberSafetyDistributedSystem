
import sys
from CyberSafetyPredictor.Predictor import CyberSafetyPredcitor as CyberSafetyPredictor
import pika
import time

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
IP_LOCALHOST = "192.168.0.12"
STATUS_QUEUE = "status"




class CountCallback(object):
    def __init__(self, count):
        self.count = count

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






def cyberSafetyPredictorWorks():
    for post_to_be_predicted in list_of_posts_to_be_predicted:
        post_to_be_predicted.priority =  cybersafety_predictor.startPrediction(post_to_be_predicted)
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






def checkStatusQueue():
    credentials = pika.PlainCredentials(USERNAME,PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    status_queue = channel.queue_declare(queue=STATUS_QUEUE) 
    callback = CountCallback(status_queue.method.message_count)
    channel.basic_consume(callback,
                          queue=STATUS_QUEUE,
                          no_ack=True)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
def selectQueueToSendMediaSessions():
    number_of_slaves = len(slave_status_dictionary)
    for i in range(1,number_of_slaves+1):
        if slave_status_dictionary[i] < 90:
            return slave_status_dictionary[i][1]
    return None 

def sendMediaSessionsToSlaveQueue(queue_to_send_media_sessions):
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_to_send_media_sessions)
    message = ""
    for post in list_of_posts_to_be_predicted:
        message = message+str(post.postId)+","
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
        time.sleep(60) # sleep for a minute and then check the status queue for current slave usage statuses 
        checkStatusQueue()
        queue_to_send_media_sessions = selectQueueToSendMediaSessions()
        if queue_to_send_media_sessions is None:
            print "All slaves are operating at the maximum. Spawn out another slave please."
        else:
            sendMediaSessionsToSlaveQueue(queue_to_send_media_sessions)
            
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
import pika
import time
import sys

WHAT_SYSTEM_TO_RUN = 0
DATABASE_NAME = "VineDatabase"
POST_COLLECTION_NAME = "SampledASONAMPosts"

USERNAME = "test"
PASSWORD = "test"
IP_LOCALHOST = "128.138.244.39"
STATUS_QUEUE = "status"

N = 100

list_of_monitoring_media_sessions = []


class CountCallback(object):
    def __init__(self, count):
        self.count = count

    def __call__(self, ch, method, properties, body):
        tokens = body.split(",")
        for token in tokens:
            list_of_monitoring_media_sessions.append(token)
        print str(len(tokens))+" number of media sessions got by this slave. Added them to the monitoring list"
        ch.stop_consuming()
    
def sendStatusToMaster(slaveid,queue):
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=STATUS_QUEUE)
    message = str(len(list_of_monitoring_media_sessions))+","+queue+","+slaveid
    print "Sending status message to the master: "+message
    channel.basic_publish(exchange='',
                      routing_key=STATUS_QUEUE,
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2,
                      ))
    connection.close()
    


def getMediaSessionsFromQueue(queue):
    credentials = pika.PlainCredentials(USERNAME,PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    media_session_queue = channel.queue_declare(queue=queue) 
    if media_session_queue.method.message_count == 0:
        print "slave:media session queue is empty. returning"
        connection.close()
        return
    callback = CountCallback(media_session_queue.method.message_count)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)
    channel.start_consuming()


def startRunningSlave(slaveid,queue):
    while True:
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        sendStatusToMaster(slaveid,queue)
        getMediaSessionsFromQueue(queue)
        #print "slave is going to sleep for 5 seconds."
        time.sleep(5)
        
    return  



if __name__ == "__main__":
    slave_run_arguments = sys.argv
    if len(slave_run_arguments) == 1:
        print "you have to specify slave id and queue associated with this slave. Run python slave.py help to see the usage."
    else:
        if slave_run_arguments[1] == "help":
            print "python slave.py slaveid queuename what_system_to_run"
            print "0: round robin scheduler, everything in memory (default)"
            print "1: scheduler, everything in memory"
            
        else:
            if slave_run_arguments[3] == '0':
                print "running round robin everything in memory system"
                WHAT_SYSTEM_TO_RUN = 0
            elif slave_run_arguments[3] == '1':
                print "running scheduler, everything in memory"
                WHAT_SYSTEM_TO_RUN = 1
            startRunningSlave(slave_run_arguments[1],slave_run_arguments[2])
    print "slave is exiting ..."


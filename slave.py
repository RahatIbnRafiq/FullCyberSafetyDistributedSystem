import pika
import time
import sys
import threading
from Utility.SlaveMediaSession import SlaveMediaSession as SlaveMediaSession
from datetime import datetime
import os
import psutil

from IncrementalClassifier import ClassifierWorks as ClassifierWorks

WHAT_SYSTEM_TO_RUN = 0
DATABASE_NAME = "VineDatabase"
POST_COLLECTION_NAME = "SampledASONAMPosts"

USERNAME = "test"
PASSWORD = "test"
IP_LOCALHOST = "128.138.244.39"
STATUS_QUEUE = "status"


list_of_monitoring_media_sessions = []
list_of_new_media_sessions_from_master = []
total_media_sessions_being_monitored = 0

#list_of_media_sessions_got_from_master = []

lock_media_session_list = threading.Lock()


class classifyThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        while True:
            global list_of_monitoring_media_sessions
            global list_of_new_media_sessions_from_master
            global lock_media_session_list
            if len(list_of_new_media_sessions_from_master) > 0:
                #print "classify thread getting the lock"
                lock_media_session_list.acquire()
                for new_media_session in list_of_new_media_sessions_from_master:
                    list_of_monitoring_media_sessions.append(new_media_session)
                list_of_new_media_sessions_from_master = []
                lock_media_session_list.release()
                #print "classify thread released the lock and appended the new media sessions"
            ClassifierWorks.classifyMediaSessions(list_of_monitoring_media_sessions)

class CountCallback(object):
    def __init__(self, count):
        self.count = count

    def __call__(self, ch, method, properties, body):
        global list_of_monitoring_media_sessions
        #global list_of_new_media_sessions_from_master
        #global lock_media_session_list
        tokens = body.split(",")
        #print "communicator thread getting the lock"
        #lock_media_session_list.acquire()
        for token in tokens:
            if len(token) > 0:
                slave_media_session = SlaveMediaSession(token)
                #list_of_new_media_sessions_from_master.append(slave_media_session)
                list_of_monitoring_media_sessions.append(slave_media_session)
        #print str(len(tokens))+" number of media sessions got by this slave. Added them to the monitoring list"
        
        #lock_media_session_list.release()
        #print "communicator thread releasing the lock"
        ch.stop_consuming()
    
def sendStatusToMaster(slaveid,queue):
    credentials = pika.PlainCredentials(USERNAME, PASSWORD)
    parameters = pika.ConnectionParameters(IP_LOCALHOST, 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=STATUS_QUEUE)
    global list_of_monitoring_media_sessions
    #global list_of_new_media_sessions_from_master
    #global lock_media_session_list
    #global total_media_sessions_being_monitored
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    message = str(mem)+","+queue+","+slaveid
    #print "Sending status message to the master: "+message
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
        #print "slave:media session queue is empty. returning"
        connection.close()
        return
    callback = CountCallback(media_session_queue.method.message_count)
    channel.basic_consume(callback,
                          queue=queue,
                          no_ack=True)
    channel.start_consuming()


def startRunningSlave(slaveid,queue):
    global list_of_monitoring_media_sessions
    #thread1 = classifyThread(1, "classify thread")
    #thread1.start()
    while True:
        print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        sendStatusToMaster(slaveid,queue)
        getMediaSessionsFromQueue(queue)
        #print "slave is going to sleep for 5 seconds."
        #time.sleep(5)
        ClassifierWorks.classifyMediaSessions(list_of_monitoring_media_sessions)
        print str(len(list_of_monitoring_media_sessions))+" number of media sessions currently being monitored by this slave"
    #thread1.join()
      



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


'''
Created on Jan 21, 2015

@author: RahatIbnRafiq
'''
import pymongo as mongo

client = mongo.MongoClient('localhost', 27017)


def findPostsFromCollection(databaseName, collectionName,userid):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find({"userId": userid})

def findPostsbyUrlFromCollection(databaseName, collectionName,shareUrl):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find({"shareUrl": shareUrl})
    
def getDistinctUserFromPostCollection(databaseName, collectionName):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.distinct("userId")


def insertDataInDatabase(databaseName,collectionName, data):
    db = client[databaseName]
    collection = db[collectionName]
    document_id = ""
    try:
        document_id = collection.insert(data)
    except Exception as e:
        if "duplicate" in str(e):
            return document_id
        print "error in inserting data"
        print "database:"+str(databaseName)
        print "collection:"+str(collectionName)
        print "error"+str(e)
        return document_id
    return document_id

def sizeOfCollection(databaseName,collectionName):
    db = client[databaseName]
    collection = db[collectionName]
    size =  collection.count()
    return size
    

def findOneEntry(databaseName,collectionName):
    db = client[databaseName]
    collection = db[collectionName]
    data =  collection.find_one()
    return data

def dropDatabase(databaseName):
    connection = mongo.Connection()
    try:
        connection.drop_database(databaseName)
    except Exception as e:
        print "Error in dropping Database: "+str(databaseName)
        print str(e)

def dropCollection(databaseName,collectionName):
    connection = mongo.Connection()
    try:
        connection[databaseName].drop_collection(collectionName)
    except Exception as e:
        print "Error in dropping Collection: "+str(collectionName)+" in Database: "+str(databaseName)
        print str(e)

def dropDuplicatesFromCollection(databaseName,collectionName,keyName):
    db = client[databaseName]
    collection = db[collectionName]
    collection.ensure_index([("userid" , mongo.ASCENDING), ("unique" , True), ("dropDups" , True)])

def findAllDataFromCollection(databaseName,collectionName):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find()

def findAllCommentsFromCollection(databaseName,collectionName,postId):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find({"postId": postId})


def findUserFromCollection(databaseName,collectionName,userId):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find({"userId": userId})


def findPostInformationFromCollection(databaseName,collectionName,postId):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find({"postId": postId})

def getSelectedPostsFromCollection(databaseName,collectionName):
    db = client[databaseName]
    collection = db[collectionName]
    return collection.find({"commentCount": {"$gt" : 400}})


def addFieldToPoctCollection(databaseName,collectionName,postId,mentionCount,negativePercentage,negativeCount,positivePercentage,positiveCount):
    db = client[databaseName]
    collection = db[collectionName]
    documents = collection.find({"postId": postId})
    if documents.count() == 1:
        for document in documents:
            documentid = str( document["_id"])
            try:
                collection.update({'_id': documentid}, {'$set': {'mentionCount': mentionCount ,'negativePercentage': negativePercentage, 'negativeCount': negativeCount,'positivePercentage': positivePercentage, 'positiveCount': positiveCount}})
            except Exception as e:
                print str(e)+" in updating field"
                
                


def updateIsPredictedFieldPostCollection(value,databaseName,collectionName,postId):
    db = client[databaseName]
    collection = db[collectionName]
    documents = collection.find({"postId": postId})
    if documents.count() == 1:
        for document in documents:
            documentid = str( document["_id"])
            try:
                collection.update({'_id': documentid}, {'$set': {'isPredicted': value}})
            except Exception as e:
                print str(e)+" in updating field"
    
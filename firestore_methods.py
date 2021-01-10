import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import Increment


def firestore_init():
    cred = credentials.Certificate("./nwHacksServiceKey.json")
    default_app = firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db


def firestore_add(user, db, confidence):
    doc_ref = db.collection(u'userMessages').document(str(user))
    doc_ref.update({
        u'userID': user,
        u'positive': Increment(confidence[0]),
        u'neutral': Increment(confidence[1]),
        u'negative': Increment(confidence[2]),
        u'count': Increment(1)
    })


def firestore_score_array(db):
    array = []
    newArray = []

    docs = db.collection(u'userMessages').stream()
    for doc in docs:
        array.append([doc.id, doc.to_dict()])

    for value in array:
        dictionary = value[1]
        score = dictionary["positive"]*3 + \
            dictionary["neutral"]*2+dictionary["negative"]*1
        newArray.append([value[0], score])
    return newArray


def firestore_score_dict(db):
    array = []
    newDict = {}

    docs = db.collection(u'userMessages').stream()
    for doc in docs:
        array.append([doc.id, doc.to_dict()])

    for value in array:
        dictionary = value[1]
        score = dictionary["positive"]*3 + \
            dictionary["neutral"]*2+dictionary["negative"]*1
        newDict[value[0]] = score
    return newDict


def firestore_average_bubble(db):
    array = []
    newDict = {}

    docs = db.collection(u'userMessages').stream()
    for doc in docs:
        array.append([doc.id, doc.to_dict()])

    for value in array:
        dictionary = value[1]
        score = dictionary["positive"]*3 + \
            dictionary["neutral"]*2+dictionary["negative"]*1
        if dictionary["count"] == 0:
            pass
        else:
            score = score/dictionary["count"]
        newDict[value[0]] = score
    return newDict


def set_current_leader(db, user, score):
    doc_ref = db.collection(u'Variables').document(u'Leader')
    doc_ref.set({
        u'userID': user,
        u'max_score': score
    })


def pull_current_leader(db):
    doc_ref = db.collection(u'Variables').document("Leader")
    doc = doc_ref.get()
    dict = doc.to_dict()
    ID = dict['userID']
    return ID

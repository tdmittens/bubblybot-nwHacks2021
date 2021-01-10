import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def firestore_init():
    # Use the application default credentials
    cred = credentials.Certificate("./nwHacksServiceKey.json")
    default_app = firebase_admin.initialize_app(cred)

    db = firestore.client()


def firestore_add(user, db, confidence):
    doc_ref = db.collection(u'userMessages').document(user)
    doc_ref.set({
        u'userID': user,
        u'positive': confidence[0],
        u'neutral': confidence[1],
        u'negative': confidence[2]
    })

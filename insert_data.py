from firebase import firebase

firebase_session = firebase.FirebaseApplication(
    "https://superapp-6ac22-default-rtdb.firebaseio.com/"
)

firebase_session.put(
    "/users",
    "1",
    {"username": "test", "email": "test@test.com"}
)

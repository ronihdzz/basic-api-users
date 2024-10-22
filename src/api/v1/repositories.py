from database import firebase_session

class FirebaseRepository:

    @staticmethod
    def insert_user(id, data):
        firebase_session.put(f'/users', id, data)
        
    @staticmethod       
    def get_user(id):
        return firebase_session.get(f'/users', id)
    
    @staticmethod
    def update_user(id, data):
        firebase_session.put(f'/users', id, data)

    @staticmethod
    def delete_user(id):
        firebase_session.delete(f'/users', id)

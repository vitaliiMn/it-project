from datetime import datetime

from typing import List

class History:

    _id_counter = 0

    def __init__(self, user_id: int, time: datetime):
        self.id = History._generate_id()
        self.user_id = user_id
        self.time = time

    @classmethod
    def _generate_id(cls):
        cls._id_counter += 1
        return cls._id_counter
    
class HistoryDB:

    histories: List[History] = []

    def create_history(self, user_id: int) -> History:
        time = datetime.now()
        new_history = History(user_id=user_id, time=time)
        self.histories.append(new_history)
        return new_history
    
    def get_user_history(self, user_id: int) -> list:
        res = []
        for history in self.histories:
            if history.user_id == user_id:
                res.append({
                    "id": history.id,
                    "date": history.time
                })
        return res
    
histories = HistoryDB()
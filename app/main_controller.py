from .db.db_manager_abc import DbManagerABC
from .queue_manager import QueueManager


class MainController(object):
    def __init__(self, queue_manager: QueueManager, db_manager: DbManagerABC):
        self._queue_manager = queue_manager
        self._db_manager = db_manager
        self._queue_manager.bind_to(self.run_filter)

    def run_filter(self):
        print("OK")
        while not self._queue_manager.is_queue_empty():
            post_id = self._queue_manager.get_from_queue()
            self._db_manager.update_columns('posts', {'flag': '5'}, 'ID=' + str(post_id), join_transaction=True)
            # result = self._db_manager.select_from_table('posts', condition='ID='+str(post_id), join_transaction=True)
            # print(str(result))
        self._db_manager.commit()
        self._db_manager.disconnect()

    def add_to_queue(self, content):
        self._queue_manager.add_to_queue(content)

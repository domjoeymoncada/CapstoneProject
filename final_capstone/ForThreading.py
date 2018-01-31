import DBHelper as Db
import VoiceHelper as voice
from threading import Thread

class FuncThread(Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        Thread.__init__(self)

    def run(self):
        self._target(*self._args)

if __name__ == "__main__":
    t1 = FuncThread(voice.doMath(), [1, 2], 6)
    t2 = FuncThread(Db.checkDB("806169"), [1, 2], 6)
    t1.start()
    t2.start()
    t2.join()
    t1.join()

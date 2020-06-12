import threading
import update_seats
import datetime
import time
end = False

def check_test():
    print('sleep', datetime.datetime.now())
    time.sleep(5)
    print('awake', datetime.datetime.now())


def execute_per_minute(second=10.0, num=0):
    global end
    num += 1
    print(num)
    if end:
        print('엥')
        return
    # update_seats.cinemaLoop()
    check_test()
    threading.Timer(second, execute_per_minute, [second, num]).start()

execute_per_minute(2, 0)


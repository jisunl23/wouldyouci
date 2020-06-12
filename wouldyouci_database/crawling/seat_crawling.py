import threading
import update_seats

end = False

def execute_per_minute(second=30.0):
    global end
    if end:
        return
    update_seats.cinemaLoop()
    threading.Timer(second, execute_per_minute, [second]).start()

execute_per_minute(10)


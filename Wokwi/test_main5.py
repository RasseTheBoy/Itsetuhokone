from time import sleep

def while_runner(func):
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)

    return wrapper


@while_runner
def run():
    while True:
        print('Running')
        sleep(0.5)
    
    print('Stopped')
    sleep(1)


try:
    run()
except KeyboardInterrupt:
    print('Interrupted')

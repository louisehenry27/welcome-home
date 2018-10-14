import asyncio
import functools
from lights import Light
from datetime import datetime
import os
from poll_events import poll_event


tv = Light(12)
lamp = Light(1)


async def periodic(loop, period):
    prev_time = datetime.now()

    while True:
        print('running periodic @', datetime.now())

        # loop.create_task(tv.party(seconds = 5, count = 8))
        # loop.create_task(lamp.party(seconds = 2, count = 8))

        loop.create_task(poll_event(loop, prev_time))

        prev_time = datetime.now()
        await asyncio.sleep(period)

                                  
async def exit():                                              
    loop = asyncio.get_event_loop()                      
    print("Stop")                                        
    loop.stop() 

    print("Shutdown complete ...")    

                                      
async def cancel_async(task):                                              
    task.cancel()
 
if __name__ == '__main__':

    my_event_loop = asyncio.get_event_loop()
    try:
        print('task creation started')

        periodic_task = my_event_loop.create_task(periodic(my_event_loop, 10))

        # my_event_loop.run_until_complete(asyncio.wait(tasks))
        my_event_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:

        try:
            print("Shutting down")

            pending = asyncio.Task.all_tasks()

            print('waiting for any pending tasks to complete...') 

            # Run loop until tasks done:
            my_event_loop.run_until_complete(asyncio.gather(*pending))
        except KeyboardInterrupt:
            print("Cancelling tasks due to user sigterm ;)")

            for task in asyncio.Task.all_tasks():
                task.cancel()

        finally:
                 
            asyncio.ensure_future(exit())   



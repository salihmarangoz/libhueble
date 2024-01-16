import libhueble
import asyncio
import time
from apscheduler.schedulers.blocking import BlockingScheduler

BLUETOOTH_ADDRESS = 'C1:F4:FA:FD:FB:78'
START_BRIGHTNESS = 0.0
FINAL_BRIGHTNESS = 1.0
START_TEMPERATURE = 1.0
FINAL_TEMPERATURE = 0.5
TIME_STEP = 1.0  # seconds. do not go below 0.5
NUM_TIME_STEPS = 60*15 # finish the transition in 15 mins

async def wake_up_scenario():
    lamp = libhueble.Lamp(BLUETOOTH_ADDRESS)
    await lamp.connect()
    print('Connected to the Lamp.')

    # Close the lamp and wait for a second
    await lamp.set_power(False)
    await asyncio.sleep(1.0)

    # Interpolate from start to final brightness and temperature
    is_power_on = False
    try:
        for t in range(NUM_TIME_STEPS+1):
            timestamp = time.time()
            current_time = t / NUM_TIME_STEPS
            current_brightness = (FINAL_BRIGHTNESS-START_BRIGHTNESS)*current_time + START_BRIGHTNESS
            current_temperature = (FINAL_TEMPERATURE-START_TEMPERATURE)*current_time + START_TEMPERATURE
            #print(current_brightness, current_temperature)

            await lamp.set_brightness(current_brightness)
            await lamp.set_temperature(current_temperature)
            if not is_power_on:
                await lamp.set_power(True)

            timediff = time.time() - timestamp
            if TIME_STEP - timediff > 0:
                await asyncio.sleep(TIME_STEP - timediff)
    finally:
        await lamp.disconnect()

def job_function():
    asyncio.run(wake_up_scenario())

scheduler = BlockingScheduler()
#scheduler.add_job(job_function, 'cron', second=0) # For testing
scheduler.add_job(job_function, 'cron', hour=7, minute=30)
scheduler.start()
scheduler.shutdown(wait=True)
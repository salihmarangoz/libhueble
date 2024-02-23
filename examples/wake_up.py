import libhueble
import asyncio
import time
from apscheduler.schedulers.blocking import BlockingScheduler

BLUETOOTH_ADDRESS = 'C1:F4:FA:FD:FB:78'
START_BRIGHTNESS = 0.0
FINAL_BRIGHTNESS = 1.0
START_TEMPERATURE = 1.0
FINAL_TEMPERATURE = 0.2
TIME_STEP = 10.0  # seconds. do not go below 0.5
NUM_TIME_STEPS = (60*30)//TIME_STEP # finish the transition in 60 mins

async def wake_up_scenario():
  lamp = libhueble.Lamp(BLUETOOTH_ADDRESS)
  is_finished = False
  t = 0

  while t <= NUM_TIME_STEPS:
    try:
      print('Connecting to the Lamp.')
      await lamp.connect()
      print('Connected!')

      # Close the lamp and wait for a second
      if t == 0:
        await lamp.set_power(False)
        await asyncio.sleep(1.0)

      # Interpolate from start to final brightness and temperature
      is_power_on = False
      while t <= NUM_TIME_STEPS:
        timestamp = time.time()
        t += 1
        current_time = t / NUM_TIME_STEPS
        current_brightness = (FINAL_BRIGHTNESS-START_BRIGHTNESS) * current_time + START_BRIGHTNESS
        current_temperature = (FINAL_TEMPERATURE-START_TEMPERATURE) * current_time + START_TEMPERATURE
        print(current_time, current_brightness, current_temperature)

        await lamp.set_brightness(current_brightness)
        await lamp.set_temperature(current_temperature)
        if not is_power_on:
          await lamp.set_power(True)

        timediff = time.time() - timestamp
        if TIME_STEP - timediff > 0:
          await asyncio.sleep(TIME_STEP - timediff)

      await lamp.disconnect()
    except:
      print("Connection lost. Reconnecting...")
      await asyncio.sleep(1.0)

def job_function():
  asyncio.run(wake_up_scenario())

scheduler = BlockingScheduler()
#scheduler.add_job(job_function, 'cron', second=0) # For testing
scheduler.add_job(job_function, 'cron', hour=7, minute=0)
scheduler.start()
scheduler.shutdown(wait=True)
import time
from soil import getSensorReadings

def getSoilReadings():
    sensor_per = -1
    try:
      sensor_per = -1
    except RuntimeError as error:
      print(error.args[0])
    except Exception as error:
      print("Closed device due to an encountered error: ", error)
    finally:
      time.sleep(2.0)
      return sensor_per
from acconeer.exptool import a121
from acconeer.exptool.a121.algo.distance import Detector as DistanceDetector, DetectorConfig as DistanceConfig
import time

client = a121.Client.open(serial_port="/dev/ttyUSB0")

tracking_reading = None
threshold = 0.5
miss_count = 0
max_misses = 5
current_time = time.time() #start timer
previous_time = 0 
calculated_speed = 0

def compute_speed(current_reading, tracking_reading, dt):
        
        return (current_reading - tracking_reading) / dt

distance_detector = DistanceDetector (
    client = client,
    sensor_ids=[1],
    detector_config = DistanceConfig(
        start_m = 0.2, #you can change these parameters
        end_m = 5
    )
)

distance_detector.calibrate_detector()
distance_detector.start()

try:
    while True:
        result = distance_detector.get_next()[1] #get results for sensor 1
        distances = result.distances #save the distances in a variable

        #if no distances are detected, increase the miss count
        if len(distances)==0: 
            miss_count+=1

        else:
            # take the minimum distance as the current reading 
            # (you can also use other methods, such as averaging)
            current_reading = min(distances) 

            # check if there is a value in previous reading, if not, set it to current reading and reset miss count
            if tracking_reading is None and previous_time == 0:
                tracking_reading = current_reading
                previous_time = current_time
                miss_count = 0 # restart miss count if we have a valid reading

            #if there is a value, compare it to the threshold
            elif abs(current_reading - tracking_reading) <= threshold:
                
                if (current_reading - tracking_reading) < 0:
                     print("Object is approaching")
                     calculated_speed = compute_speed(current_reading, tracking_reading, current_time - previous_time)
                     print(f"Calculated speed: {calculated_speed:.3f} m/s")
                     previous_time = current_time # update the previous time for the next speed calculation
                
                elif (current_reading - tracking_reading) > 0:
                    print("Object is moving away")
                    calculated_speed = compute_speed(current_reading, tracking_reading, current_time - previous_time)
                    print(f"Calculated speed: {calculated_speed:.3f} m/s")
                    previous_time = current_time # update the previous time for the next speed calculation

                tracking_reading = current_reading
                miss_count = 0
        
            else:
                miss_count+=1 # otherwise, increase the miss count

        # if too many miss counts, object lost
        if miss_count > max_misses: 
                tracking_reading = None 
                miss_count = 0
        if tracking_reading is None:
                print("None")
                    
        else:
            print(f"{tracking_reading:.3f}")
                

except KeyboardInterrupt:
    print("Stopping tracking system...")

    distance_detector.stop()
    client.close()

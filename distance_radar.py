from acconeer.exptool import a121
from acconeer.exptool.a121.algo.distance import Detector as DistanceDetector, DetectorConfig as DistanceConfig

client = a121.Client.open(serial_port="/dev/ttyUSB0")

tracked_distance = None
threshold = 0.5
miss_count = 0
max_misses = 2

distance_detector = DistanceDetector (
    client = client,
    sensor_ids=[1],
    detector_config = DistanceConfig(
        start_m = 0.2, #you can change these parameters
        end_m = 2
    )
)

distance_detector.calibrate_detector()
distance_detector.start()

while True:
    result = distance_detector.get_next()[1]
    distances = result.distances

    if len(distances)==0:
        miss_count+=1

    else:
        measured_distance = min(distances)
            
        if tracked_distance is None or abs(measured_distance - tracked_distance) <= threshold:
            tracked_distance = measured_distance
            miss_count = 0
        else:
            miss_count+=1

    if miss_count > max_misses: 
            tracked_distance = None 
            miss_count = 0

    valid = tracked_distance is not None
            
    if tracked_distance is None:
        print("None")
            
    else:
        print(f"{tracked_distance:.3f}")

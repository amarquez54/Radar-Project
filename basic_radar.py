from acconeer.exptool import a121
from acconeer.exptool.a121.algo.distance import Detector as DistanceDetector, DetectorConfig as DistanceConfig
from acconeer.exptool.a121.algo.speed import Detector as SpeedDetector, DetectorConfig as SpeedConfig
import json


def main():

    #only run one at a time
   run_speed()
    #run_distance()

    

def run_distance():
    client = a121.Client.open(serial_port="/dev/ttyUSB0")

    distance_detector = DistanceDetector (
        client = client,
        sensor_ids=[1],
        detector_config = DistanceConfig(
            start_m = 0.2, #you can change these parameters
            end_m = 1.5
        )
    )

    distance_detector.calibrate_detector()
    distance_detector.start()

    print("Distance Mode: press CTRL + C to stop")

    try:
        while True:
            result = distance_detector.get_next()[1]

            if len(result.distances) == 0:
                data = {
                    "distances": None
                }
            else:
                distance = min(result.distances)
                data = {
                    "distance": round(distance, 3)
                }
            
            print(json.dumps(data))

    except KeyboardInterrupt:
        print("Stopping")

    distance_detector.stop()
    client.close()

def run_speed():
    client = a121.Client.open(serial_port="/dev/ttyUSB0")

    speed_detector = SpeedDetector(
        client=client,
        sensor_id=1,
        detector_config=SpeedConfig(
            start_point=200,     #you can change these parameters
            num_points=1,
            num_bins=50,
            max_speed=10.0,
            threshold=100.0,
        ),
    )

    speed_detector.start()

    print("Speed Mode: press CTRL + C to stop")

    try:
        while True:
            result = speed_detector.get_next()
            speed = result.max_speed

            data = {
                "speed": round(speed, 3)
            }

            print(json.dumps(data))

    except KeyboardInterrupt:
        print("Stopping")

    speed_detector.stop()
    client.close()



if __name__ == "__main__":
    main()
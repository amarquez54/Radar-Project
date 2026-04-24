from acconeer.exptool import a121
from acconeer.exptool.a121.algo.speed import Detector as SpeedDetector, DetectorConfig as SpeedConfig

client = a121.Client.open(serial_port="/dev/ttyUSB0")

# parameters to change
sensitivity = 0.01
miss_count = 0
max_misses = 5
tracked_speed = 0
start_m = 1.0

motion = "no motion detected"
start_point = int(start_m / 0.0025)

speed_detector = SpeedDetector(
    client=client,
    sensor_id=1,
    detector_config=SpeedConfig(
        # all parameters set to default

        start_point=start_point, #start point of measurement interval

        num_points=1,# Measure speed at a single point, increasing points increases coverage but reduces specificity 

        num_bins=50, # Determines the resolution in m/s, increasing bins increases resolution but also reduces update rate

        max_speed=10.0, # set slightly higher than what you are expecting to measure to increase accuracy

        threshold=100.0, # this is what prohibits the detector from reporting random deviations as detected speeds
                         # filter out lesser reflective objects by increasing threshold
    ),
)

speed_detector.start()

try:
    while True:
        result = speed_detector.get_next()
        measured_speed = result.max_speed

        if abs(measured_speed) > sensitivity:
            tracked_speed = measured_speed
            miss_count = 0

            if tracked_speed < 0:
                motion = "object approaching"
            else:
                motion = "object moving away"

        else:
            miss_count += 1

            if miss_count >= max_misses:
                tracked_speed = 0
                motion = "no motion detected"
                miss_count = max_misses

        print(f"{tracked_speed:.3f} m/s  {motion}")

except KeyboardInterrupt:
    print("Stopping")
    speed_detector.stop()
    client.close()
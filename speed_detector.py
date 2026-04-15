from acconeer.exptool import a121
from acconeer.exptool.a121.algo.speed import Detector as SpeedDetector, DetectorConfig as SpeedConfig

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

try:
    while True:
        result = speed_detector.get_next()
        speed = result.max_speed

        if speed < 0:
            print(f"{speed:.3f}, Object Approaching")
        elif speed > 0:
            print(f"{speed:.3f}, Object Leaving")
        else:
            print(f"{speed:.3f}, No target detected")

except KeyboardInterrupt:
    print("Stopping")

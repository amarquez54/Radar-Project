import numpy as np
import acconeer.exptool as et
from acconeer.exptool import a121
from acconeer.exptool.a121.algo.obstacle import Detector, DetectorConfig

SENSOR_ID = [1]


client = a121.Client.open(serial_port="/dev/ttyUSB0")

detector_config = DetectorConfig(
    start_m=0.2,
    end_m=1,
    num_mean_threshold=1.5,
    num_std_threshold=4.0, 
    sweeps_per_frame=15, 
    max_robot_speed=0.1
)

detector = Detector(
    client=client,
    sensor_ids=SENSOR_ID,
    detector_config=detector_config
)

detector.calibrate_detector()
detector.start()    


try:
    while True:
        detector_result = detector.get_next()
        pr = detector_result.processor_results[SENSOR_ID[0]]

        if not pr.targets:
            print("No target")
        else:
            r_targets = pr.targets[0].distance
            v_targets = pr.targets[0].velocity

            print(f"Distance: {r_targets:.3f} m, Velocity: {v_targets:.3f} m/s")

except KeyboardInterrupt:
    print("Stopping detector...")
    detector.stop()
    client.close()


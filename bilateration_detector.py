import numpy as np
import acconeer.exptool as et
from acconeer.exptool import a121
from acconeer.exptool.a121.algo.bilateration import Processor, ProcessorConfig
from acconeer.exptool.a121.algo.distance import Detector, DetectorConfig, ThresholdMethod

_SENSOR_IDS = [2, 3]

client = a121.Client.open(serial_port="/dev/ttyUSB0")

detector_config = DetectorConfig(
    start_m = 0.25,
    end_m = 1.0,
    signal_quality = 25.0,
    max_profile = a121.Profile.PROFILE_1,
    max_step_length=2,
    threshold_method=ThresholdMethod.CFAR
)

detector = Detector(
    client = client,
    sensor_ids=_SENSOR_IDS,
    detector_config=detector_config
)

session_config = detector.session_config

processor_config = ProcessorConfig()

processor = Processor(
    session_config=session_config,
    processor_config=processor_config,
    sensor_ids=_SENSOR_IDS
)

detector.calibrate_detector()
detector.start()

try:
    while True:
        detector_result = detector.get_next()
        processor_result = processor.process(detector_result)



except KeyboardInterrupt:
    print("Stopping detector...")
    detector.stop()
    client.close()
import logging
import os

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        filename=os.path.join(log_dir, "a380_ai.log"),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

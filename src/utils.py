import yaml
import logging
import os


def setup_logging():
    # रूटमध्ये असल्याने थेट 'logs' फोल्डर वापरता येईल
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=os.path.join(log_dir, "pipeline.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filemode="a"
    )
    return logging.getLogger()


def load_config():
    # थेट 'config/config.yaml' वापरा
    try:
        with open("config/config.yaml", "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return None
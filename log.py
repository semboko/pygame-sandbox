import logging


logger = logging.getLogger("voxel_world")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("log.txt")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

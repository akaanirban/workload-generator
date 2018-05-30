from Generators.ImageDataGenerator import ImageDataGenerator
import logging
import sys
logging.getLogger(__name__)

# TODO: Use a config file for the init  configuration

if __name__ == "__main__":
    time = float(sys.argv[1])
    new_workload = ImageDataGenerator(src="/home/anirban/Pictures/First200", dest="/home/anirban/Pictures/test",
                                      time_interval =time, chunk_size=4, repeat_images=True)
    new_workload.generate()

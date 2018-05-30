from Generators.ImageDataGenerator import ImageDataGenerator
import logging

logging.getLogger(__name__)

# TODO: Use a config file for the init  configuration

if __name__ == "__main__":
    new_workload = ImageDataGenerator(src="/home/anirban/Pictures/First200", dest="/home/anirban/Pictures/test",
                                      time_interval =.01, chunk_size=4, repeat_images=True)
    new_workload.generate()

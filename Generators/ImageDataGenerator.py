import os
import random
import threading
import logging
import timeit


logging.basicConfig(format='%(asctime)s Content: %(message)s',level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


class ImageDataGenerator:
    def __init__(self, src: str, dest: str, chunk_size: int = 4,
                 time_interval: float = 1, repeat_images: bool = True) -> None:
        """
            Initializes an Image Generator Object.

            Generates a fixed number of symlinks in a destination folder from a source folder
            within a given interval asynchronously.

            Parameters
            ----------
            src : str
                Source folder.
            dest : str
                Destination folder.
            chunk_size : int
                The number of symlinks created per interval.
            time_interval : float
                The time interval for creating the symlinks.
            repeat_images : bool
                Flag to determine, whether to continue using same images after 1 pass.

            Returns
            -------
            None
        """
        self.id = random.randint(1, 10000)
        self.source_path = src
        self.destination_path = dest
        self.chunk_size = chunk_size
        self.all_files = []
        self.counter = 0
        self.time_interval = time_interval
        self.stop_generate_flag = threading.Event()
        self.repeat_images_flag = repeat_images
        self.get_all_files()
        logger.info(msg="Source Set at : {}".format(self.source_path))
        logger.info(msg="Destination Set at : {}".format(self.destination_path))
        logger.info(msg="{} images will be emitted per {} seconds".format(self.chunk_size, self.time_interval))
        self.totalcounter = 0

    def get_all_files(self):
        try:
            if os.path.exists(self.source_path):
                for filename in os.listdir(self.source_path):
                    self.all_files.append(self.source_path + os.sep + filename)
        except Exception as e:
            logger.error(msg=str(e))

    def create_symlink(self):
        """
            Image symlink creator function.

            If repeat images is set of False, then after all images in the folder are exhausted
            , the program will Exit

            Else, creates the symlinks sequentially, increments the counter.

        """
        #
        if self.counter+1 >= len(self.all_files) and self.repeat_images_flag is not True:
            self.stop()
            exit(0)

        for i in range(self.chunk_size):
            file_path = self.all_files[self.counter + i]
            filename = file_path.strip().split(os.sep)[-1]
            destination_path = self.destination_path + os.sep + filename
            if not os.path.exists(destination_path):
                os.symlink(file_path, destination_path)
            logger.info(msg="Symlink created for {}".format(filename))
        self.increment_counter()

    def unlink_previous(self):
        try:
            if os.path.exists(self.source_path):
                for filename in os.listdir(self.destination_path):
                    os.remove(self.destination_path + os.sep + filename)
        except Exception as e:
            logger.error(msg=str(e))

    def increment_counter(self):
        self.counter = self.counter + self.chunk_size
        if self.repeat_images_flag is True and self.counter >= len(self.all_files):
            self.counter = 0
        self.totalcounter = self.totalcounter+ self.chunk_size

    def generate(self):
        """
            Image symlink generator.

            Generates a fixed number of symlinks in a destination folder from a source folder
            within a given interval asynchronously.

        """
        start_time = timeit.default_timer()
        self.unlink_previous()
        self.create_symlink()
        if not self.stop_generate_flag.set():
            threading.Timer(self.time_interval, self.generate, []).start()
        logger.info(msg="Created {} symlinks in {} seconds, total images processed {}".format(self.chunk_size, timeit.default_timer() - start_time, self.totalcounter))

    def stop(self):
        self.stop_generate_flag.set()

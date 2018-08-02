import sqlite3
import sys
from os import path, environ
import timeit, logging
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Monitors.DockerMonitor import DockerMonitorUtils
import time

DB_FILE_NAME = "anirban.db"
conn = sqlite3.connect(DB_FILE_NAME)
cursor = conn.cursor()

logging.basicConfig(format='%(asctime)s Content: %(message)s',level=environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    cursor.execute('''CREATE TABLE IF NOT EXISTS docker_stats
                      ( ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
                        CONTAINER_ID TEXT,
                        CONTAINER_NAME TEXT NOT NULL,
                        RAW_MEMORY TEXT NOT NULL,
                        PERCENT_MEMORY TEXT NOT NULL,
                        NET_IO TEXT NOT NULL,
                        BLOCK_IO TEXT NOT NULL,
                        CPU_PERCENT TEXT NOT NULL                   
                            );''')
    count = 0
    try:
        while True:
            start_time = timeit.default_timer()
            docker_stats = DockerMonitorUtils.get_docker_stats_nonapi()
            print(docker_stats)
            for stats in docker_stats:
                cursor.execute(
                    "INSERT INTO docker_stats (CONTAINER_ID, CONTAINER_NAME, RAW_MEMORY, PERCENT_MEMORY, NET_IO, BLOCK_IO, CPU_PERCENT) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?);", (stats['container_id'], stats['cont_name'],
                                                                 stats['raw_memory'],
                                                                 stats['percent_memory'], stats['net_io'],
                                                                 stats['block_io'], stats['cpu_percent']))

                logger.info(msg="Logged data for {} in SQL".format(stats['cont_name']))
            logger.info(
                msg="Round {} done in symlinks in {} seconds".format(count, timeit.default_timer() - start_time))
            count += 1
            if not docker_stats:
                time.sleep(1)
    except KeyboardInterrupt:
        conn.commit()
        conn.close()
        logger.info("Exiting...")
        sys.exit(0)

    conn.commit()
    conn.close()

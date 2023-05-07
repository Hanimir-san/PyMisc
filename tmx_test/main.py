import datetime
import logging
import os

from timeit import default_timer
from pathlib import Path

import utils
import test

script_name = os.path.basename(__file__)
script_dir = Path(__file__).parent.absolute()
log_dir = os.path.join(script_dir, 'logs')

# if a log directory doesn't exist, create it
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

# generate log file name from current script name and date
now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logfile = os.path.join(log_dir, f'{script_name}_{now}.log')
handler = logging.FileHandler(logfile, 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)-30s %(module)-50s %(message)s')

# define logger, write log messages both to terminal and file
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

test_tmx_memoq = os.path.join(script_dir, 'data', 'memoq_sample_100000_tus.tmx')
test_tmx_files = (test_tmx_memoq, )

for test_tmx in test_tmx_files:
    logger.info(f'Running tests for file {test_tmx}')

    logger.info(f'Testing source and target text extraction with regular Python for loops.')
    start = default_timer()
    test.test_tu_get_text(test_tmx)
    end = default_timer()
    logger.info(f'Execution time: {end-start}')


    logger.info(f'Testing source and target text extraction with for loops over list indices with regular Python range.')
    start = default_timer()
    test.test_tu_get_text_range(test_tmx)
    end = default_timer()
    logger.info(f'Execution time: {end-start}')

    logger.info(f'Testing source and target text extraction with for loops over list indices with numpy arange.')
    start = default_timer()
    test.test_tu_get_text_np_arange(test_tmx)
    end = default_timer()
    logger.info(f'Execution time: {end-start}')


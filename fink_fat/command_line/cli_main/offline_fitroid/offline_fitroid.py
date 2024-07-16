import datetime
import os
import subprocess
from fink_fat.others.utils import LoggerNewLine
import fink_fat
import configparser
import pathlib

from fink_fat.others.utils import init_logging


def offline_fitroid(
    config: configparser.ConfigParser,
    path_config: str,
    start_date: datetime,
    end_date: datetime,
    logger: LoggerNewLine,
    verbose: bool,
):
    """
    Launch the run_offline_fitroid script in a separate processus.

    Parameters
    ----------
    config: configparser.ConfigParser
        configuration file object
    path_config: str
        path to the fink-fat configuration file
    start_date: datetime
        start date of the offline mode
    end_date:
        end date of the offline mode (not include)
    logger: LoggerNewLine
        logging object
    verbose: bool
        if true, activate verbosity
    """
    if verbose:
        logger.info(
            f"""
 --- START FITROID OFFLINE ---
 start date: {start_date}
 end date: {end_date}
    """
        )
        logger.newline()

    ff_path = os.path.dirname(fink_fat.__file__)
    offline_path = os.path.join(ff_path, "command_line", "cli_main", "offline_fitroid")

    log_path = config["OFFLINE"]["log_path"]
    if not os.path.isdir(log_path):
        pathlib.Path(log_path).mkdir(parents=True)

    proc = subprocess.run(
        os.path.join(
            offline_path,
            f"run_offline_fitroid.sh {str(start_date)} {str(end_date)} {offline_path} {path_config} {log_path} {verbose}",
        ),
        shell=True,
    )

    if proc.returncode != 0:
        logger = init_logging()
        logger.info(proc.stderr)
        logger.info(proc.stdout)
    return

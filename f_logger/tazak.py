import datetime
from f_utils import u_datetime


class LoggerTazak:

    # Logger CSV-File
    logger = None

    # DateTime of Logger Construction
    dt_init = None

    def __init__(self, titles, dir_logger=None):
        """
        ========================================================================
         Description: Constructor. Init the Private Attributes.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. titles : str (Column Titles separated by commas).
            2. path_dir : str (Path to Directory to store the logs).
        ========================================================================
        """
        if type(titles) == list:
            titles = ','.join(titles)
        assert type(titles) == str
        assert dir_logger is None or type(dir_logger) == str
        self.dt_init = datetime.datetime.now()
        csv_logger = f'log_{u_datetime.to_str(self.dt_init)}.csv'
        csv_logger = f'{dir_logger}\\{csv_logger}' if dir_logger else csv_logger
        self.logger = open(csv_logger, 'w', encoding='utf-8')
        self.logger.write(f'tazak,{titles}\n')

    def write(self, values):
        """
        ========================================================================
         Description: Write Values to the Logger with Tazak (delta of seconds
                        between now and the tazak of logger construction).
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. values : str or list (Values to Log).
        ========================================================================
        """
        assert type(values) in {str, tuple, list}
        if type(values) != str:
            values = ','.join([str(val) for val in values])
        dt_now = datetime.datetime.now()
        delta_seconds = (dt_now - self.dt_init).seconds
        print(delta_seconds)
        self.logger.write(f'{delta_seconds},{values}\n')

    def close(self):
        """
        ========================================================================
         Description: Close the CSV-File with the Logger.
        ========================================================================
        """
        print('CLOSE LOGGER TAZAK')
        self.logger.close()

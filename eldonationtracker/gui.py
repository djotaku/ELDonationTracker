# type: ignore

"""Launch the GUI."""
import logging
from rich.logging import RichHandler  # type ignore

import eldonationtracker.ui.call_main_gui as the_gui


# logging
LOG_FORMAT = '%(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[RichHandler(markup=True, show_path=False)])


if __name__ == '__main__':
    the_gui.main()

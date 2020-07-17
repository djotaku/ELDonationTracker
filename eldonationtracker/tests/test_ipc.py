"""Unit tests for ipc.py"""

import eldonationtracker.ipc as ipc

from unittest.mock import patch, mock_open


def test_write_ipc():
    open_mock = mock_open()
    with patch("eldonationtracker.ipc.open", open_mock, create=True):
        ipc.write_ipc("outputfolder", "1")
        open_mock.assert_called_with('outputfolder/trackerIPC.txt', 'w')
        open_mock.return_value.write.assert_called_once_with("1")

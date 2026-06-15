import os
import csv
import pickle
import tempfile
from typing import Iterable

from f_google.services.drive._internal._download import _Download
from f_google.services.drive._internal._upload import _Upload


class _Serial:
    """
    ========================================================================
     Drive Serialization — round-trip Python objects / tabular rows
     through Drive files. Composes the download/upload helpers and owns
     the temp-file lifecycle, so callers never touch tempfile / pickle /
     csv themselves.
    ========================================================================
    """

    def __init__(self,
                 download: _Download,
                 upload: _Upload) -> None:
        """
        ====================================================================
         Init with the Drive download and upload helpers.
        ====================================================================
        """
        self._download = download
        self._upload = upload

    def read_pickle(self, path: str) -> object:
        """
        ====================================================================
         Download a pickle file from Drive and return the unpickled
         object. The local temp file is removed before returning.
        ====================================================================
        """
        fd, local = tempfile.mkstemp(suffix='.pkl')
        os.close(fd)
        try:
            self._download.download(path_src=path, path_dest=local)
            with open(local, 'rb') as f:
                return pickle.load(f)
        finally:
            if os.path.exists(local):
                os.unlink(local)

    def upload_pickle(self, obj: object, path: str) -> None:
        """
        ====================================================================
         Pickle `obj` to a temp file and upload it to Drive at `path`
         (parent folders auto-created, overwrites silently).
        ====================================================================
        """
        fd, local = tempfile.mkstemp(suffix='.pkl')
        os.close(fd)
        try:
            with open(local, 'wb') as f:
                pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
            self._upload.upload(path_src=local, path_dest=path)
        finally:
            if os.path.exists(local):
                os.unlink(local)

    def upload_rows(self,
                    rows: Iterable[dict],
                    columns: list[str],
                    path: str) -> None:
        """
        ====================================================================
         Stream `rows` (dicts keyed by `columns`) to a temp CSV and
         upload it to Drive at `path`. Extra keys are ignored; `rows`
         may be a generator (written one at a time).
        ====================================================================
        """
        fd, local = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        try:
            with open(local, 'w', newline='') as f:
                writer = csv.DictWriter(f,
                                        fieldnames=columns,
                                        extrasaction='ignore')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            self._upload.upload(path_src=local, path_dest=path)
        finally:
            if os.path.exists(local):
                os.unlink(local)

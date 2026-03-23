import io
import os
from googleapiclient.http import MediaIoBaseDownload
from f_google.services.drive._internal._nav import _Nav, _FOLDER

_EXPORT_MIMES = {
    'application/vnd.google-apps.document':
        ('application/pdf', '.pdf'),
    'application/vnd.google-apps.spreadsheet':
        ('application/vnd.openxmlformats-officedocument'
         '.spreadsheetml.sheet', '.xlsx'),
    'application/vnd.google-apps.presentation':
        ('application/pdf', '.pdf'),
    'application/vnd.google-apps.drawing':
        ('application/pdf', '.pdf'),
}


class _Download:
    """
    ========================================================================
     Drive Download — download files/folders to local disk.
    ========================================================================
    """

    def __init__(self, service, nav: _Nav) -> None:
        """
        ====================================================================
         Init with a Drive API service and navigation helper.
        ====================================================================
        """
        self._service = service
        self._nav = nav

    def download(self,
                 path_src: str,
                 path_dest: str) -> None:
        """
        ====================================================================
         Download a file or folder from Drive to a local path.
         Creates parent directories locally if needed.
         Google-native docs are exported to suitable formats.
        ====================================================================
        """
        file_id = self._nav.resolve(path=path_src)
        meta = self._service.files().get(
            fileId=file_id,
            fields='mimeType'
        ).execute()
        mime = meta['mimeType']
        if mime == _FOLDER:
            self._folder(folder_id=file_id,
                         path_local=path_dest)
        else:
            os.makedirs(os.path.dirname(path_dest),
                        exist_ok=True)
            self._file(file_id=file_id,
                       mime=mime,
                       path_local=path_dest)

    def _file(self,
              file_id: str,
              mime: str,
              path_local: str) -> None:
        """
        ====================================================================
         Download a single file. Export if Google-native.
        ====================================================================
        """
        if mime in _EXPORT_MIMES:
            export_mime, ext = _EXPORT_MIMES[mime]
            # Append export extension if not already present
            if not path_local.endswith(ext):
                path_local += ext
            request = self._service.files().export_media(
                fileId=file_id,
                mimeType=export_mime
            )
        else:
            request = self._service.files().get_media(
                fileId=file_id
            )
        fh = io.FileIO(path_local, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.close()

    def _folder(self,
                folder_id: str,
                path_local: str) -> None:
        """
        ====================================================================
         Recursively download a folder from Drive.
        ====================================================================
        """
        os.makedirs(path_local, exist_ok=True)
        query = (f"'{folder_id}' in parents and "
                 f"trashed = false")
        response = self._service.files().list(
            q=query,
            fields='files(id, name, mimeType)'
        ).execute()
        for item in response.get('files', []):
            child_path = os.path.join(path_local, item['name'])
            if item['mimeType'] == _FOLDER:
                self._folder(folder_id=item['id'],
                             path_local=child_path)
            else:
                self._file(file_id=item['id'],
                           mime=item['mimeType'],
                           path_local=child_path)

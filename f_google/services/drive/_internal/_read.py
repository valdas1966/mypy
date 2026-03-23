import io
import os
from googleapiclient.http import MediaIoBaseDownload
from f_google.services.drive._internal._nav import _Nav
from f_google.services.drive._internal._read_response import _ReadResponse
from f_pdf.main import UPdf


class _Read:
    """
    ========================================================================
     Drive Read — read files into memory (no disk writes).
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

    def read(self,
             path: str,
             encoding: str = 'utf-8') -> _ReadResponse:
        """
        ====================================================================
         Read a file from Drive into memory.
         Supports .txt, .csv (decoded text) and .pdf (markdown text
         + rendered page images via f_pdf).
        ====================================================================
        """
        file_id = self._nav.resolve(path=path)
        data = self._to_memory(file_id=file_id)
        ext = os.path.splitext(path)[1].lower()
        if ext == '.pdf':
            pdf = UPdf.read(data=data)
            return _ReadResponse(text=pdf.text,
                                 pages=pdf.pages)
        # Text-based files (txt, csv, etc.)
        text = data.decode(encoding)
        return _ReadResponse(text=text)

    def _to_memory(self, file_id: str) -> bytes:
        """
        ====================================================================
         Download a file from Drive into memory and return raw bytes.
        ====================================================================
        """
        request = self._service.files().get_media(
            fileId=file_id
        )
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return buffer.getvalue()

import os


class UFile:
    """
    ============================================================================
     Utils-Class for File in Operating System.
    ============================================================================
    """

    @staticmethod
    def create(path: str) -> None:
        """
        ========================================================================
         Create an Empty File at the given Path.
        ========================================================================
        """
        try:
            with open(file=path, mode='w') as _:
                pass  # Just to create an empty file
        except Exception as e:
            raise IOError(f'Error creating file {path}: {e}')

    @staticmethod
    def is_exists(path: str) -> bool:
        """
        ========================================================================
         Return True if the File exists.
        ========================================================================
        """
        return os.path.exists(path)

    @staticmethod
    def delete(path: str) -> None:
        """
        ========================================================================
         Delete a File in a given Path.
        ========================================================================
        """
        try:
            os.remove(path)
        except FileNotFoundError:
            pass  # If the file does not exist, we pass
        except Exception as e:
            raise IOError(f'Error deleting file {path}: {e}')

    @staticmethod
    def change_extension(path: str, extension_new: str) -> None:
        """
        ========================================================================
         Change Extension of a given File.
        ========================================================================
        """
        pre = path.split('.')[0]
        path_new = f'{pre}.{extension_new}'
        os.rename(src=path, dst=path_new)


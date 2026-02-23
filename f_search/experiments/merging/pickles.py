from f_utils import u_pickle
from pathlib import Path


class MergePickles:
    """
    ============================================================================
     Merge all pkl files in a folder into one pkl file.
    ============================================================================
    """

    @staticmethod
    def run(folder: str, output: str) -> None:
        """
        ========================================================================
         Merge all pkl files in a folder into one pkl file.
         Files are processed in alphabetical order by filename.
        ========================================================================
        """
        path_folder = Path(folder)
        pkl_files = sorted(path_folder.glob('*.pkl'), key=lambda p: p.name)
        if not pkl_files:
            print(f'No pkl files found in: {folder}')
            return
        all_items: list = []
        for pkl_file in pkl_files:
            print(f'Loading: {pkl_file.name}')
            items = u_pickle.load(path=str(pkl_file))
            all_items.extend(items)
            print(f'  Added {len(items)} items. Total: {len(all_items)}')
        path_output = path_folder / output
        u_pickle.dump(obj=all_items, path=str(path_output))
        print(f'Saved {len(all_items)} items to: {path_output}')


def main() -> None:
    folder = 'f:\\paper\\i_4_solutions\\aggregative'
    output = 'aggregative.pkl'
    MergePickles.run(folder=folder, output=output)


if __name__ == '__main__':
    main()
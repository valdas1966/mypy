from f_utils import u_pickle
from pathlib import Path


def merge_pickles(folder_path: str, output_filename: str = 'problems.pkl') -> None:
    """
    ============================================================================
     Merge all pkl files in a folder into one pkl file.
     Files are processed in alphabetical order by filename.
    ============================================================================
    """
    folder = Path(folder_path)

    # Get all pkl files, sorted alphabetically by filename
    pkl_files = sorted(folder.glob('*.pkl'), key=lambda p: p.name)

    # Merge all problems into one list
    all_problems: list = []
    for pkl_file in pkl_files:
        print(f'Loading: {pkl_file.name}')
        problems = u_pickle.load(path=str(pkl_file))
        all_problems.extend(problems)
        print(f'  Added {len(problems)} problems. Total: {len(all_problems)}')

    # Save merged result
    output_path = folder / output_filename
    u_pickle.dump(obj=all_problems, path=str(output_path))
    print(f'Saved {len(all_problems)} problems to: {output_path}')


def main() -> None:
    path = 'f:\\paper\\i_3_problems\\100k'
    merge_pickles(folder_path=path)


if __name__ == '__main__':
    main()
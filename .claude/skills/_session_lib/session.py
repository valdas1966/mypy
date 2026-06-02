"""
============================================================================
 Drive helpers for the `session` skill.
============================================================================
 Mechanical Google-Drive operations for the session lifecycle, so the
 skill does not re-implement them inline each time. Run from the MyPy
 repo root (so `f_google` imports resolve):

   python .claude/skills/session/scripts/session.py find   <name>
   python .claude/skills/session/scripts/session.py read   <drive_path>
   python .claude/skills/session/scripts/session.py create <name> <YYYY-MM-DD> <local_md>

 - find   : scan YYYY/MM/DD for <name>_session.md; print exact + similar
            matches (newest first), the most-recent path, and whether it
            is a skeleton.
 - read   : print a Drive file's text (prior session, instructions, ...).
 - create : upload <local_md> to YYYY/MM/DD/<name>_session.md.
============================================================================
"""

import sys
from pathlib import Path

# Bootstrap: this script lives under <repo>/.claude/skills/session/scripts/,
# so its own dir is sys.path[0] and shadows the repo root. Walk up to the
# ancestor that holds `f_google` and put it first on the path.
_here = Path(__file__).resolve()
for _p in _here.parents:
    if (_p / 'f_google').is_dir():
        sys.path.insert(0, str(_p))
        break

from f_google.services.drive import Drive

# Marker written by skeleton session files (see SKILL.md template).
_SKELETON_MARKER = '_(to be filled in'


def _drive() -> Drive:
    return Drive.Factory.valdas()


def _is_skeleton(text: str) -> bool:
    # A skeleton has the placeholder in its work sections.
    return text.count(_SKELETON_MARKER) >= 2


def find(name: str) -> None:
    drive = _drive()
    target = f'{name.lower()}_session.md'
    exact: list[str] = []
    similar: list[str] = []
    # Year folders only (4-digit names) hold dated session files.
    years = [f for f in drive.folders() if f.isdigit() and len(f) == 4]
    for yy in sorted(years, reverse=True):
        for mm in drive.folders(path=yy):
            try:
                days = drive.folders(path=f'{yy}/{mm}')
            except Exception:
                continue
            for dd in days:
                try:
                    files = drive.files(path=f'{yy}/{mm}/{dd}')
                except Exception:
                    continue
                for f in files:
                    low = f.lower()
                    if not low.endswith('_session.md'):
                        continue
                    full = f'{yy}/{mm}/{dd}/{f}'
                    if low == target:
                        exact.append(full)
                    elif name.lower() in low:
                        similar.append(full)
    exact.sort(reverse=True)
    similar.sort(reverse=True)
    print('EXACT:')
    for p in exact:
        print(f'  {p}')
    print('SIMILAR:')
    for p in similar:
        print(f'  {p}')
    if exact:
        most = exact[0]
        try:
            skel = _is_skeleton(drive.read(path=most).text)
        except Exception:
            skel = False
        print(f'MOST_RECENT: {most}')
        print(f'SKELETON: {skel}')
    else:
        print('MOST_RECENT: (none)')


def read(path: str) -> None:
    print(_drive().read(path=path).text)


def create(name: str, date: str, local_md: str) -> None:
    yy, mm, dd = date.split('-')
    dest = f'{yy}/{mm}/{dd}/{name}_session.md'
    _drive().upload(path_src=local_md, path_dest=dest)
    print(f'UPLOADED: {dest}')


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]
    if cmd == 'find' and len(rest) == 1:
        find(rest[0])
    elif cmd == 'read' and len(rest) == 1:
        read(rest[0])
    elif cmd == 'create' and len(rest) == 3:
        create(rest[0], rest[1], rest[2])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()

"""
============================================================================
 Windows backend - launch Claude tabs via Windows Terminal (wt.exe).
============================================================================
"""
import subprocess


def open_windows(names: list[str],
                 path_project: str) -> None:
    """
    ============================================================================
     Open Windows Terminal with one tab per Session-Name.
    ============================================================================
     Each tab runs:
        wsl.exe -- bash -lic
            "cd '<path_project>' && claude \"start session '<name>';\""
     Tabs are chained with the wt.exe ';' separator.
    ============================================================================
    """
    args: list[str] = ['wt.exe']
    for i, name in enumerate(names):
        if i > 0:
            args.append(';')
        bash_cmd = (
            f"cd '{path_project}' && "
            f'claude "start session \'{name}\';"'
        )
        args += [
            'new-tab',
            '--title', name,
            'wsl.exe', '--', 'bash', '-lic', bash_cmd,
        ]
    subprocess.Popen(args)

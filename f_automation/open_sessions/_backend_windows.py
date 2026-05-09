"""
============================================================================
 Windows backend - launch Claude tabs via Windows Terminal (wt.exe).
============================================================================
"""
import subprocess


def open_windows(names: list[str],
                 path_project: str) -> None:
    """
    ========================================================================
     Open Windows Terminal with one tab per Session-Name.
    ========================================================================
     Each tab runs:
        wsl.exe -- bash -lic
            "cd '<path>' && claude 'start session '\\''<name>'\\'';'"
     Tabs are chained with the wt.exe ';' separator.

     The bash command uses single-quote-only escaping (no embedded
     double quotes) so it survives the WSL/Windows interop chain,
     which otherwise mangles `\\"` and leaves bash with an
     unterminated `"` (EOF-while-looking-for-matching-`"`).
    ========================================================================
    """
    args: list[str] = ['wt.exe']
    for i, name in enumerate(names):
        if i > 0:
            args.append(';')
        prompt = f"start session '{name}';"
        bash_cmd = (
            f"cd {_sq(path_project)} && claude {_sq(prompt)}"
        )
        args += [
            'new-tab',
            '--title', name,
            'wsl.exe', '--', 'bash', '-lic', bash_cmd,
        ]
    subprocess.Popen(args)


def _sq(s: str) -> str:
    """
    ========================================================================
     Wrap `s` in single quotes for safe inclusion in a bash command.
    ========================================================================
     Replaces every `'` with the standard idiom `'\\''` (close, escaped
     quote, reopen) and wraps the result in `'...'`.
    ========================================================================
    """
    return "'" + s.replace("'", "'\\''") + "'"

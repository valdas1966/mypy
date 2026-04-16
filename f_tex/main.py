import subprocess
import tempfile
from pathlib import Path


class Tex:
    """
    ============================================================================
     LaTeX Compiler.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 engine: str = 'tectonic') -> None:
        """
        ========================================================================
         Init Tex Compiler bound to a specific LaTeX Engine Binary.
        ========================================================================
        """
        self._engine = engine

    @property
    def engine(self) -> str:
        """
        ========================================================================
         Name of the LaTeX Engine Binary (e.g. 'tectonic').
        ========================================================================
        """
        return self._engine

    def compile(self, src: str) -> bytes:
        """
        ========================================================================
         Compile a .tex Source String into PDF Bytes.
         Uses a temp directory; leaves no artifacts on disk.
         Raises RuntimeError with engine stderr on failure.
        ========================================================================
        """
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tex_file = tmp_path / 'main.tex'
            tex_file.write_text(data=src, encoding='utf-8')
            # Run engine inside the temp dir so \input{..} resolves locally
            self._run(args=[str(tex_file)], cwd=tmp)
            pdf_path = tmp_path / 'main.pdf'
            return pdf_path.read_bytes()

    def compile_file(self,
                     path_src: str,
                     path_dest: str | None = None) -> bytes:
        """
        ========================================================================
         Compile a .tex File into PDF Bytes.
         Multi-file \\input{..} resolves relative to path_src's directory.
         Writes PDF to path_dest if given.
        ========================================================================
        """
        src_path = Path(path_src)
        if not src_path.is_file():
            raise FileNotFoundError(path_src)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            self._run(args=[f'--outdir={tmp}', str(src_path)])
            pdf = (tmp_path / f'{src_path.stem}.pdf').read_bytes()
        if path_dest is not None:
            Path(path_dest).write_bytes(data=pdf)
        return pdf

    def _run(self,
             args: list[str],
             cwd: str | None = None) -> None:
        """
        ========================================================================
         Run the LaTeX Engine with args; raise RuntimeError on failure.
        ========================================================================
        """
        try:
            result = subprocess.run(
                [self._engine, '--chatter=minimal', *args],
                cwd=cwd,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError:
            raise RuntimeError(
                f'Engine binary not found: {self._engine!r}. '
                f'Install it or pass engine=<name> to Tex(...).'
            )
        if result.returncode != 0:
            raise RuntimeError(
                f'{self._engine} failed (exit {result.returncode}):\n'
                f'{result.stderr or result.stdout}'
            )

    def __repr__(self) -> str:
        return f'Tex(engine={self._engine!r})'

from f_proj.noteret.tiktok.pipeline import PipelineInsert
import sys


# Set _NAME and _WORKERS for PyCharm, or pass as CLI arguments
_NAME = 'videos_by_hashtag'
_WORKERS = 16

if len(sys.argv) > 1:
    _NAME = sys.argv[1]
if len(sys.argv) > 2:
    _WORKERS = int(sys.argv[2])
PipelineInsert.run(name=_NAME, workers=_WORKERS)

from pathlib import Path
selfdir = Path(__file__).parent

js = open(selfdir/'script.js').read()

__all__ = [
	'js'
]
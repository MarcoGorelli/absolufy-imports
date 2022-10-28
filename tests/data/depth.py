from mypackage.mysubpackage import already_absolute
from mypackage.mysubpackage import already_absolute as f
from .foo.bar import baz
from .foo.bar.baz import baz
from ..foo import T
from .bar import D
from . import O
from datetime import datetime

print(T)
print(D)

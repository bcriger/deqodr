#!/usr/bin/python
##
# __init__.py: Package definition for deqodr.
##
# copyright 2014 Ben Criger (bcriger@gmail.com).
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the 
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public 
# License along with this program. If not, see 
# <http://www.gnu.org/licenses/>.
##

__version__ = (0, 0, 0)

import coset_hist as _ch

__modules = [_ch]

# So that reload(deqodr) does what users expect, we need to reload each
# module.
map(reload, __modules)

# We now expose the particular names we want to expose, relying on the
# __all__ variable in each module to define which names to expose.
from coset_hist import *

__all__ = reduce(lambda a, b: a+b, 
            map(lambda mod: mod.__all__, __modules)) + ['__version__']
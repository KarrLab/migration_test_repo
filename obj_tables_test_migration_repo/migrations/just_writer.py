""" Load custom IO classes for migration of model files whose data model is defined by this schema repo

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-07-18
:Copyright: 2019, Karr Lab
:License: MIT
"""

# if used, this file dynamically loads a Reader and/or Writer from the schema repo
# if this file exists, it will be imported the obj_tables migrator
# normally (as in wc_lang) this file will import a local Reader and/or Writer
# but this example just uses obj_tables's io
from obj_tables.io import Writer

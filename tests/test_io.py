""" Test reading of files in fixtures

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-23
:Copyright: 2019, Karr Lab
:License: MIT
"""

import unittest
import os
import obj_model
from pathlib import Path
from migration_test_repo import core


class TestIO(unittest.TestCase):

    def test_read_data_file_git_metadata(self):
        
        git_metadata = core._GIT_METADATA
        # todo: code in migrate to put git_metadata in a NamedTuple
        metadata_model_type = git_metadata[0]
        _, _, revision_attr = git_metadata[1]

        for data_file in Path(__file__).parent.glob('**/*.xlsx'):

            # ignore backup files
            if data_file.name.startswith('~$'):
                continue
            data_file = str(data_file)
            models = obj_model.io.Reader().run(data_file, models=[metadata_model_type], ignore_extra_sheets=True,
                ignore_sheet_order=True, ignore_extra_attributes=True,
                ignore_attribute_order=True, group_objects_by_model=True, validate=False)

            # check that there's exactly 1 instance of the metadata_model_type
            self.assertEqual(len(models[metadata_model_type]), 1)
            metadata_model = models[metadata_model_type][0]
            commit_hash = getattr(metadata_model, revision_attr)
            self.assertTrue(isinstance(commit_hash, str))
            self.assertEqual(len(commit_hash), 40)

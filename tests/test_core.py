""" Test of migration_test_repo.core

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-21
:Copyright: 2019, Karr Lab
:License: MIT
"""

import unittest
from migration_test_repo import core
from obj_model.utils import set_git_repo_metadata_from_path


class TestCore(unittest.TestCase):

    def test_make_models(self):
        ref_1 = core.NewReference(id='ref_1', published=True)
        ref_2 = core.NewReference(id='ref_2', published=False)
        test_1 = core.Test(
            id='test_1',
            name='example test_1',
            existing_attr=1,
            references=[ref_1, ref_2]
        )
        test_2 = core.Test(
            id='test_2',
            references=[ref_1]
        )
        self.assertEqual(ref_1.id, 'ref_1')
        self.assertTrue(ref_1.published)
        self.assertEqual(ref_1, test_1.references[0])
        self.assertEqual(test_2.existing_attr, 3)

    def test_git_metadata(self):
        metadata_class, metadata_attrs = core._GIT_METADATA
        self.assertEqual(core.GitMetadata, metadata_class)
        self.assertEqual(set(metadata_class.Meta.attributes), set(metadata_attrs))

        git_metadata = core.GitMetadata()
        set_git_repo_metadata_from_path(git_metadata)
        for attr in core.GitMetadata.Meta.attributes:
            self.assertTrue(getattr(git_metadata, attr))

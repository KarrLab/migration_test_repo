""" Test of obj_tables_test_migration_repo.core

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-21
:Copyright: 2019, Karr Lab
:License: MIT
"""

import unittest
from obj_tables_test_migration_repo import core


class TestCore(unittest.TestCase):

    def test_make_models(self):
        ref_1 = core.Reference(id='ref_1', published=True)
        ref_2 = core.Reference(id='ref_2', published=False)
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

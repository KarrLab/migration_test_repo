""" Test __main__.py

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-21
:Copyright: 2019, Karr Lab
:License: MIT
"""

import unittest
import argparse
import os
import capturer

from argparse import Namespace
from migration_test_repo.__main__ import main, Utils


class TestMain(unittest.TestCase):

    def setUp(self):
        repo_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        '''
        self.good_schema_changes_file = os.path.join(repo_root,
            'migrations', 'schema_changes_2019-03-23-17-43-25_095bca3.yaml')
        self.bad_schema_changes_file = os.path.join(repo_root,
            'tests', 'fixtures', 'bad_schema_changes_2019-03-23.yaml')
        '''

    def test_main(self):
        parser = argparse.ArgumentParser()
        args = Namespace(arguments=[], command='not a command')
        with capturer.CaptureOutput(relay=False):
            with self.assertRaises(SystemExit):
                main(parser, args)

    def test_utils(self):
        parser = argparse.ArgumentParser()
        args = Namespace(arguments=[], command='make_schema_changes_template')
        with capturer.CaptureOutput(relay=False):
            schema_changes_template_file = main(parser, args)
        self.assertTrue(os.path.isfile(schema_changes_template_file))
        filename = os.path.basename(schema_changes_template_file)

        # test validate_schema_changes_file
        args = Namespace(arguments=[filename], command='validate_schema_changes_file')
        with capturer.CaptureOutput(relay=False):
            with self.assertRaisesRegex(Exception, "schema changes file '.*' is empty"):
                main(parser, args)
        os.remove(schema_changes_template_file)

        args = Namespace(arguments=[], command='validate_schema_changes_file')
        with capturer.CaptureOutput(relay=False) as capture_output:
            with self.assertRaises(SystemExit):
                main(parser, args)

        '''
        args = Namespace(arguments=[self.good_schema_changes_file], command='validate_schema_changes_file')
        with capturer.CaptureOutput(relay=False) as capture_output:
            errors = main(parser, args)
        self.assertFalse(errors)

        args = Namespace(arguments=[self.bad_schema_changes_file], command='validate_schema_changes_file')
        with self.assertRaises(ValueError):
            main(parser, args)
        '''

        # test validate_schema
        args = Namespace(arguments=[], command='validate_schema')
        with capturer.CaptureOutput(relay=False):
            with self.assertRaises(SystemExit):
                main(parser, args)

        args = Namespace(arguments=['fixtures/bad_schema.py'], command='validate_schema')
        with capturer.CaptureOutput(relay=False) as capture_output:
            with self.assertRaises(ValueError):
                main(parser, args)

        args = Namespace(arguments=['migration_test_repo/core.py'], command='validate_schema')
        with capturer.CaptureOutput(relay=False):
            rv = main(parser, args)
            self.assertIn('successfully imported', rv)

        # test make_data_file
        for filename in ['test_file', 'test_file.xlsx']:
            args = Namespace(arguments=[filename], command='make_data_file')
            with capturer.CaptureOutput(relay=False):
                make_data_file = main(parser, args)
            self.assertTrue(os.path.isfile(make_data_file))
            os.remove(make_data_file)
        # filename is required
        args = Namespace(arguments=[], command='make_data_file')
        with capturer.CaptureOutput(relay=False) as capture_output:
            with self.assertRaises(SystemExit):
                main(parser, args)

        # test make_automated_migration_config_file
        # todo: fix this test: write the migration_config_file elsewhere so it doesn't overwrite the existing one
        '''
        args = Namespace(arguments=[], command='make_automated_migration_config_file')
        with capturer.CaptureOutput(relay=False):
            migration_config_file = main(parser, args)
        self.assertTrue(os.path.isfile(migration_config_file))
        os.remove(migration_config_file)
        '''

        with capturer.CaptureOutput(relay=False):
            with self.assertRaises(SystemExit):
                Utils.not_supported(parser, args)

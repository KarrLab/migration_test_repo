""" Code for creating configuration files in this repo

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-21
:Copyright: 2019, Karr Lab
:License: MIT
"""

import argparse
import os
from obj_model import migrate
from obj_model.migrate import SchemaChanges
import obj_model
from migration_test_repo import core


# todo: move or copy validate_schema_changes_file, make_schema_changes_template and make_data_schema_migration_conf_file creation to
# obj_model/migrate.py so they can be used by programmers doing migration
class Utils(object):

    @staticmethod
    def make_schema_changes_template(parser, args):
        this_git_repo = migrate.GitRepo(os.path.dirname(__file__), search_parent_directories=True)
        schema_changes = SchemaChanges(git_repo=this_git_repo)
        return schema_changes.make_template(verbose=True)

    @staticmethod
    def validate_schema_changes_file(parser, args):
        # if no argument provided, then validate all schema_changes_files
        this_git_repo = migrate.GitRepo(os.path.dirname(__file__), search_parent_directories=True)
        if args.arguments:
            schema_changes_files = [os.path.join(this_git_repo.migrations_dir(), args.arguments[0])]
        else:
            schema_changes_files = SchemaChanges.all_schema_changes_files(this_git_repo.migrations_dir())
        all_errors = []
        for schema_changes_file in schema_changes_files:
            errors = SchemaChanges.validate(SchemaChanges.load(schema_changes_file))
            if errors:
                all_errors.append((schema_changes_file, errors))
            else:
                print("validated schema changes file: '{}'".format(schema_changes_file))
        if all_errors:
            raise ValueError("schema changes file(s) '{}' do not validate:\n{}".format(
                [file for file, _ in all_errors], all_errors))

    @staticmethod
    def validate_schema(parser, args):
        if not args.arguments:
            parser.error("'validate_schema' command requires a filename argument")
        schema_file = args.arguments[0]
        try:
            migrate.SchemaModule(schema_file).import_module_for_migration()
        except migrate.MigratorError as e:
            raise ValueError("cannot import: '{}'\n{}".format(schema_file, e))
        rv = "successfully imported: '{}'".format(schema_file)
        print(rv)
        return rv

    @staticmethod
    def make_data_file(parser, args):
        if not args.arguments:
            parser.error("'make_data_file' command requires a filename argument")
        filename = args.arguments[0]
        if not filename.endswith('.xlsx'):
            filename = filename + '.xlsx'

        # make a few Models
        ref_1 = core.Reference(id='ref_1', published=True)
        ref_2 = core.Reference(id='ref_2', published=False)
        test_1 = core.Test(
            id='test_1',
            name='example test_1',
            existing_attr=1,
            references=[ref_1, ref_2]
        )

        fixtures_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'tests', 'fixtures'))
        fixture_file = os.path.join(fixtures_path, filename)
        obj_model.io.Writer().run(fixture_file, [test_1], models=[core.Test, core.Reference])
        print("Wrote obj_model data file: {}".format(fixture_file))
        return fixture_file

    @staticmethod
    def make_data_schema_migration_conf_file(parser, args):
        this_git_repo = migrate.GitRepo(os.path.dirname(__file__), search_parent_directories=True)
        data_schema_migration_conf_file = migrate.DataSchemaMigration.make_template_config_file(
            this_git_repo, 'migration_test_repo')
        print("Wrote data-schema migration config file: {}".format(data_schema_migration_conf_file))
        return data_schema_migration_conf_file

    @staticmethod
    def not_supported(parser, args):
        parser.error("command '{}' is not supported".format(args.command))

def main(parser, args):
    exec_map = dict(
        make_schema_changes_template=Utils.make_schema_changes_template,
        validate_schema_changes_file=Utils.validate_schema_changes_file,
        validate_schema=Utils.validate_schema,
        make_data_file=Utils.make_data_file,
        make_data_schema_migration_conf_file=Utils.make_data_schema_migration_conf_file
    )
    if args.command not in exec_map:
        parser.error("'{}' not a known command".format(args.command))
    fun = exec_map[args.command]
    return fun(parser, args)

if __name__ == '__main__':  # pragma: no cover
    parser = argparse.ArgumentParser(description='manage configuration files in this repo')
    parser.add_argument('command', choices=['make_schema_changes_template', 'validate_schema_changes_file',
        'validate_schema', 'make_data_file', 'make_data_schema_migration_conf_file'],
        help='operation to execute')
    # todo: describe each command
    parser.add_argument('arguments', nargs='*', help='arguments for the file being made')
    args = parser.parse_args()
    main(parser, args)

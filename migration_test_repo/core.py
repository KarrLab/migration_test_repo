""" Test repo for migration

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-21
:Copyright: 2019, Karr Lab
:License: MIT
"""

from obj_model import (SlugAttribute, BooleanAttribute, StringAttribute, IntegerAttribute,
    ManyToManyAttribute, TabularOrientation)
import obj_model


class GitMetadata(obj_model.Model):
    url = StringAttribute()
    branch = StringAttribute()
    revision = StringAttribute()

    class Meta(obj_model.Model.Meta):
        attribute_order = ('url', 'branch', 'revision')
        tabular_orientation = TabularOrientation.column
_GIT_METADATA = (GitMetadata, ('url', 'branch', 'revision'))


class Test(obj_model.Model):
    id = SlugAttribute()
    name = StringAttribute(default='test')
    existing_attr = IntegerAttribute(default=3)
    references = ManyToManyAttribute('Reference', related_name='tests')

    class Meta(obj_model.Model.Meta):
        attribute_order = ('id', 'name', 'existing_attr')


class Reference(obj_model.Model):
    id = SlugAttribute()
    published = BooleanAttribute()

    class Meta(obj_model.Model.Meta):
        attribute_order = ('id', 'published')

# comment on master
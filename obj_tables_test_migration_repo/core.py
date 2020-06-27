""" Test repo for migration

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2019-03-21
:Copyright: 2019, Karr Lab
:License: MIT
"""

from obj_tables import (SlugAttribute, BooleanAttribute, StringAttribute, IntegerAttribute,
                        ManyToManyAttribute)
import obj_tables


class Test(obj_tables.Model):
    id = SlugAttribute()
    name = StringAttribute(default='test')
    existing_attr = IntegerAttribute(default=3)
    references = ManyToManyAttribute('Reference', related_name='tests')

    class Meta(obj_tables.Model.Meta):
        attribute_order = ('id', 'name', 'existing_attr')


class Reference(obj_tables.Model):
    id = SlugAttribute()
    published = BooleanAttribute()

    class Meta(obj_tables.Model.Meta):
        attribute_order = ('id', 'published')

# comment on master

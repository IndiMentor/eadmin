from peewee import CharField, IntegrityError, BooleanField
from .base import BaseModel, BaseModelView


class Location(BaseModel):
    name = CharField(unique=True, max_length=40)
    description = CharField(max_length=80)
    directions = CharField(null=True, max_length=80)
    is_incall = BooleanField(null=True, default=False)
    active = BooleanField(default=True, null=True)

    def __unicode__(self):
        return self.name


class LocationAdmin(BaseModelView):
    # Visible columns in the list view
    column_list = ['name', 'description']
    column_exclude_list = []

    form_args = {
        'name': {
            'label': 'Name'
        },
        'directions': {
            'label': 'Driving Directions',
            'render_kw': {'placeholder': 'Very Brief Driving Directions'}
        },
        'is_incall': {
            'label': 'Is Incall?'
        }
    }
    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('name', )

    # Full text search
    column_searchable_list = ('name', )

    # Column filters
    column_filters = ('name', )

    # form_ajax_refs = {
    #     'user': {
    #         'fields': (User.username, 'email')
    #     }
    # }


def create_fake_locations(db):
    ftl = Location(name="Fort-Lauderale",
                   description="Luxury Appointment",
                   is_incall=True,
                   directions='Exit 43 I-95'
                   )
    wpb = Location(name="Outcall WPB", description="Anywhere south of PGA Blvd.", is_incall=False)
    mia = Location(name="Outcall Miami", description="North of Homestead Only", is_incall=False)

    try:
        ftl.save()
        wpb.save()
        mia.save()
    except IntegrityError:
        pass

    # db.commit()
    # db.close()

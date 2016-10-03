from peewee import CharField, SmallIntegerField, IntegrityError, PrimaryKeyField, ForeignKeyField, TextField
from .base import BaseModel, BaseModelView
from flask_admin.form import rules
from .photo import Photo
from wtforms.validators import Email, Regexp, NumberRange


class Site(BaseModel):
    site_id = PrimaryKeyField()
    name = CharField(unique=True, max_length=32)
    seo_text = CharField(max_length=64)
    tag_line = CharField(max_length=64)

    # Marketing Stuff
    logo = ForeignKeyField(Photo, 'is logo of', null=True, default=None)
    banner = ForeignKeyField(Photo, 'is banner for', null=True, default=None)

    # Contact Info
    booking_email = CharField(null=True)
    admin_email = CharField(null=True)
    phone_1 = CharField(null=True)
    phone_2 = CharField(null=True)
    phone_3 = CharField(null=True)

    base_rate = SmallIntegerField(null=True)
    discount_amt = SmallIntegerField()

    def __unicode__(self):
        return self.name


class SiteAdmin(BaseModelView):
    # Visible columns in the list view
    # column_exclude_list = []

    # form_choices = {
    #     'discount_amt': [('10', '10% (Agency)'),
    #                      ('20', '20% (Independent)')
    #                      ]
    # }

    form_args = {
        'name': {
            'label': 'Name'
        },
        'tag_line': {
            'label': 'Tag Line',
            'render_kw': {'placeholder': 'The catchy description of your entity'}
        },
        'seo_text': {
            'label': 'SEO',
            'render_kw': {'placeholder': 'Keywords your site should be optimized for (max 3)'}
        },
        'base_rate': {
            'label': 'Undiscouted Rate',
            'render_kw': {'placeholder': 'The Website hourly rate.  Used as baseline for calculating Indi '
                                         'Discounted rates'},
            'validators': [
                NumberRange(min=150,
                            message="The value entered is too low.  "
                                    "Should be $100 more than Indi Rate")]
        },
        'discount_amt': {
            'label': 'Indi Discout %',
            'render_kw': {'placeholder': 'Usually, 10% Agency.  20% Independent'}
        },
        'phone_1': {
            'label': 'Primary Phone',
            'render_kw': {'placeholder': 'Main phone number'}
        },
        'phone_2': {
            'label': 'Alternate Phone'
        },
        'phone_3': {
            'label': 'Alternate Phone'
        },
        'booking_email': {
            'label': 'Email',
            'render_kw': {'placeholder': 'Email online bookings should go to'},
            'validators': [Email("Must be an email address")]
        },
        'admin_email': {
            'label': 'Admin Email',
            'render_kw': {'placeholder': 'The email system notifications should be sent to'},
            'validators': [Email("Must be an email address")]
        },
        'banner': {
            'label': 'Website Banner'
        },
        'logo': {
            'label': 'Website Logo'
        }
    }

    form_create_rules = [
        rules.FieldSet(('name', 'tag_line', 'seo_text'), 'Profile'),
        rules.FieldSet(('logo', 'banner'), 'Marketing'),
        rules.FieldSet(('base_rate', 'discount_amt'), 'Pricing'),
        rules.FieldSet(('booking_email', 'admin_email', 'phone_1', 'phone_2', 'phone_3'), 'Contact')
    ]

    column_list = ['name', 'seo_text', 'phone_1']
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


def create_fake_sites(db):

    heather = Site(name="xxxHeather",
                   discount_amt=20,
                   seo_text="GFE MILF BLOND",
                   tag_line="The Most Mind Blowing Experience... EVER",
                   base_rate=350,
                   booking_email="justheatherescort@gmail.com",
                   phone_1="95Fore Five91 1657"
                   )

    bb = Site(name="Broward Bunnies",
              seo_text="GFE FTL WPB",
              tag_line="The Best a Man Can Get",
              base_rate=300,
              discount_amt=10,
              booking_email="justheatherescort@gmail.com",
              phone_1="95Fore Five91 1657"
              )
    fd = Site(name="Fantasy Dreams",
              seo_text="WPB GFE OUTCALL",
              tag_line="Where Dreams Come True",
              base_rate=350,
              discount_amt=10,
              booking_email="justheatherescort@gmail.com",
              phone_1="95Fore Five91 1657"
              )

    mya = Site(name="Mya",
               discount_amt=20,
               seo_text="ASIAN DOLL GFE",
               tag_line="Perfect Asian Spinner",
               base_rate=350,
               booking_email="myaxxxgfe@gmail.com",
               phone_1="954-300-5two88"
               )

    an = Site(name="Angels",
              discount_amt=10,
              seo_text="Angel European Models",
              tag_line="Fly Away To Heaven",
              base_rate=400,
              booking_email="justheatherescort@gmail.com",
              phone_1="95Fore Five91 1657"
              )

    mya.save()
    heather.save()
    bb.save()
    fd.save()
    an.save()
    db.commit()
    # db.commit()
    # db.close()



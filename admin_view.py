from flask_admin.contrib.peewee import ModelView
import os.path as op

file_path = op.join(op.dirname(__file__), 'static')

class BaseModelView(ModelView):
    """https://flask-admin.readthedocs.io/en/latest/api/mod_model/"""

    can_delete = False  # disable model deletion
    page_size = 50  # the number of entries to display on the list view

    # Dictionary where key is column name and value is string to display.
    # column_labels = dict(name='Name', last_name='Last Name')

    # Dictionary where key is column name and value is description for list view column or add/edit formfield
    # column_descriptions = dict(full_name='First and Last name')

    # Dictionary of list view column formatters.
    # For example, if you want to show price multiplied by two, you can do something like this:
    # column_formatters = dict(price=lambda v, c, m, p: m.price*2)

    # column_default_sort = None
    # Default sort column if no sorting is applied.
    # column_default_sort = 'user'


class EscortAdmin(ModelView):
    # can_view_details = True
    # create_modal = True
    # edit_modal = True
    can_delete = False
    can_export = True

    form_widget_args = {
        'description': {
            'rows': 10,
            'style': 'color: black'
        }
    }
    form_args = {
        'available_text': {'label': 'Availability'}
    }
    # form_ajax_refs = {
    #     'site_id': {
    #         'fields': ['name', 'seo_text'],
    #         'page_size': 10
    #     }
    # }
    # form_create_rules = [
    #     # Header and four fields. Email field will go above phone field.
    #     rules.FieldSet(('name', 'description', 'on_today', 'on_tommorrow'), 'Profile')
    # ]

    column_list = ['name', 'on_today', 'on_tommorrow', 'available_text']
    # Visible columns in the list view
    # column_exclude_list = ['height', 'weight', 'hair_color', 'description', 'eyes', 'vitals',
    #                        'bust', 'implants', 'tattoos', 'piercings', 'language', 'nationality',
    #                        'ethnicity']
    column_editable_list = ['available_text']
    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('name', 'on_today', 'on_tommorrow')

    # Full text search
    # Would be nice to search on available but not supported have to sort
    column_searchable_list = ('name',)

    # Column filters
    column_filters = ('name', 'on_today', 'on_tommorrow')

    @action('set_on_today', 'Set Available Today', 'Are you sure you want to set selected girls as '
                                                   'available today?')
    def set_on_today(self, ids):
        """Action available in list to make only the checked girls available"""
        try:
            query = Escort.select().where(Escort.user_id.in_(ids))

            for girl in query:
                girl.set_on_today(True)
                girl.save()

            # todo decide: not sure if really want this
            # query_not = Escort.select().where(Escort.user_id.not_in(ids))
            # for girl in query_not:
            #     girl.set_on_today(False)
            #     girl.save()

        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

    @action('set_on_tommorrow', 'Set Available Tommorrow')
    def set_on_tommorrow(self, ids):
        try:
            query = Escort.select().where(Escort.user_id.in_(ids))
            for girl in query:
                girl.set_on_tommorrow(True)
                girl.save()

            # todo decide: not sure if really want this
            # query_not = Escort.select().where(Escort.user_id.not_in(ids))
            # for girl in query_not:
            #     girl.set_on_tommorrow(False)
            #     girl.save()

        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

    @action('post_ad', 'Post Ad', 'Are you sure you want to post an ad with these girls?')
    def post_adhoc_ad(self, ids):
        """Posts an adhoc ad, using girls selected in List View"""
        # todo Implment adhoc ad posting.
        return

    @action('do_delete', 'Delete Girl', 'Delete. Are you sure?')
    def do_delete(self, ids):
        """Deletes selected girls from list view"""
        # todo delete girls in (ids)
        return


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


class SiteAdmin(BaseModelView):
    # Visible columns in the list view
    # column_exclude_list = []

    # form_choices = {
    #     'discount_amt': [('10', '10% (Agency)'),
    #                      ('20', '20% (Independent)')
    #                      ]
    # }
    inline_models = (models.photo.PhotoLogo,)
    """http://flask-admin.readthedocs.io/en/latest/api/mod_form_upload/"""
    form_extra_fields = {
        'logo': form.ImageUploadField('Logo',
                                      base_path="static",
                                      relative_path="./bb/",
                                      thumbnail_size=(100, 100, True)),
        'banner': form.ImageUploadField('Banner',
                                        base_path="static",
                                        relative_path="./bubba/",
                                        thumbnail_size=(100, 100, True))

    }

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
        }
        # ,
        # 'banner': {
        #     'label': 'Website Banner'
        # } #  ,
        # 'logo': {
        #     'label': 'Website Logo'
        # }
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


class PhotoAdmin(BaseModelView):
     column_list = ['name']
     form_extra_fields = {
        'name': form.ImageUploadField('Name',
                                      base_path="static",
                                      relative_path="./bb/",
                                      thumbnail_size=(100, 100, True))

    }

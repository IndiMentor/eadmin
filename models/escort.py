from peewee import (CharField, TextField, SmallIntegerField, IntegrityError, BooleanField,
                    PrimaryKeyField, ForeignKeyField)
from flask_admin.contrib.peewee import ModelView
from .base import BaseModel
from .site import Site
from flask_admin.actions import action
from flask_admin.form import rules


class Escort(BaseModel):
    """Defines an escort and the relationships she has with other entities
    Contains the following attributes:
    name            height      weight      hair_color  eyes
    vitals          bust        implants    tattoos     piercings   language
    brand_text      nationality ethnicity   description ad_text
    featured        available   vacation    new_girl    gfe
    pse             located_at

    null    index   unique  default
    """
    # Keys
    user_id = PrimaryKeyField()
    site_id = ForeignKeyField(Site, related_name="works_for")

    # Important Fields
    name = CharField(unique=True, max_length=80)

    # Frequently Updated Fields
    base_rate = SmallIntegerField(null=True)
    brand_text = CharField()
    ad_text = TextField(null=True)
    description = TextField(null=False)
    on_today = BooleanField(null=True, default=False)
    on_tommorrow = BooleanField(null=True, default=False)
    available_text = CharField(null=True, max_length=64)
    vacation = BooleanField(null=True, default=False)

    height = CharField(null=True, max_length=10)
    weight = SmallIntegerField(null=True)
    hair_color = CharField(null=True, max_length=16)
    eyes = CharField(null=True)
    vitals = CharField(null=True)
    bust = CharField(null=True)

    implants = BooleanField(null=True)
    tattoos = CharField(null=True, default=True)
    piercings = CharField(null=True, default=False)

    language = CharField(null=True, default='English')
    nationality = CharField(null=True)
    ethnicity = CharField(null=True)

    # Flags
    featured = BooleanField(null=True, default=False)

    new_girl = BooleanField(null=True, default=True)
    gfe = BooleanField(null=True, default=True)
    pse = BooleanField(null=True, default=False)

    def set_on_today(self, status):
        self.on_today = status

    def set_on_tommorrow(self, status):
        self.on_tommorrow = status

    def __unicode__(self):
        return self.name


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


def create_fake_escorts(db):
    """Creates test data consisting of 4 escorts"""
    sid = Site.get(Site.name == 'Broward Bunnies')
    mid = Site.get(Site.name == 'Mya')
    hid = Site.get(Site.name == 'xxxHeather')

    mya = Escort.create(name='Mya',
                        height="5'3",
                        weight=110,
                        eyes="Brown",
                        site_id=mid,
                        brand_text="Asian Spinner Doll",
                        implants=True,
                        new_girl=True,
                        gfe=True,
                        pse=False,
                        description="""Hey guys! I'm Mya! I'm 28 yrs old. I'm 5'3 110 lbs 34C-22-33.
Perfect Spinner! I'm always 100% GFE. I provide an unbelievable experience that will make you
want more and more. Trust me, my reviews prove it. I'm 100% Korean, though born in VA.
So I speak perfect English. I have looooonngg black hair and beautiful brown eyes.

I'm college educated. So we can have some nice convo as well as fun lol"""
                        )

    stella = Escort.create(name='Stella', height="5'0", weight=105, eyes='Blue',
                           site_id=sid,
                           brand_text='Best a Man can Get', implants=True, new_girl=True,
                           gfe=True,
                           description="""
                    Stella is out eastern european lovely.  She is new with us but has promised to
                    be the best a man can get""", ad_text="Ad text",
                           bust='34D')
    heather = Escort.create(name="xxxHeather",
                            height="5'3",
                            weight=120,
                            eyes="Green",
                            site_id=hid,
                            brand_text="The MOST mind blowing experience...Ever",
                            implants=True,
                            new_girl=True,
                            gfe=True,
                            pse=True,
                            description="""All Good"""
                            )
    robin = Escort.create(name='Robin', height="5'1", weight=115, eyes='Green',
                          site_id=sid,
                          brand_text='British Spinner', implants=False, new_girl=True,
                          gfe=True,
                          pse=True, ad_text="Robins ad text",
                          description="""Robin has recently arrived on these shores and has brought
her English attitude of refinement and couture with her.   She is a
bright girl, who will quickly put you at ease and then some.""",
                          bust='32C'
                          )

    allfields = Escort.create(name='Robinallfields', height="5'1", weight=115, eyes='Green',
                              brand_text='British Spinner', implants=False, new_girl=True,
                              site_id=sid,
                              gfe=True,
                              pse=True,
                              description="""Robin has recently arrived on these shores and has brought
her English attitude of refinement and couture with her.   She is a
bright girl, who will quickly put you at ease and then some.""",
                              bust='32C', hair_color="Blonde", vitals="32-34-32", tattoos=False,
                              piercings=False, language="Englsh", nationality='Russian', ethnicity='AA',
                              ad_text="Get it!", featured=True, available=True, vacation=False)

    new_girl = Escort.create(name='Naomi', height="5'3", weight=95, eyes='Green',
                             site_id=sid,
                             brand_text='AA Spinner', implants=False, new_girl=True,
                             gfe=True,
                             pse=True,
                             description="""Naomi has big tits and goes bareback""",
                             bust='36C', hair_color="Black", vitals="36-34-32", tattoos=False,
                             piercings=False, language="Englsh", nationality='American', ethnicity='AA',
                             ad_text="Get it bare!", featured=False, available=True, vacation=False
                             )
    # mya.save()
    # db.commit()
    # heather.save()
    # db.commit()
    # robin.save()
    # db.commit()
    # stella.save()
    # db.commit()
    # allfields.save()
    # db.commit()
    # new_girl.save()
    # db.commit()
    #

    db.commit()
    db.close()

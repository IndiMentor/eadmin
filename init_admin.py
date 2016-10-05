from model import Escort, Site, Location, Photo
from peewee import IntegrityError
from flask_admin import Admin
from admin_view import EscortAdmin, LocationAdmin, SiteAdmin, PhotoAdmin

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

def create_fake_photos(db):
    return

def init_admin(ems_admin_app, db):
    ems_admin = Admin(ems_admin_app, name='EMS', template_mode='bootstrap3')
    ems_admin.add_view(LocationAdmin(Location))

    ems_admin.add_view(EscortAdmin(models.escort.Escort))
    ems_admin.add_view(SiteAdmin(models.site.Site))
    ems_admin.add_view(PhotoAdmin(models.photo.Photo))

    Photo.create_table(fail_silently=True)
    create_fake_photos(db)

    Site.create_table(fail_silently=True)
    create_fake_sites(db)

    Location.create_table(fail_silently=True)
    create_fake_locations(db)

    Escort.create_table(fail_silently=True)
    create_fake_escorts(db)


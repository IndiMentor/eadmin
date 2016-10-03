# eadmin

Beginnings of an admin interface for ems

## Todo
1. ~~Add Test Data for xxxheather + Mya~~
1. ~~Add active flag for locations in case no driver, P/T incall etc~~
2. Outcall handling for rates
3. config management could use a class with public vars - user config file is just python assignments 
   config option just imports module.
4. Start establishing scaffolding for website instead of redirect to admin
3. M:M with location
    intersection table
    Foreign keys
    sub-form with list of location girl at
    (what about ad by loc which loc is girl listed under)
3. Image Processing sub-system
    redis / rq based
    workers on site where agency website hosted
    1 queue 1 worker
4. Write Best Practice Models doc.
4. Inline Forms
4. Image types array + processing
    Profile Photo Field Add
    Portfolio Table Add
    ImageTypes Table/class
        original
        indi-landscape
        indi-portrait
        ws-landscape
        ws-portrait
9. Relatopnships are ugly need to override display
9. Checkboxes smaller & 1/2 Sized Text Fields
9. Rate Hierarchy idea is not part of MVP
9. Refactor reviews code into product
    calls to image alchemy & pillow
    
## To done

~~Fillout Escort Object~~
~~Create site Object~~
~~Create location object~~
1. ~~Add discount_amt to Site~~
2. ~~Foreign Keys~~
3. ~~Rates Helper Class
    constructor takes base_price
    indi -= 100
    indi VIP base-100-(base-100)*discount_amt~~
3. ~~Init for debug purposes when seeding data~~
3. ~~Relationships set~~
    ~~Site First~~
3. ~~Add available-now action to list view https://flask-admin
.readthedocs.io/en/latest/advanced/#customizing-batch-actions~~
1. ~~Put rate @ escort level too~~
3. ~~Should loc have an incall Flag
    (how does ad look if girl is incall WPB, and outcall WPB,MIA,FTL)~~
5. ~~Basic Agency Site Skeleton~~
3. ~~Logo Field on site (200x200 say)~~
3. ~~Banner field on site (800x200 say)~~
3. ~~Phone # on site x 3 ~~
3. ~~eMail on site~~
3. ~~re-label all fields form_args = {
    'name': {
        'label': 'First Name',
        'validators': [required()]
        }
    }~~
1. ~~Basic Authorization~~
2. ~~Fix Deleting UI~~
1. ~~Change container to fluid~~Is there a need? Seems to be 
bootstrap's default
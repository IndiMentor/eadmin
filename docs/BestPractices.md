
## models & ModelViews


* Derive from BaseModel & BaseModelView
    from .base import BaseModel, BaseModelView
* set help_text parameter on field type in model (set's placeholder 
text)
* set unique = False for nullable columns
* explicitly declare a PrimaryKeyField
* List Keys, then Name, Then frequently edited then rest of fields
* default= where appropriate
* set max_length on charfields
* Use form_args to set labels/placeholders/Validators
    form_args = {
    'base_rate': {
                'label':'Undiscouted Rate',
                'render_kw': {'placeholder':'The Website hourly rate.  Used as baseline for calculating Indi '
                                            'Discounted rates'},
                'validators': [NumberRange(min=150, message="The value entered is too low.  Should be $100 more than Indi Rate")]
        }
    }
* Use RuleSets to layout information nicer
    form_create_rules = [
        rules.FieldSet(('name','tag_line','seo_text'),'Profile'),
        rules.FieldSet(('logo','banner'),'Marketing'),
        rules.FieldSet(('base_rate','discount_amt'),'Pricing'),
        rules.FieldSet(('booking_email','admin_email','phone_1','phone_2','phone_3'),'Contact')
    ]
* set column_list small enough that fits on smallest mobile
    column_list = ['name', 'seo_text','phone_1']
* Use form_widget_args to set height of TextArea s
    form_widget_args = {
        'description': {
        'rows': 10,
        'style': 'color: black'
        }
    }
* Use action_hanlers where possible for simpler user interface
* Use inline editors for edit from list to simplify user/IF
    column_editable_list = ['available_text']
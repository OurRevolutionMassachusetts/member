import re

class Member:
    invalid_affiliate_choice = [
        'DSA, ORMA and others',
        'Freedom Road Socialist Organization',
        'I am part of OR Hull and want start  or help start more regional south  shore affiliate',
        'Voter Choice Massachusetts',
        'We the People Massachusetts',
        'Wolf-PAC',
        'Worcester Community Labor Coalition'
    ]

    def __init__(self, csv=None):
        self.affiliate = None
        self.city = None
        self.csv = csv
        self.email = None
        self.event = None
        self.first_name = None
        self.last_name = None
        self.state = None
        self.tags = []
        self.unaffiliated = None
        self.zip_code = None

        if self.csv:
            self.bootstrap()

    def bootstrap(self):
        # handle the easy attrs
        self.load_basic_attrs()

        # split up tags
        self.tags = self.csv['can2_user_tags'].split(", ")

        # first pass at assigning affiliate based on fields
        self.load_affiliate_fields()

        # now based on tags
        self.load_affiliate_tags()

    def clean_city(self):
        if self.city is None:
            return False

        self.city = self.city.lower().lstrip().rstrip()
        self.city = re.sub(r', ma.*$', '', self.city)
        self.city = re.sub(r' town of$', '', self.city)
        self.city = re.sub(r'^town of ', '', self.city)

    def load_basic_attrs(self):
        map = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email',
            'zip_code': 'zip_code',
            'can2_user_city': 'city',
            'can2_state_abbreviated': 'state',
            'Event': 'event'
        }

        for (csv_k, obj_k) in map.items():
            if (len(self.csv[csv_k])) > 0:
                setattr(self, obj_k, self.csv[csv_k])

        # clean up city
        self.clean_city()

    def load_affiliate_fields(self):
        aff_fields = ['Affiliate or Caucus ', 'whichaffiliate']
        for f in aff_fields:
            choice = self.csv[f]
            if len(choice) > 0 and choice not in self.invalid_affiliate_choice:
                self.affiliate = choice
                self.unaffiliated = False

        # now based on "affiliate_status"; any value but "Yes" is unaffiliated (but no value is undetermined)
        if len(self.csv['affiliate_status']) > 0 and self.csv['affiliate_status'].lower() not in ['yes', 'true']:
            self.unaffiliated = True
            self.affiliate = False

    def load_affiliate_tags(self):
        for t in self.tags:
            if t == 'Our Revolution Local Group Member' or re.match('^OR ', t):
                self.affiliate = t
                self.unaffiliated = False
                break
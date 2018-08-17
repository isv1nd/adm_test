from django import test
from rest_framework import test as rf_test


class BaseTest(test.TestCase):
    pass


class BaseSimpleTest(test.TestCase):
    pass


class BaseV1TestCase(BaseTest):
    def setUp(self):
        super(BaseV1TestCase, self).setUp()
        self.client = rf_test.APIClient()

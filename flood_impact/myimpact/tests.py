from django.test import TestCase


class MyImpactTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test_discover(self):
        self.assertEquals('test', 'test')

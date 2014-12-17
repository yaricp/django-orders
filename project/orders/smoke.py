
from smoketest import SmokeTest
#from smoketest.decorators import slow, rolled_back
from .models import Order

print 123
class DemoTest(SmokeTest):
    def test_order_reads(self):
        """ just make sure we can read data from the db """
        cnt = Order.objects.all().count()
        print cnt
        self.assertTrue(cnt > 0)

    #@rolled_back
    #def test_order_writes(self):
        #""" make sure we can also write to the database
        #but do not leave any test detritus around.
        #"""
        #f = Order.objects.create()

    #@slow
    #def test_something_slow(self):
        #""" this test will not be run in "fast" mode
        #because it uses a lot of resources or otherwise
        #could bog down the production server in bad ways
        #"""
        ## do a bunch of slow stuff
        ## ...
        #self.assertEqual(foo, bar)


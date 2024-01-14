from django.test import TestCase
from spec_calculator.models import Height_groups, Age_ref, Income_groups

# Create your tests here.


class HeightTestCase(TestCase):

    @classmethod    
    def setUpTestData(cls):
        # Create test data for the Height_groups model
        Height_groups.objects.create(height_cm=160, ht_per = 50)
        Height_groups.objects.create(height_cm=140, ht_per= 60)

    def test_dbaccess(self):
        all_items = Height_groups.objects.filter(height_cm__gte=150)
        
        self.assertTrue(len(all_items) > 0)

        # Check if all items in the queryset meet the specified condition
        for item in all_items:
            self.assertGreaterEqual(item.height_cm, 150)
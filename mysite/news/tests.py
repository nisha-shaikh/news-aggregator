import datetime

from django.test import TestCase
from django.urls import reverse

from news.models import SearchResults, SearchRequests

# Create your tests here.

class searchNewsView(TestCase):

    def testAddToDB(self):
        """
        When new query is run, it should be added to database
        """

        response = self.client.post(reverse("news:searchNews"), {'kw': 'virus'})
        fields = list(SearchRequests.objects.filter(query='virus').values_list())
        self.assertEqual(fields, [('virus', datetime.date.today())])

    def testUpdateDate(self):
        """
        If query in database was added before EXP_DATE, query date should be updated
        """

        #adding test data to be removed after POST request
        old_query = SearchRequests.objects.create(query="virus", dateAdded=datetime.date(2019, 1, 1))
        response = self.client.post(reverse('news:searchNews'), {'kw': 'virus'})
        self.assertNotEqual(SearchRequests.objects.filter(query="virus").values("dateAdded"), datetime.date(2019, 1, 1))

    def testDeleteOldData(self):
        """
        Old data (with date > EXP_DATE) should not be in database
        """

        # adding test data
        old_query = SearchRequests.objects.create(query="virus", dateAdded=datetime.date(2019, 1, 1))
        oldEntry1 = SearchResults.objects.create(headline='test1', link='www.test1.com', source='reddit')
        oldEntry1.request.add(old_query)
        oldEntry2 = SearchResults.objects.create(headline='test2', link='www.test2.com', source='reddit')
        oldEntry2.request.add(old_query)
        oldEntry3 = SearchResults.objects.create(headline='test3', link='www.test3.com', source='newsapi')
        oldEntry3.request.add(old_query)

        # checking if these results have been added to database
        self.assertTrue(oldEntry1 in SearchResults.objects.filter(request='virus'))
        self.assertTrue(oldEntry2 in SearchResults.objects.filter(request='virus'))
        self.assertTrue(oldEntry3 in SearchResults.objects.filter(request='virus'))

        response = self.client.post(reverse('news:searchNews'), {'kw': 'virus'})

        # checking if the results have been removed
        self.assertFalse(oldEntry1 in SearchResults.objects.filter(request='virus'))
        self.assertFalse(oldEntry2 in SearchResults.objects.filter(request='virus'))
        self.assertFalse(oldEntry3 in SearchResults.objects.filter(request='virus'))
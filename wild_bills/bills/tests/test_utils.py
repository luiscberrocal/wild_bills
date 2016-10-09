from datetime import date, datetime

from django.test import TestCase

from ..utils import FrequencyCalculator, frequency_calculator


class TestFrequencyCalculator(TestCase):

    def test_next_week(self):
        cdate = datetime(2015,11,22)
        fc = FrequencyCalculator()
        next_week = fc.get_next_week_date(cdate, 'saturday')
        self.assertEqual(date(2015, 11, 28), next_week)

    def test_next_month(self):
        cdate = datetime(2015,11,22)
        fc = FrequencyCalculator()
        next_week = fc.get_next_month_date(cdate)
        self.assertEqual(date(2015, 12, 22), next_week)

    def test_next_month_feb(self):
        cdate = datetime(2015,1,30)
        fc = FrequencyCalculator()
        next_week = fc.get_next_month_date(cdate)
        self.assertEqual(date(2015, 2, 28), next_week)

    def test_next_singleton_month_feb(self):
        cdate = datetime(2015,1,30)
        next_week = frequency_calculator.get_next_month_date(cdate)
        self.assertEqual(date(2015, 2, 28), next_week)

    def test_get_next_closest(self):
        cdate = datetime(2015,11,12)
        next_closest = frequency_calculator.get_next_closest(cdate, [15, 30])
        self.assertEqual(date(2015, 11, 15), next_closest)

        cdate = datetime(2015,11,15)
        next_closest = frequency_calculator.get_next_closest(cdate, [15, 30])
        self.assertEqual(date(2015, 11, 30), next_closest)

        cdate = datetime(2015,11,16)
        next_closest = frequency_calculator.get_next_closest(cdate, [15, 30])
        self.assertEqual(date(2015, 11, 30), next_closest)

    def test_get_next_loop(self):
        # cdate = datetime(2015,11,12)
        # next_closest = frequency_calculator.get_next_closest(cdate, [15, 30])
        # self.assertEqual(date(2015, 11, 15), next_closest)
        #
        # next_closest = frequency_calculator.get_next_closest(next_closest, [15, 30])
        # self.assertEqual(date(2015, 11, 30), next_closest)
        ref_date = datetime(2015,11,30)
        next_closest = frequency_calculator.get_next_closest(ref_date, [15, 30])
        self.assertEqual(date(2015, 12, 15), next_closest)

    def test_get_next_closest_single(self):
        cdate = datetime(2015,11,12)
        next_closest = frequency_calculator.get_next_closest(cdate, [15])
        self.assertEqual(date(2015, 11, 15), next_closest)

        cdate = datetime(2015,11,15)
        next_closest = frequency_calculator.get_next_closest(cdate, [15])
        self.assertEqual(date(2015, 12, 15), next_closest)

    def test_get_next_closest_feb(self):
        cdate = datetime(2015,2,16)
        next_closest = frequency_calculator.get_next_closest(cdate, [15, 30])
        self.assertEqual(date(2015, 2, 28), next_closest)

    def test__build_deloreans(self):
        cdate = datetime(2015,3,16)
        d_dates = frequency_calculator._build_deloreans(cdate, [15, 30])
        self.assertEqual(date(2015, 3, 15), d_dates[0].date)
        self.assertEqual(date(2015, 3, 30), d_dates[1].date)

    def test__build_deloreans_feb(self):
        cdate = datetime(2015,2,16)
        d_dates = frequency_calculator._build_deloreans(cdate, [15, 30])
        self.assertEqual(date(2015, 2, 15), d_dates[0].date)
        self.assertEqual(date(2015, 2, 28), d_dates[1].date)


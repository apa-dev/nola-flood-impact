from django.conf import settings


class FloodImpactCalculator(object):
        """
        a simple rainfall runoff calculator, based on this model:
        https://en.wikipedia.org/wiki/Runoff_curve_number
        """

        def __init__(self, cover_type, area_square_feet, rainfall=1.5):
            self.soil_type = 'D'  # not yet used in the model
            self.cover_type = cover_type
            self.area_square_feet = area_square_feet
            self.rainfall = rainfall

        @property
        def runoff_curve_number(self):
                return next(ct[2] for ct in settings.COVER_TYPES if ct[0] == self.cover_type)

        @property
        def soil_retention(self):
                """max soil moisture retention... this is "S" in the model"""
                return (1000 / self.runoff_curve_number) - 10

        def calc_runoff(self, rainfall=1.5):
                return ((rainfall - (0.2 * self.soil_retention))**2) / (rainfall + (0.8 * self.soil_retention))

        def calc_runoff_volume(self, rainfall=1.5):
                """ calculates runoff volume in cubic feet """
                return self.calc_runoff(rainfall) * (1/12) * self.area_square_feet

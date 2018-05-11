
COVER_TYPES = (
	# (IDENTIFIER, Title, Runnoff curve number) 
	# see: https://en.wikipedia.org/wiki/Runoff_curve_number
	('IMPERVIOUS', 'Impervious Area', 98),
	('OPEN_SPACE', 'Open Space - Average', 85),
	('COMMERCIAL', 'Commercial / Business', 95),
	('INDUSTRIAL', 'Industrial', 93),
	('URBAN_RES', 'Urban Residential: <1/8 acre', 92),
	('SUBURBAN_RES_SMALL', 'Suburban Residential: <1/4 acre', 87),
	('SUBURBAN_RES_LARGE', 'Suburban Residential: 1/3 acre', 86),
	('RURAL_RES_SMALL', 'Rural Residential: 1/2 acre', 85),
	('RURAL_RES_MID', 'Rural Residential: 1 acre', 84),
	('RURAL_RES_LARGE', 'Rural Residential: 2 acre', 82),
	)

class FloodImpactCalculator(object):
	"""
	a simple rainfall runoff calculator, based on this model: 
	https://en.wikipedia.org/wiki/Runoff_curve_number
	"""
	soil_type = 'D' # not yet used in the model
	cover_type = 'URBAN_RES' # default to urban res
	area_square_feet = 5197 # default for example/testing purposes

	@property
	def runoff_curve_number(self):
		return next(ct[2] for ct in COVER_TYPES if ct[0]==self.cover_type)

	@property
	def soil_retention(self):
		"""max soil moisture retention... this is "S" in the model"""
		return (1000/self.runoff_curve_number)-10

	def calc_runoff(self, rainfall=1.5):
		return ((rainfall - (0.2*self.soil_retention))**2 ) / (rainfall + (0.8*self.soil_retention))

	def calc_runoff_volume(self, rainfall=1.5):
		""" calculates runoff volume in cubic feet """
		return self.calc_runoff(rainfall) * (1/12) * self.area_square_feet



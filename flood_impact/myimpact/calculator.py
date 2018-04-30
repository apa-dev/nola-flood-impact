COVER_TYPES = (
	('IMPERVIOUS', 'Impervious Area'),
	('OPEN_SPACE', 'Open Space - Average'),
	('COMMERCIAL', 'Commercial / Business'),
	('INDUSTRIAL', 'Industrial'),
	('URBAN_RES', 'Urban Residential: <1/8 acre'),
	('SUBURBAN_RES_SMALL', 'Suburban Residential: <1/4 acre'),
	('SUBURBAN_RES_LARGE', 'Suburban Residential: 1/3 acre'),
	('RURAL_RES_SMALL', 'Rural Residential: 1/2 acre'),
	('RURAL_RES_MID', 'Rural Residential: 1 acre'),
	('RURAL_RES_LARGE', 'Rural Residential: 2 acre'),
	)


class FloodImpactCalculator(object):
	soil_type = 'D' # not yet used
	cover_type = 'URBAN_RES' # default to urban res



	def calculate(self):
		pass
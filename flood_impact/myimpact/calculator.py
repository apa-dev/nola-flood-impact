
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

# Mapping models.ZoningDistrict.zone_description to a COVER_TYPE Identifier
NOLA_ZONING_COVER_TYPE_MAPPING = {
        "Auto-Oriented Commercial District"                                             : "COMMERCIAL",
        "Business-Industrial Park District"                                             : "INDUSTRIAL",
        "CBD-1 Core Central Business District"                                          : "COMMERCIAL",
        "CBD-2 Historic Commercial and Mixed-Use District"                              : "COMMERCIAL",
        "CBD-3 Cultural Arts District"                                                  : "COMMERCIAL",
        "CBD-4 Exposition District"                                                     : "COMMERCIAL",
        "CBD-5 Urban Core Neighborhood Lower Intensity Mixed-Use District"              : "URBAN_RES",
        "CBD-6 Urban Core Neighborhood Mixed-Use District"                              : "URBAN_RES",
        "CBD-7 Bio-Science District"                                                    : "INDUSTRIAL",
        "Educational Campus District"                                                   : "SUBURBAN_RES_LARGE",
        "General Commercial District"                                                   : "COMMERCIAL",
        "General Planned Development District"                                          : "COMMERCIAL",
        "Greenway Open Space District"                                                  : "OPEN_SPACE",
        "Heavy Commercial District"                                                     : "COMMERCIAL",
        "Heavy Industrial District"                                                     : "INDUSTRIAL",
        "High Intensity Mixed-Use"                                                      : "COMMERCIAL",
        "High Intensity Mixed-Use District"                                             : "COMMERCIAL",
        "Historic Marigny/Trem?/Bywater Commercial District"                            : "COMMERCIAL",
        "Historic Marigny/Trem?/Bywater Mixed-Use District"                             : "COMMERCIAL",
        "Historic Marigny/Trem?/Bywater Residential District"                           : "URBAN_RES",
        "Historic Urban Multi-Family Residential District"                              : "URBAN_RES",
        "Historic Urban Neighborhood Business District"                                 : "COMMERCIAL",
        "Historic Urban Neighborhood Mixed-Use District"                                : "COMMERCIAL",
        "Historic Urban Single-Family Residential District"                             : "URBAN_RES",
        "Historic Urban Two-Family Residential District"                                : "URBAN_RES",
        "Life Science Mixed-Use District"                                               : "INDUSTRIAL",
        "Light Industrial District"                                                     : "INDUSTRIAL",
        "Maritime Industrial District"                                                  : "INDUSTRIAL",
        "Maritime MIxed-Use District"                                                   : "COMMERCIAL",
        "Medical Campus District"                                                       : "INDUSTRIAL",
        "Medical Service District"                                                      : "INDUSTRIAL",
        "Medium Intensity Mixed-Use District"                                           : "COMMERCIAL",
        "Natural Areas District"                                                        : "OPEN_SPACE",
        "Neighborhood Open Space District"                                              : "OPEN_SPACE",
        "Regional Open Space District"                                                  : "OPEN_SPACE",
        "Rural Residential Estate District"                                             : "RURAL_RES_MID",
        "Suburban Business District"                                                    : "COMMERCIAL",
        "Suburban Lake Area General Commercial District"                                : "COMMERCIAL",
        "Suburban Lake Area High-Residential District"                                  : "SUBURBAN_RES_SMALL",
        "Suburban Lake Area High-Rise Multi-Family Residential District"                : "SUBURBAN_RES_SMALL",
        "Suburban Lake Area Low-Rise Multi-Family Residential District"                 : "SUBURBAN_RES_SMALL",
        "Suburban Lake Area Marina District"                                            : "COMMERCIAL",
        "Suburban Lake Area Neighborhood Business District"                             : "COMMERCIAL",
        "Suburban Lake Area Neighborhood Park District"                                 : "OPEN_SPACE",
        "Suburban Lake Vista Two-Family Residential District"                           : "SUBURBAN_RES_SMALL",
        "Suburban Lake Vista and Lake Shore Single-Family Residential District"         : "SUBURBAN_RES_LARGE",
        "Suburban Lakeview Single-Family Residential District"                          : "SUBURBAN_RES_LARGE",
        "Suburban Lakewood and Country Club Gardens Single-Family Residential District" : "SUBURBAN_RES_LARGE",
        "Suburban Lakewood/Parkview Two-Family Residential District"                    : "SUBURBAN_RES_LARGE",
        "Suburban Multi-Family Residential District"                                    : "SUBURBAN_RES_SMALL",
        "Suburban Neighborhood Mixed-Use District"                                      : "COMMERCIAL",
        "Suburban Pedestrian-Oriented Corridor Business District"                       : "COMMERCIAL",
        "Suburban Single-Family Residential District"                                   : "SUBURBAN_RES_LARGE",
        "Suburban Two-Family Residential District"                                      : "SUBURBAN_RES_LARGE",
        "Vieux Carr? Commercial District"                                               : "COMMERCIAL",
        "Vieux Carr? Entertainment District"                                            : "COMMERCIAL",
        "Vieux Carr? Park District"                                                     : "OPEN_SPACE",
        "Vieux Carr? Residential District"                                              : "URBAN_RES",
        "Vieux Carr? Service District"                                                  : "INDUSTRIAL"
        }

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



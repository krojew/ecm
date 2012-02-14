# Copyright (c) 2010-2011 Robin Jarry
#
# This file is part of EVE Corporation Management.
#
# EVE Corporation Management is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# EVE Corporation Management is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# EVE Corporation Management. If not, see <http://www.gnu.org/licenses/>.

__date__ = "2011 11 2"
__author__ = "diabeteman"


ENRICHED_URANIUM_TYPEID = 44
OXYGEN_TYPEID = 3683
MECHANICAL_PARTS_TYPEID = 3689
COOLANT_TYPEID = 9832
ROBOTICS_TYPEID = 9848
LIQUID_OZONE_TYPEID = 16273
HEAVY_WATER_TYPEID = 16272
STRONTIUM_CLATHRATES_TYPEID = 16275

HELIUM_ISOTOPES_TYPEID = 16274
OXYGEN_ISOTOPES_TYPEID = 17887
NITROGEN_ISOTOPES_TYPEID = 17888
HYDROGEN_ISOTOPES_TYPEID = 17889

CALDARI_RACEID = 1
MINMATAR_RACEID = 2
AMARR_RACEID = 4
GALLENTE_RACEID = 8

RACE_TO_ISOTOPE = {
    CALDARI_RACEID: NITROGEN_ISOTOPES_TYPEID,
    MINMATAR_RACEID: HYDROGEN_ISOTOPES_TYPEID,
    AMARR_RACEID: HELIUM_ISOTOPES_TYPEID,
    GALLENTE_RACEID: OXYGEN_ISOTOPES_TYPEID,
}
ISOTOPE_TO_RACE = {
    NITROGEN_ISOTOPES_TYPEID: CALDARI_RACEID,
    HYDROGEN_ISOTOPES_TYPEID: MINMATAR_RACEID,
    HELIUM_ISOTOPES_TYPEID: AMARR_RACEID,
    OXYGEN_ISOTOPES_TYPEID: GALLENTE_RACEID,
}
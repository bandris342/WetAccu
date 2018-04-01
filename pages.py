# -*- coding: utf-8 -*-

# Copyright(C) 2018      bandris342
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from weboob.browser.pages import JsonPage, HTMLPage
from weboob.browser.filters.json import Dict
from weboob.browser.elements import ItemElement, method, DictElement
from weboob.capabilities.weather import Forecast, Current, City, Temperature
from weboob.browser.filters.standard import Format, CleanText, CleanDecimal
from datetime import date

class CityPage(JsonPage):
    ENCODING = 'utf-8'

    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            klass = City

            obj_id = Dict('Key')
            obj_name = Format('%s (%s - %s)',
                              Dict('LocalizedName'),
                              Dict['AdministrativeArea']['LocalizedName'],
                              Dict['Country']['LocalizedName'])



class CurrentPage(HTMLPage):

    @method
    class get_current(ItemElement):
        klass = Current

        obj_date = date.today()

        def obj_temp(self):

             temp = CleanDecimal('//*[@id="day-part"]/div[2]/span[1]/b')(self)
             return Temperature(temp, 'C')

        obj_text = Format('%s - Wind from the %s - Humidity %s - Pressure %s',
                          CleanText('//*[@id="day-part"]/p[1]'),
                          CleanText('//*[@class="d-wrap wind"]/p/span/text()[2]'),
                          CleanText('//*[@id="details"]/div[5]/p'),
                          CleanText('//*[@id="day-part"]/p[2]/text()'))





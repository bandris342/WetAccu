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
from weboob.browser.elements import ItemElement, ListElement, method, DictElement
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
            obj_name = Format('%s, %s, %s',
                              Dict('LocalizedName'),
                              Dict['AdministrativeArea']['LocalizedName'],
                              Dict['Country']['LocalizedName'])



class CurrentPage(HTMLPage):

    @method
    class get_current(ItemElement):
        klass = Current

        obj_date = date.today()

        def obj_temp(self):

             temp = CleanDecimal('//*[@class="current temp-block"]/span[1]/b')(self)
             return Temperature(temp, 'C')

        obj_text = Format('%s - Wind from the %s - Humidity %s - Pressure %s',
                          CleanText('//*[@class="cond"]'),
                          CleanText('//*[@class="d-wrap wind"]/p/span/text()[2]'),
                          CleanText('//*[@class="d-wrap hum"]/p'),
                          CleanText('//*[@class="info pressure"]/text()'))


class ForecastPage(HTMLPage):

    @method
    class iter_forecast(ListElement):
        item_xpath = '//*[@id="extended"]/ul/li[position()=3 or (12>position() and position()>4) or (20>position() and position()>12)]'

        class item(ItemElement):
            klass = Forecast

            obj_date = Format('%s  %s',
                              CleanText('./a/dl/dt/b'),
                              CleanText('./a/dl/dt/text()[2]'))
            obj_id = obj_date

            obj_text = Format('- %s - Precipitation %s',
                              CleanText('./a/dl/dd[2]'),
                              CleanText('./a/dl/dd[1]/em'))

            # In the late afternoon (forecast "Tonight") only the Min temperature is shown
            def obj_low(self):
                low_text = CleanText('./a/dl/dd[1]/b')(self)
                if low_text:
                    temp = CleanDecimal('./a/dl/dd[1]/b')(self)
                    return Temperature(temp, 'C')
                else:
                    temp = CleanDecimal('./a/dl/dd[1]/strong')(self)
                    return Temperature(temp, 'C')

            def obj_high(self):
                low_text = CleanText('./a/dl/dd[1]/b')(self)
                if low_text:
                    temp = CleanDecimal('./a/dl/dd[1]/strong')(self)
                    return Temperature(temp, 'C')

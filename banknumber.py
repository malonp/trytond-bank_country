##############################################################################
#
#    GNU Condo: The Free Management Condominium System
#    Copyright (C) 2016- M. Alonso <port02.server@gmail.com>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


def countries():
    '''
    Return the list of country's codes that have check function
    '''

    res = [x.replace('check_code_', '').upper() for x in globals()
          if x.startswith('check_code_')]
    res.sort()
    return res


def check_code(country, account):
    '''
    Check bank code for the given country which should be a
    two digit ISO 3166 code.
    '''
    try:
        checker = globals()['check_code_%s' % country.lower()]
    except KeyError:
        return False
    return checker(account)

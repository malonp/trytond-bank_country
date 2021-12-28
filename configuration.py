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

from trytond.model import ModelSingleton, ModelSQL, ModelView, fields

HAS_BANKNUMBER = False
BANK_COUNTRIES = []
try:
    from . import banknumber

    HAS_BANKNUMBER = True
    for country in banknumber.countries():
        BANK_COUNTRIES.append(country)

except ImportError:
    import logging

    logging.getLogger('bank_validation').warning('Unable to import banknumber. Bank code validation disabled.')


__all__ = ['BankConfiguration', 'BankAccountConfiguration']


class BankConfiguration(ModelSingleton, ModelSQL, ModelView):
    'Bank Configuration'
    __name__ = 'bank.configuration-bank'

    bank_country = fields.Many2One(
        'country.country',
        'Bank Country',
        domain=[('code', 'in', BANK_COUNTRIES)],
        help=('The value set on this field will preset the country on new ' 'banks'),
    )


class BankAccountConfiguration(ModelSingleton, ModelSQL, ModelView):
    'Bank Configuration'
    __name__ = 'bank.configuration-account'

    account_currency = fields.Many2One(
        'currency.currency',
        'Account Currency',
        help=('The value set on this field will preset the currency on new ' 'bankaccounts'),
    )

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

from stdnum import iban
from trytond.model import ModelSQL, ModelView, Unique, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Bool, Eval, Not

from . import banknumber
from .configuration import BANK_COUNTRIES, HAS_BANKNUMBER

__all__ = ['Bank', 'BankAccount', 'BankAccountNumber', 'BankAccountParty']


class Bank(metaclass=PoolMeta):
    __name__ = 'bank'
    country = fields.Many2One(
        'country.country',
        'Country',
        domain=[('code', 'in', BANK_COUNTRIES)],
        help='Select country to enter national identification number for this bank',
    )
    code = fields.Char(
        'National Code',
        help='National Identifier Code for this bank',
        depends=['bic', 'country'],
        states={'invisible': Not(Bool(Eval('country'))), 'required': Not(Bool(Eval('bic')))},
    )

    @classmethod
    def __setup__(cls):
        super(Bank, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [('bank_uniq', Unique(t, t.country, t.code), 'This bank already exists!')]

    @classmethod
    def search_rec_name(cls, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op, ('party',) + tuple(clause[1:]), ('bic',) + tuple(clause[1:]), ('code',) + tuple(clause[1:])]

    @staticmethod
    def default_country():
        Configuration = Pool().get('bank.configuration-bank')
        config = Configuration(1)
        if config.bank_country:
            return config.bank_country.id


class BankAccount(metaclass=PoolMeta):
    __name__ = 'bank.account'

    currency = fields.Many2One('currency.currency', 'Currency')

    @staticmethod
    def default_currency():
        Configuration = Pool().get('bank.configuration-account')
        config = Configuration(1)
        if config.account_currency:
            return config.account_currency.id


class BankAccountNumber(metaclass=PoolMeta):
    __name__ = 'bank.account.number'

    @classmethod
    def __setup__(cls):
        super(BankAccountNumber, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('bankaccountnumber_uniq', Unique(t, t.type, t.number_compact), 'This bank account number already exists!')
        ]
        cls._error_messages.update({'invalid_iban': 'Invalid IBAN "%s".', 'invalid_bban': 'Invalid BBAN "%s".'})

    @fields.depends('type', 'number')
    def pre_validate(self):
        super(BankAccountNumber, self).pre_validate()
        '''
        Check the Bank number depending of the country.
        '''
        if self.type == 'iban' and self.number and HAS_BANKNUMBER:
            bban = iban.compact(self.number)[4:]
            if not getattr(banknumber, 'check_code_' + self.number[:2].lower())(bban):
                self.raise_user_error('invalid_bban', bban)

    @classmethod
    def validate(cls, bankaccountnumbers):
        super(BankAccountNumber, cls).validate(bankaccountnumbers)
        for bankaccountnumber in bankaccountnumbers:
            bankaccountnumber.iban_not_empty()

    def iban_not_empty(self):
        if self.type == 'iban' and not self.number:
            self.raise_user_error('IBAN value is empty')


class BankAccountParty(metaclass=PoolMeta):
    __name__ = 'bank.account-party.party'

    @classmethod
    def __setup__(cls):
        super(BankAccountParty, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('bankaccountowner_uniq', Unique(t, t.account, t.owner), 'The party is already owner of this account!')
        ]

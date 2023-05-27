import argparse
import sys
from math import log, ceil


def time_format(month):
    year, month = divmod(month, 12)
    text = ''
    if year:
        text += f"{year} year{'s' * (year > 1)}"
    if year and month:
        text += ' and '
    if month:
        text += f"{month} month{'s' * (month > 1)}"
    return text


def pos_float(str_num):
    num = float(str_num)
    if num < 0:
        raise ValueError
    return num


def pos_int(str_num):
    num = int(str_num)
    if num < 0:
        raise ValueError
    return num

#
# class ArgumentParser2(argparse.ArgumentParser):
#     def error(self, message):
#         print('Incorrect parameters')
#         raise self.exit()
#

parser = argparse.ArgumentParser(exit_on_error=False)
parser.add_argument('--type', choices=['annuity', 'diff'])
parser.add_argument('--payment', type=pos_int)
parser.add_argument('--principal', type=pos_int)
parser.add_argument('--interest', type=pos_float)
parser.add_argument('--periods', type=pos_int)

try:
    args = parser.parse_args()#'--type=annuity --principal=1000000 --payment=104000'.split())
    payment = args.payment
    months = args.periods
    interest = args.interest and args.interest / 12 / 100
    principal = args.principal

    if args.type == 'annuity' and interest:
        if not principal:
            principal = payment * (1 - (1 + interest)**-months) / interest
            principal = ceil(principal)
            print(f'Your loan principal = {principal}!')
        elif not payment:
            payment = principal * interest / (1 - (1 + interest)**-months)
            payment = ceil(payment)
            print(f'Your monthly payment = {payment}!')
        elif not months:
            months = -log(1 - interest * principal / payment, 1 + interest)
            months = ceil(months)
            print(f'It will take {time_format(months)} to repay this loan!')
        else:
            raise ValueError
        print('Overpayment =', months * payment - principal)

    elif args.type == 'diff' and interest and not payment:
        ppn = principal / months
        sum_diff_p = 0
        for m in range(1, months + 1):
            diff_payment = ppn * (1 + interest * (months - (m - 1)))
            diff_payment = ceil(diff_payment)
            sum_diff_p += diff_payment
            print(f'Month {m}: payment is', diff_payment)
        print('Overpayment =', sum_diff_p - principal)

    else:
        raise ValueError

except (argparse.ArgumentError, ValueError):
    print('Incorrect parameters')


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import datetime
from dateutil.parser import parse


def download():
    fromDate, toDate = getDatesFromArgs()

    while(fromDate < toDate):
        url = f'https://hupx.hu/hu/id/market_data/export.xlsx?date={fromDate}'

        response = requests.get(url)
        assert(response.status_code == 200)

        filename_with_path = f"HUPX_ID_{fromDate}.xlsx"
        with open(filename_with_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        fromDate += datetime.timedelta(days=1)


def getDatesFromArgs():
    parser = argparse.ArgumentParser(
        description='Download the HUPX ID data.')
    parser.add_argument('from_date', nargs='?')
    parser.add_argument('to_date', nargs='?')

    args = vars(parser.parse_args())
    if args['from_date']:
        fromDateTimeLocal = parse(args['from_date'])
        if args['to_date']:
            toDateTimeLocal = parse(args['to_date'])
        else:
            toDateTimeLocal = fromDateTimeLocal + datetime.timedelta(days=1)
    else:
        raise RuntimeError('Invalid date!')

    return fromDateTimeLocal, toDateTimeLocal


if __name__ == '__main__':
    download()

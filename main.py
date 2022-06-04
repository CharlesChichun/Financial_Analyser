import argparse
from parso import parse
# from postman_crawler import IS_M_QUAR, wholeState


def get_parser():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument('-i', '--industry', default="")
    parser.add_argument('-c', '--company', type=int, nargs="+")
    parser.add_argument('-y', '--year', type=int, help="query year")
    parser.add_argument('-s', '--season', type=int)
    parser.add_argument(
        '-e', '--email', help='email address to receive the result')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print(args.company)
    companies = args.company
    # wholeState(companies, IS_M_QUAR).to_excel

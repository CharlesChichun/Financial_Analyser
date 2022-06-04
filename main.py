import argparse
from finaAnalysis import genPLEL, genPivot, drawROPlot, writeResultExcel
from email_handler import send_mail_with_excel
from postman_crawler import BS_M_QUAR, IS_M_QUAR, wholeState
import pandas as pd


def get_parser():
    parser = argparse.ArgumentParser(description='my description')
    parser.add_argument('-i', '--industry', default="")
    parser.add_argument('-c', '--company', type=int, nargs="+")
    parser.add_argument('-y', '--year', type=int, help="query year")
    parser.add_argument('-q', '--quarter', help="Q1, Q2, Q3 or Q4")
    parser.add_argument('-e', '--email', required=True,
                        help='email address to receive the result')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    companies = args.company
    email = args.email
    year = args.year
    quarter = args.quarter
    industry = args.industry

    eSUBJECT = 'Financial Analyser Result'
    eCONTENT = 'The attachment is a report of financial analysis from '\
        'Financial Analyser of following companies: \n %s' % (
            str(companies))

    print("Start querying data ...")
    df_BS = wholeState(companies, BS_M_QUAR)
    df_IS = wholeState(companies, IS_M_QUAR)
    df_BS.to_excel('df_BS.xlsx')
    df_IS.to_excel('df_IS.xlsx')
    df_BS = pd.read_excel('df_BS.xlsx')
    df_IS = pd.read_excel('df_IS.xlsx')

    df_pro, df_liq, df_eff, df_lev = genPLEL(
        df_BS, df_IS, year, quarter=quarter, industry=industry)
    p1, p2 = genPivot(df_IS)

    roePath = drawROPlot(df_IS=df_IS, df_BS=df_BS,
                         industry=industry, stype="ROE")
    roaPath = drawROPlot(df_IS=df_IS, df_BS=df_BS,
                         industry=industry, stype="ROA")

    writeResultExcel("./FA_result.xlsx",
                     dfs=[df_pro, df_liq, df_eff, df_lev], ps=[p1, p2], imgPaths=[roePath, roaPath])

    send_mail_with_excel(email, eSUBJECT, eCONTENT, 'FA_result.xlsx')
    print("分析完成 !!!")
    print("已經結果寄至: %s" % (email))

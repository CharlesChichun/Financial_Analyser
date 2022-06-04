from http.client import InvalidURL
import pandas as pd
from postman_crawler import IS_M_QUAR, BS_M_QUAR, companyState, wholeState
import matplotlib.pyplot as plt


# to show chinese in plt
# https://tw511.com/a/01/22453.html
plt.rcParams['font.sans-serif'] = 'Arial Unicode MS'
plt.rcParams['axes.unicode_minus'] = False


def Ratio_Q(df_BS, df_IS, year, quarter=None, industry=None):
    cri_IS = pd.Series(dtype=bool)
    cri_BS = pd.Series(dtype=bool)
    if quarter != None:
        if industry != None:
            cri_IS = (df_IS["年份"] == year) & (
                df_IS["季度"] == quarter) & (df_IS["產業"] == industry)
            cri_BS = (df_BS["年份"] == year) & (
                df_BS["季度"] == quarter) & (df_BS["產業"] == industry)
        else:
            cri_IS = (df_IS["年份"] == year) & (df_IS["季度"] == quarter)
            cri_BS = (df_BS["年份"] == year) & (df_BS["季度"] == quarter)
    else:
        if industry != None:
            cri_IS = (df_IS["年份"] == year) & (df_IS["產業"] == industry)
            cri_BS = (df_BS["年份"] == year) & (df_BS["產業"] == industry)
        else:
            cri_IS = df_IS["年份"] == year
            cri_BS = df_BS["年份"] == year

    df_IS_1 = df_IS[cri_IS]
    df_BS_1 = df_BS[cri_BS]

    df_all = df_IS_1.merge(df_BS_1, on=["公司", "股票代號", "產業", "年份", "季度"])
    df_some = df_all[["公司", "股票代號", "產業", "年份", "季度", "營業收入", "營業成本", "營業毛利", "營業利益", "財務成本", "稅前淨利", "稅後淨利",
                      "每股稅後盈餘(元)", "現金及約當現金", "應收帳款", "存貨", "流動資產合計", "資產總額", "短期借款", "應付帳款", "流動負債合計", "長期借款", "股東權益總額"]]

    return df_some


def cal_ratio(df, quarter=None):

    if quarter != None:
        df["Name"] = df["公司"]
        df["Ticker"] = df["股票代號"]
        df["Gross Margin"] = df["營業毛利"] / df["營業收入"]
        df["Operating Margin"] = df["營業利益"] / df["營業收入"]
        df["Net Margin"] = df["稅後淨利"] / df["營業收入"]
        df["EPS (NTD)"] = df["每股稅後盈餘(元)"]
        df["ROE"] = df["稅後淨利"] / df["股東權益總額"]
        df["ROA"] = df["稅後淨利"] / df["資產總額"]
        df["Current Ratio"] = df["流動資產合計"] / df["流動負債合計"]
        df["Quick Ratio"] = (df["流動資產合計"] - df["存貨"]) / df["流動負債合計"]
        df["Interest Coverage Ratio"] = (df["稅前淨利"] + df["財務成本"]) / df["財務成本"]
        df["DSO"] = 365 / (df["營業收入"] / df["應收帳款"])
        df["DIO"] = 365 / (df["營業成本"] / df["存貨"])
        df["DPO"] = 365 / (df["營業成本"] / df["應付帳款"])
        df["CCC"] = df["DSO"] + df["DIO"] + df["DPO"]
        df["Debt to Equity Ratio"] = (df["短期借款"] + df["長期借款"]) / df["股東權益總額"]
        df["Net Debt to Equity Ratio"] = (
            df["短期借款"] + df["長期借款"] - df["現金及約當現金"]) / df["股東權益總額"]
    else:
        df = df.groupby(["公司", "股票代號", "產業", "年份"]).agg({
            "營業收入": "sum",
            "營業成本": "sum",
            "營業毛利": "sum",
            "營業利益": "sum",
            "財務成本": "sum",
            "稅前淨利": "sum",
            "稅後淨利": "sum",
            "每股稅後盈餘(元)": "sum",
            "現金及約當現金": "mean",
            "應收帳款": "mean",
            "存貨": "mean",
            "流動資產合計": "mean",
            "資產總額": "mean",
            "短期借款": "mean",
            "應付帳款": "mean",
            "長期借款": "mean",
            "流動負債合計": "mean",
            "股東權益總額": "mean", })
        df = df.rename_axis(["公司", "股票代號", "產業", "年份"]).reset_index()
        df["Name"] = df["公司"]
        df["Ticker"] = df["股票代號"]
        df["Gross Margin"] = df["營業毛利"] / df["營業收入"]
        df["Operating Margin"] = df["營業利益"] / df["營業收入"]
        df["Net Margin"] = df["稅後淨利"] / df["營業收入"]
        df["EPS (NTD)"] = df["每股稅後盈餘(元)"]
        df["ROE"] = df["稅後淨利"] / df["股東權益總額"]
        df["ROA"] = df["稅後淨利"] / df["資產總額"]
        df["Current Ratio"] = df["流動資產合計"] / df["流動負債合計"]
        df["Quick Ratio"] = (df["流動資產合計"] - df["存貨"]) / df["流動負債合計"]
        df["Interest Coverage Ratio"] = (df["稅前淨利"] + df["財務成本"]) / df["財務成本"]
        df["DSO"] = 365 / (df["營業收入"] / df["應收帳款"])
        df["DIO"] = 365 / (df["營業成本"] / df["存貨"])
        df["DPO"] = 365 / (df["營業成本"] / df["應付帳款"])
        df["CCC"] = df["DSO"] + df["DIO"] + df["DPO"]
        df["Debt to Equity Ratio"] = (df["短期借款"] + df["長期借款"]) / df["股東權益總額"]
        df["Net Debt to Equity Ratio"] = (
            df["短期借款"] + df["長期借款"] - df["現金及約當現金"]) / df["股東權益總額"]

    return df


# Profitability Liquidity Efficiency Leverage
def genPLEL(df_BS, df_IS, year, quarter=None, industry=None):
    result = Ratio_Q(df_BS, df_IS, year=year,
                     quarter=quarter, industry=industry)

    df = cal_ratio(result, quarter=quarter)

    df_pro = df.loc[:, ["Name", "Ticker", "Gross Margin",
                        "Operating Margin", "Net Margin", "EPS (NTD)", "ROE", "ROA"]]
    df_liq = df.loc[:, ["Name", "Ticker", "Current Ratio",
                        "Quick Ratio", "Interest Coverage Ratio"]]
    df_eff = df.loc[:, ["Name", "Ticker", "DSO", "DIO", "DPO", "CCC"]]
    df_lev = df.loc[:, ["Name", "Ticker",
                        "Debt to Equity Ratio", "Net Debt to Equity Ratio"]]

    return df_pro, df_liq, df_eff, df_lev


def genPivot(df_IS):
    p1 = pd.pivot_table(data=df_IS, index=["產業", "公司"], columns=[
        "年份", "季度"], values="營業收入")
    p2 = pd.pivot_table(data=df_IS, index=["產業", "公司"], columns=[
        "年份", "季度"], values="稅後淨利")
    return p1, p2


# stype = "ROE" or "ROA"
def drawROPlot(df_BS, df_IS, industry="半導體業", stype="ROE"):
    if industry == None:
        industry = df_BS["產業"][0]

    df_all = df_IS.merge(df_BS, on=["公司", "股票代號", "產業", "年份", "季度"])
    df_some = df_all[["公司", "股票代號", "產業", "年份", "季度", "營業收入", "營業成本", "營業毛利", "營業利益", "財務成本", "稅前淨利", "稅後淨利",
                      "每股稅後盈餘(元)", "現金及約當現金", "應收帳款", "存貨", "流動資產合計", "資產總額", "短期借款", "應付帳款", "流動負債合計", "長期借款", "股東權益總額"]]
    df_plt = cal_ratio(df_some)
    df_plt_indus = df_plt[df_plt["產業"] == industry]
    corps = list(df_plt_indus["公司"].unique())

    for corp in corps:
        df_plt_corp = df_plt_indus[df_plt_indus["公司"] == corp]
        plt.plot("年份", stype, data=df_plt_corp)
    plt.xlabel("year")
    plt.ylabel(stype)
    plt.title("%s %s" % (industry, stype))
    plt.legend(corps)
    figPath = './result/%s_%s.png' % (industry, stype)
    plt.savefig(figPath)
    plt.close()
    return figPath


def writeResultExcel(outPath, dfs, ps, imgPaths):
    with pd.ExcelWriter(outPath, engine='xlsxwriter') as writer:

        df_pro, df_liq, df_eff, df_lev = dfs
        p1, p2 = ps

        workbook = writer.book
        worksheet = workbook.add_worksheet('analysis')
        writer.sheets['analysis'] = worksheet
        df_pro.to_excel(writer, sheet_name='analysis', index=False,
                        startrow=1, startcol=0)
        df_liq.to_excel(writer, sheet_name='analysis', index=False,
                        startrow=1, startcol=9)
        df_eff.to_excel(writer, sheet_name='analysis', index=False,
                        startrow=1, startcol=15)
        df_lev.to_excel(writer, sheet_name='analysis', index=False,
                        startrow=1, startcol=22)
        worksheet.set_column("A:AA", 25)
        cell_format = workbook.add_format()
        cell_format.set_font_size(20)
        worksheet.write(0, 0, "Profitability", cell_format)
        worksheet.write(0, 9, "Liquidity", cell_format)
        worksheet.write(0, 15, "Efficiency", cell_format)
        worksheet.write(0, 22, "Leverage", cell_format)

        worksheet = workbook.add_worksheet('pivot')
        writer.sheets['pivot'] = worksheet
        p1.to_excel(writer, sheet_name='pivot',
                    startrow=1, startcol=0)
        p2.to_excel(writer, sheet_name='pivot',
                    startrow=10, startcol=0)

        worksheet = workbook.add_worksheet('charts')
        writer.sheets['pivot'] = worksheet
        worksheet.insert_image('A1', imgPaths[0])
        worksheet.insert_image('L1', imgPaths[1])
    pass


if __name__ == "__main__":
    companies = [2329, 2330, 2337, 2338]
    df_BS = wholeState(companies, BS_M_QUAR)
    df_IS = wholeState(companies, IS_M_QUAR)
    # df_IS = pd.read_excel('./df_IS.xlsx')
    # df_BS = pd.read_excel('./df_BS.xlsx')
    df_pro, df_liq, df_eff, df_lev = genPLEL(df_BS, df_IS, 2020)
    p1, p2 = genPivot(df_IS)

    roePath = drawROPlot(df_IS=df_IS, df_BS=df_BS,
                         industry="半導體業", stype="ROE")
    roaPath = drawROPlot(df_IS=df_IS, df_BS=df_BS,
                         industry="半導體業", stype="ROA")

    # writeResultExcel("./FA_result.xlsx",
    #                  dfs=[df_pro, df_liq, df_eff, df_lev], ps=[p1, p2], imgPaths=[roePath, roaPath])

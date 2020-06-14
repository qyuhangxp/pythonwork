import akshare as ak
import fund_em_qiao

a = fund_em_qiao.fund_market_price()
print(a)









stock_zh_a_spot_df = ak.stock_zh_a_spot()
print(stock_zh_a_spot_df)

a=stock_zh_a_spot_df
b = a[1,1]
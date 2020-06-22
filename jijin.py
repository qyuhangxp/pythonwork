import akshare as ak
import fund_em_qiao



a=fund_em_qiao.fund_openend_status()
a=a.set_index('基金代码')
b=fund_em_qiao.fund_em_value_estimation()
b=b.set_index('基金代码')
c=a.join(b,lsuffix='_left', rsuffix='_right')




stock_zh_a_spot_df = ak.stock_zh_a_spot()
print(stock_zh_a_spot_df)

a=stock_zh_a_spot_df
b = a[1,1]


from bs4 import BeautifulSoup
import requests
url = 'http://hb.ahzwfw.gov.cn/bsdt/config/ssqdDeptInfoList.do?xzqh=340600000000&_=1519280920117'
#result={}
html=requests.get(url)

list=html.json()
for a in list:
	print(a)


fund_em_value_estimation_df = ak.fund_em_value_estimation()
print(fund_em_value_estimation_df)
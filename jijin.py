import requests
from bs4 import BeautifulSoup
import akshare as ak
import fund_em_qiao
import pandas as pd
import smtplib
import schedule
import time

#计算折溢价基金数据
def fund_premium_discount():
    a = fund_em_qiao.fund_openend_status()
    b = fund_em_qiao.fund_em_value_estimation()
    c = fund_em_qiao.fund_market_price_2()

    a = a.set_index('基金代码')  # 将基金代码转为index
    b = b.drop(["基金类型", "基金名称"], axis=1)  # 删除基金类型和基金名称列，因为与a重复了
    b = b.set_index('基金代码')  # 将基金代码转为index
    c = c.drop(["基金名称"], axis=1)  # 删除基金名称列，因为与a重复了
    c = c.set_index('基金代码')  # 将基金代码转为index
    ab = a.join(b, lsuffix='_left', rsuffix='_right')  # ab结合
    abc = ab.join(c, lsuffix='_left', rsuffix='_right')  # abc结合
    fund_value = abc.reset_index()  # 恢复index和基金名称列
    fund_value.dropna(subset=['成交额'], inplace=True)  # 删除成交额中的空值行（没有成交也没有套利价值）
    fund_value.dropna(subset=['估算值'], inplace=True)  # 删除估算值中的空值行没有估算值没有套利参照）
    fund_value = fund_value[fund_value['估算值'] != '---']  # 删除估算值中的空值行（没有估算值没有套利参照）
    fund_value = fund_value[fund_value['成交额'] > 100000]  # 删除成交额中的小于10万的行（没有成交也没有套利价值）
    fund_value['最新价']=pd.to_numeric(fund_value['最新价'])#转浮点数
    fund_value['估算值']=pd.to_numeric(fund_value['估算值'])#转浮点数
    fund_value['手续费']=pd.to_numeric(fund_value['手续费'].map(lambda x: x.rstrip('%')))#转浮点数
    fund_value['折溢价']=(fund_value['最新价']-fund_value['估算值'])/fund_value['最新价']*100-fund_value['手续费']#计算折溢价
    fund_premium=fund_value[fund_value['折溢价']>0]#筛选出存在溢价的基金
    fund_discount=fund_value[fund_value['折溢价']<0]#筛选出存在折价的基金
    fund_premium=fund_premium[fund_premium['申购状态']!='暂停申购']#去掉暂停申购的溢价基金（因为无法套利）
    fund_discount=fund_discount[fund_discount['赎回状态']!='暂停赎回']#去掉暂停赎回的折价基金（因为无法套利）
    fund_premium=fund_premium.sort_values(by='折溢价',ascending=False)
    fund_discount=fund_discount.sort_values(by='折溢价')
    fund_premium.to_excel('溢价基金.xlsx')
    fund_discount.to_excel('折价基金.xlsx')
    return

def send_email():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication

    if __name__ == '__main__':

        fromaddr = '1323286788@qq.com'
        password = 'ocdbtpuomqkujbgi'
        toaddrs = ['1323286788@qq.com']
        content = 'hello, this is email content.'
        textApart = MIMEText(content)
        elsxFile = '溢价基金.xlsx'
        elsxApart = MIMEApplication(open(elsxFile, 'rb').read())
        elsxApart.add_header('Content-Disposition', 'attachment', filename=elsxFile)
        elsxFile_2 = '折价基金.xlsx'
        elsxApart_2 = MIMEApplication(open(elsxFile_2, 'rb').read())
        elsxApart_2.add_header('Content-Disposition', 'attachment', filename=elsxFile_2)
        m = MIMEMultipart()
        m.attach(textApart)
        m.attach(elsxApart)
        m.attach(elsxApart_2)
        m['Subject'] = '折溢价基金'  # 邮件标题
        m['To'] = 'qyuhangxp@hotmail.com'  # 收件人
        m['From'] = '1323286788@qq.com' # 发件人
        try:
            server = smtplib.SMTP('smtp.qq.com')
            server.login(fromaddr, password)
            server.sendmail(fromaddr, toaddrs, m.as_string())
            print('success')
            server.quit()
        except smtplib.SMTPException  as e:
            print('error:', e)  # 打印错误

schedule.every().day.at("21:48").do(fund_premium_discount)
schedule.every().day.at("21:49").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(30)
import pandas as pd
import os
import base64
import re
import numpy as np
import matplotlib.pyplot as plt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

path = '/home/flamingo/Documents/web_scraping/stockproject/'

def find_number(s):
    num = re.findall(r'[+]*[-]*[\d]+.[\d]+', str(s))
    print(num)
    if len(num) > 0 :
        return float(num[0])
    else:
        return float(0.01)
def organize_data(path):
    if(os.path.exists('flow.csv') and os.path.isfile('flow.csv')):
        flow = pd.read_csv(path + 'flow.csv')
        flow['time_stamp'] = flow.current_timestamp.str.split(" ", expand = True)[3]
        flow['time_stamp'] = flow['time_stamp'].str[0:2]
        flow['percentage_change'] = flow.price_change.str.split(",", expand = True)[2]
        print(list(flow['percentage_change']))
        flow['percentage_change'] = flow.percentage_change.apply(find_number)
        print(list(flow['percentage_change']))
        flow = flow[['stock_name',
            'time_stamp',
            'prev_close',
            'open',
            'intraday_price',
            'price_change',
            'percentage_change',
            'market_cap',
            'earnings_date',
            'pe_ratio',
            'volume',
            'volume_avg',
            'est_yr_target',
            'range_day',
            'range_52weeks',
            'fwd_div_yield',
            'exp_div_date',
            'eps',
            'beta_5yr_monthly',
            'ask',
            'bid']]
        print(flow[['price_change','percentage_change']])

        
        if(os.path.exists('stock.csv') and os.path.isfile('stock.csv')):
            stock = pd.read_csv(path+'stock.csv')
            stock = pd.concat([stock,flow], ignore_index=True)
            stock.to_csv(path+'stock.csv')
        else: 
            flow.to_csv(path+'stock.csv')
        os.remove('flow.csv')
    else:
        print('web scraping Error')
    return flow
        
def highlight_stock(df):
    email_df = df[(df['percentage_change'] > 0.2) | (df['percentage_change'] < -0.2)]
    if email_df.shape[0] > 0:
        #store the volatile stock name and their percentage change
        stock_lst = tuple(email_df['stock_name'])
        price_lst = tuple(email_df['percentage_change'])
        
        #present some plots
        plt.bar(list(email_df['stock_name']), list(email_df['percentage_change']))
        plt.xlabel("Stock Name")
        plt.ylabel("Percentage Change")
        plt.title('Volatile Stock Change')
        plt.xticks(rotation=30, ha='right')
        plt.savefig(path+'stock_plot.png',bbox_inches='tight',dpi=100)


        mail_from = 'Sender Email'
        mail_to = 'Receiver Email'
        mail_sub = 'Volatile Stock'

        content = 'Here are the stock names that has daily fructuation larger than 1% '+ \
                    '</hr>' + \
                    '<table><tbody>' +\
                    '<th>The volatile stock list</th>'
            
        for i in range(len(stock_lst)):
            content += '<tr><td>' + stock_lst[i] + '</td>' 
            content += '<td>' + str(price_lst[i]) + '</td></tr>' 
        content += '</tbody></table>'
        msg = Mail(mail_from,mail_to,mail_sub,html_content = content)
        
        with open('stock_plot.png', 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('stock_plot.png'),
            FileType('iamge/png'),
            Disposition('attachment')
        )
        msg.attachment = attachedFile

        try:
            sg = SendGridAPIClient('Your SendGrid API Key')
            response = sg.send(msg)
        except Exception as e:
            print(f'Error sending email: {e}.')
        else:
            print('Email sent successfully')
            print(response.status_code)
            print(response.body)


flow = organize_data(path)
highlight_stock(flow)
import json
import csv,os,requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
def main():

    file_path=input('输入文件名：');
    file_json=open(file_path,mode='r',encoding='utf-8');
    city_list=json.load(file_json);
    city_list.sort(key=lambda city:city['aqi'])
    top5_list=city_list[:5]
    wf=open('top5.json',mode='w');
    json.dump(top5_list,wf,ensure_ascii=False);
    wf.close();


def csvmain():
    f=open('beijing_aqi.json',mode='r',encoding='utf-8');
    city_list=json.load(f);
    city_list.sort(key=lambda city:city['aqi']);

    lines=[];
    lines.append(city_list[0].keys());

    for city in city_list:
        lines.append(city.values());

    wf=open('citycsv.csv',mode='w',encoding='utf-8',newline='');
    wr=csv.writer(wf);
    for line in lines:
        wr.writerow(line);
    wf.close();


#4.0

def process_json_file(filepath):

    with open(filepath, mode='r', encoding='utf-8') as f:
        city_list_json=json.load(f)
    return city_list_json;

def process_csv_file(filepath):
    city_list_csv=[];
    with open(filepath, mode='r', encoding='utf-8',newline='') as f:

        rd=csv.reader(f);
        for row in rd:
            city_list_csv.append(row)

    return city_list_csv;

def main4():
    file_path=input('请输出文件：')
    filename,fileext=os.path.splitext(file_path)

    if fileext=='.json':
        process_json_file(file_path);
    elif fileext=='.csv':
       print(process_csv_file(file_path)) ;
    else:
        print('暂不支持该文件类型')


def main5():
    city_name=input('请输入城市拼音:')

    url='http://pm25.in/'+city_name

    r=requests.get(url,timeout=30);
    print(r,r.status_code,r.text)

def main6():

    city_list=get_city_list();

    # total_list = [];
    # for city in city_list:
    #     city_name=city[0];
    #     city_link=city[1]
    #     aqi_val=get_aqi_value(city_link);
    #     row=[city_name]+aqi_val
    #     total_list.append(row)

    head=['city','AQI','PM2.5/1h','PM10/1h','CO/1h','NO2/1h','O3/1h','O3/8h','SO2/1h']

    with open('city_aqi.csv',mode='w',encoding='utf-8',newline='') as f:
        wr=csv.writer(f);
        wr.writerow(head)
        for i,city in enumerate(city_list):
            if (i+1)%10==0:
                print("已经保存{}条记录(共{}条记录)".format(i+1,len(city_list)))

            city_name=city[0]
            city_link = city[1]
            aqi_val=get_aqi_value(city_link);
            row=[city_name]+aqi_val;
            wr.writerow(row);

def get_city_list():
    url = 'http://pm25.in'
    r = requests.get(url, timeout=30)
    soup=BeautifulSoup(r.text,'lxml')
    city_list = []
    citys=soup.find_all('div',{'class':'bottom'})[1]
    city_link_list=citys.find_all('a')


    for city_link in city_link_list:
        city_name=city_link.text
        city_href=city_link['href'][1:]
        city_list.append((city_name,city_href))

    return city_list

def get_aqi_value(city_name):
    url='http://pm25.in/'+city_name
    r=requests.get(url,timeout=30);
    soup=BeautifulSoup(r.text,'lxml')
    div_list=soup.find_all('div',{'class':'span1'})

    aqi_list=[];
    for i in range(len(div_list)-1):
        ch_div=div_list[i]
        caption=ch_div.find('div',{'class':'caption'}).text.strip()
        value=ch_div.find('div',{'class':'value'}).text.strip()
        # aqi_list.append((caption,value))
        aqi_list.append(value)
    return aqi_list


def main8():
    aqi_data=pd.read_csv('city_aqi.csv')

    print(aqi_data.info())

    print(aqi_data.head())

    print(aqi_data['AQI'].max())

    print(aqi_data['AQI'].min())

    print(aqi_data['AQI'].mean())

    top10=aqi_data.sort_values(by=['AQI']).head(10)
    print(top10)

    # top10.to_csv('top_city.csv',index=False);

    clearTop10=top10 [top10['AQI']<15]

    print(clearTop10)

    top50_city=aqi_data.sort_values(by=['AQI']).head(50)

    top50_city.plot(kind='bar',x='city',y='AQI',title='空气最好的50个城市',figsize=(20,10))

    plt.savefig('top50_city.png');
    plt.show()

if __name__=='__main__':
    # main();
    main8();



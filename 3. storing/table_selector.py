# db 저장된 모든 테이블 불러오기

import pandas as pd
import pymysql

def selectdb2df(table,config,directory)->bool:
    
    '''
    esg db에서 저장된 특정 테이블을
    데이터프레임으로 추출한 후 csv로 저장하는 함수
    ----------------------------------------
    input : table명(Company,Product,Dart,News,Jobplanet,Patent)->str,
            config(config파일 저장경로)->str,
            directory(추출한 테이블 저장경로)->str
    output : 데이터프레임 및 csv파일
    '''
    
    # esg_ec2_config 파일 읽어오기
    db_config = {}
    with open(config, 'r') as f:
        for l in f.readlines():
            key, value = l.rstrip().split('=')
            db_config[key] = value

    print('DB 연결 시작 !')
    try:
        connect=pymysql.connect(**db_config
        )
        print('DB 접속 성공')
        
        #테이블 불러오기
        try:

            sql1 = 'select * from '+table
            result= pd.read_sql(sql1, connect)
            connect.close()
            print(table+' select 성공!')
            

        except Exception as e:
            print(e)


    except Exception as e:

        print(e)
        print('DB 접속 실패')
        
    result.to_csv(directory+'/'+table+'_tb.csv')
    
    return result

#if __name__=='__main_ _':
#  selectdb2df(table,directory)
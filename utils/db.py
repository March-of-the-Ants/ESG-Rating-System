#db접속 함수
#config : esg_test_config

def connectDB(config:str)->bool:
    
    '''
    esg db에 접속하는 함수
    ----------------------------------------
    input : config(config파일 저장경로),
    output : engine(db 접속엔진)
    
    '''
    from sqlalchemy import create_engine
    import pymysql #db connector, mysqldb는 맥에서 주로 사용


    # esg_ec2_config 파일 읽어오기
    db_config = {}
    with open(config, 'r') as f: #공유 드라이브 or 로컬
        for l in f.readlines():
            key, value = l.rstrip().split('=')
            db_config[key] = value
    #url 생성        
    engine=create_engine('mysql+pymysql://'+db_config['user']+':'+db_config['password']+'@'+db_config['host']+'/esg_all?'+db_config['charset']) #echo=True : 쿼리 찍기
    # db연결
    conn=engine.connect()
    print("db 연결성공")
    
    return engine


#db내 테이블 생성
#config : esg_test_config


def createTB(config,SQLfile)->bool:
    
    '''
    esg db에 테이블 생성하는 함수
    ----------------------------------------
    input 
    - config(config파일 저장경로)->str  
    
     'host': db 서버주소',
    'user': 사용자이름,
    'password': 사용자 비밀번호,
    'db': db 이름,
    'charset': db 인코딩,
    
    - SQLfile(테이블 생성 쿼리문 파일 저장경로)->str
    
        테이블 생성 쿼리문, ';'로 구분
    output 
    - 테이블 생성여부 print
    
    '''
    
    import pymysql
    from pymysql.constants import CLIENT
    import pandas as pd
    
    # esg_ec2_config 파일 읽어오기
    db_config = {}
    with open(config, 'r') as f: #공유 드라이브 or 로컬
        for l in f.readlines():
            key, value = l.rstrip().split('=')
            db_config[key] = value

    print('DB 연결 시작 !')
    try: 
        connect=pymysql.connect(**db_config, client_flag=CLIENT.MULTI_STATEMENTS
        ) #CLIENT.MULTI_STATEMENTS : 여러개 쿼리문 한꺼번에 처리가능
        print('DB 접속 성공')
        cursor=connect.cursor()
        
        sql=open(SQLfile).read()
        
        cursor.execute(sql)
        cursor.fetchall()
        connect.close() #연결해제
        
        print('테이블 생성 성공')

    except Exception as e:
        print(e)
    
    return 

#if __name__=='__main_ _':
#  selectdb2df(table,directory)


#db내 테이블 삽입 함수
#config : esg_test_config

def insertDB(config:str,table:str,df,opt:str)->bool:
    
    
    '''

    불러온 데이터프레임을 esg db에 삽입하는 함수
    ------------------------------------
    input 
    - config(config파일 저장경로)
    - table(삽입할 db 내 테이블 명)
    - df(삽입할 데이터프레임, pandas활용해서 불러온 상태)
    - opt(데이터 적재시 append : auto_increment or replace 선택)

    '''

    # db접속합수 connectDB(config) ->return : engine
    conn=connectDB(config).connect()
    try:
        df.to_sql(table, con=connectDB(config), if_exists=opt,index=False)
        print(table+" 테이블 삽입 완료")
        
    except Exception as e:
        print(e)
        print(table+" 테이블 삽입 실패")
  

    conn.close()


    return
    


#db내 테이블 조회 함수
#config : esg_test_config
def selectDB(config:str,table:str)->bool:
    
    
    '''

    특정 테이블을 esg db에서 조회하는 함수
    ------------------------------------
    input 
    - config(config파일 저장경로)
    - table(조회할 db 내 테이블 명)
    
    output
    - 조회결과 ->데이터프레임 

    '''

    # db접속합수 connectDB(config) ->return : engine
    try:
        conn=connectDB(config).connect()
        result=pd.read_sql_table(table, conn)
        print(table+" 테이블 조회 완료")
        
    except Exception as e:
        print(e)
        print(table+" 테이블 조회 실패")
  

    conn.close()


    return result
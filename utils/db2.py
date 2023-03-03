class esgDB:
    
    #db접속 생성자
    #config : esg_test_config

    def __init__(self,config:str)->any:
        
        '''
        생성자, esg db에 접속
        ----------------------------------------
        input : config(config파일 저장경로)
        - 'host': db 서버주소',
        - 'user': 사용자이름,
        - 'password': 사용자 비밀번호,
        - 'db': db 이름,
        - 'charset': db 인코딩,
        
        output : engine(db 접속엔진)
        
        '''
        from sqlalchemy import create_engine
        import pymysql #db connector, mysqldb는 맥에서 주로 사용
        from pymysql.constants import CLIENT


        # esg_ec2_config 파일 읽어오기
        db_config = {}
        with open(config, 'r') as f: #공유 드라이브 or 로컬
            for l in f.readlines():
                key, value = l.rstrip().split('=')
                db_config[key] = value
        #url 생성    
        self.engine=create_engine('mysql+pymysql://'+db_config['user']+':'+db_config['password']+'@'+db_config['host']+'/'+db_config['db']+'?'+db_config['charset'],
                             connect_args={"client_flag": CLIENT.MULTI_STATEMENTS}) #echo=True : 쿼리 찍기 #CLIENT.MULTI_STATEMENTS : 여러개 쿼리문 한꺼번에 처리가능
        # db연결
        self.conn=self.engine.connect() # 생성, 삽입, 조회시 공통으로 사용하는 값
        print("esg db 연결성공")
        
        return 
    
    def __del__(self)->str:
        '''
        소멸자, esg db와 접속 해지
        '''
        self.conn.close()
        print('esg db 연결해제')
        return 
    
    
    
    #db내 테이블 생성
    #config : esg_test_config
    
    def createTB(self,SQLfile:str)->str:
        
        '''
        esg db에 테이블 생성하는 함수
        ----------------------------------------
        input  
        - SQLfile(테이블 생성 쿼리문 파일 저장경로)->str
        
            테이블 생성 쿼리문, ';'로 구분
        output 
        - 테이블 생성여부 print
        
        '''
        
        import pymysql
        from pymysql.constants import CLIENT
        import pandas as pd
        from sqlalchemy import text
        
        try: 
            
            sql=open(SQLfile).read()
            escaped_sql = text(sql)
            self.engine.execute(escaped_sql)
            print('테이블 생성 성공')

        except Exception as e:
            print(e)
        
        return 
    
    #db내 테이블 삽입 함수
    #config : esg_test_config

    def insertDB(self,table:str,df,opt:str)->str:
        
        
        '''

        불러온 데이터프레임을 esg db에 삽입하는 함수
        ------------------------------------
        input 
        - table(삽입할 db 내 테이블 명)
        - df(삽입할 데이터프레임, pandas활용해서 불러온 상태)
        - opt(데이터 적재시 append : auto_increment or replace 선택)

        '''

        try:
            df.to_sql(table, self.engine, if_exists=opt,index=False)
            print(table+" 테이블 삽입 성공")
            
        except Exception as e:
            print(e)
            print(table+" 테이블 삽입 실패")


        return
    
    #db내 테이블 조회 함수
    #config : esg_test_config
    def selectDB(self,table:str)->any:
        
        
        '''

        특정 테이블을 esg db에서 조회하는 함수
        ------------------------------------
        input 
        - table(조회할 db 내 테이블 명)
        
        output
        - 조회결과 ->데이터프레임 

        '''

        import pandas as pd
        try:
            result=pd.read_sql_table(table, self.conn)
            print(table+" 테이블 조회 성공")
            
        except Exception as e:
            print(e)
            print(table+" 테이블 조회 실패")


        return result
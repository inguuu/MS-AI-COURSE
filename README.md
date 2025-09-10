

## ⚙️ 초기 설정

#### 1. Azure OpenAI 생성
- Azure OpenAI 생성
- Azure AI Foundry 보거나 키에서 확인
- 배포 하고 모델 코드 랑 맞추기
```bash
   response = openai.chat.completions.create(
        model="gpt-4.1-mini",  
        messages=messages,
        max_tokens= 1000,
        temperature= 0.7,
    )
```
- Azure AI Foundry 배포 내용 확인 후 `.env` 파일 환경 변수 맞추기

#### 2. VSCode에 Python 설정
- 필요 시 `pip install`로 패키지 설치
- 터미널에서 `where python`으로 경로 확인
- VSCode 명령 팔레트(ctrl + shift + p)에서 `> Python: Select Interpreter` 검색 후 경로 입력하여 설치된 Python 추가


#### 3. Streamlit 설정
- [https://streamlit.io/](https://streamlit.io/) 접속
- 회원가입 시 메일 입력은 건너뛰어도 됨
- [가이드](https://learn.microsoft.com/ko-kr/training/paths/create-custom-copilots-ai-studio/) 참조: 김영욱 강사님 https://github.com/KoreaEva

- 실행
```bash
streamlit run app.py
```

#### 4. AZURE AI SEARCH 생성
- AZURE AI SEARCH 생성
- index_setup.py 수정 후 실행 

## 📃 목표 구성 

![images](https://github.com/user-attachments/assets/b4838790-a7b9-4122-ab35-83c4af46635f)

### 🚀 Streamlit 배포

##### 런타임 및 배포 방식
- Runtime: Python 3.1
- 배포 유형: 코드 방식 (컨테이너 단위 배포 가능)

##### Azure Portal 설정
- 경로: Azure Portal > Marketplace > 웹 앱
- 배포 후 주소: `*.azurewebsites.net` (SSL 자동 적용)

##### 리소스 스펙
- Node는 가볍지만 Streamlit은 무거움 → P1V3 SKU 권장
- 설정 > 스케일 업/스케일 아웃에서 요금 및 로드 밸런싱 조절 가능

##### 배포 슬롯
- dev 슬롯 생성 후 복제본(appweb) 테스트
- 이상 없으면 swap으로 원본 교체

##### 배포 센터
- GitHub 연동 가능 → CI/CD 구성
- VSCode로 배포 시 배포 센터 설정 불필요

##### VSCode 배포
- Azure App Service 확장 설치 후 배포
- Azure 아이콘 클릭 > 추가 > 로그인 진행
- App Service 내 확인하기
- [Azure Web App에 Streamlit 배포하기](02.streamlit_deployment.md) 참조: 김영욱 강사님 https://github.com/KoreaEva
- Azure 포탈 > App Service > 구성 > 시작명령에 넣고 저장
```bash
bash /home/site/wwwroot/streamlit.sh
```
- streamlit.sh에 배포 .py 지정 및 pip 지정
- .env를 애저포탈 서비스 내 설정 > 환경변수로 대체해도 된다
- Azure 포탈 > App Service > 개요 > 다시시작
- 로그 스트림으로 확인하기

### 🔓 스토리지 생성, AI Seach (RAG)

![images](https://github.com/user-attachments/assets/04668e00-86fd-48c3-b2f2-c8c59aa8379b)

#### 1. Azure Portal > 스토리지 계정 > 만들기  
   - 기본서비스 Azure Blob Storage 또는 Azure Data Lake Storage Gen2 성능 표준, 중복도 LRS

#### 2. 스토리지 계정 > 데이터 스토리지 > 컨테이너 > 만들기  
   - 업로드한 파일을 blob이라 한다.
   - blob을 클릭하면 개요에 url 이나온다. (권한이 없으면 url입려해도 조회가 안된다)
   - 개요 > Blob 익명 액세스 > 사용 안 함(사용으로 변경)
   - 만든 컨테이너 들어가서 > 엑세스 수준 변경(blob 수준으로 많이 준다)

#### 3. Azure AI Search 만들기   
   - 켜 놓을때마다 과금됨(기본정도로 사용)
   - 기존 만든 OpenAI에 text-embedding-3-small 새로 배포

#### 4. 데이터 가져오기(정확히 일치)
   - 데이터소스: Azure blob Storage
   - 이름: pdf-dataset
   - 구분 분석 모드: 기본값
   - 연결 문자열: 스토리지계정 > 보안+네트워킹 > 엑세스 키 > 연결 문자열
   - 컨테이너 명 :컨테이너 명 넣기
   - 인덱스 단계 > 인덱스 입력, 키 그대로 기본으로 가면 됨
   - 인덱서 단계 > 일정 한번
     
#### 5. 데이터 가져오기 및 벡터화(유사도 까지)
   - Azure blob Storage > RAG
   - 데이터연결: (blob stoage관련 선택), 폴더(root라서), 고급설정 다 기본값, 
   - 텍스트 벡터화: (ai search 관련 선택), 가격관련 체크하기
   - 이미지 벡터화: 비우고 다음
   - 고급설정: 비우고 다음
   - 검토 및 만들기 : car2

### 💻 Computer Vision 
   -  마켓플레이스 > 'Azure ai 서비스' 리소스 바로 만들기
  ```bash
     pip install azure-ai-vision-imageanalysis
     pip install azure-core
  ```
1. **사진 분석 VisualFeatures**
 - TAGS → 키워드 목록 (이미지의 주요 특징)
 - CAPTION → 짧은 설명 문장
 - OBJECTS → 객체별 이름 + 위치 좌표 (시각화 가능)
 - 
2. **감정 분석**
 - Azure Language Studio
 - Azure > 마켓플레이스> '언어 서비스' 만들기

## AI Search 테스트 
 - https://github.com/MicrosoftLearning/mslearn-knowledge-mining
 - https://microsoftlearning.github.io/mslearn-knowledge-mining/Instructions/Exercises/01-azure-search.html#upload-documents-to-azure-storage

 - git clone https://github.com/MicrosoftLearning/mslearn-knowledge-mining
 - az cli 설치 후 로그인
 - UploadDocs.cmd (윈도우 기준) 설정
 - VSCODE 에서 테스트 하고 싶은 폴더 경로(01.aiserch ~~)에서 터미널로 실행  .\UploadDocs.cmd(그냥 스토리지에 직접 업로드해도됨)
 - AI SEARCH > 인덱스(데이터가져오기) > 위치이름,핵심구추출,언어검색,태그생성,캡션생성 (위의 가이드대로 따라해야함)
 - 인덱서, 인덱스 설정 완료 후 개요에 검색 탐색기로 테스트 > 보기: json view, 전체보려면 *로 검색
## 📘 강의 통해 배운 것

0. **sku(스쿠) = 사양**

1. **테넌트 (Tenant) = 디렉토리 (Directory)**
   - 아이디들의 집합
   - LIMIT 단위는 테넌트 기준
   - 구독(Subscription)들의 집합 → 비용 관리 단위
   - 그렇기에 리소스 나눠씀

2. **리소스 그룹 (Resource Group)**
   - 이름에 `rg`를 붙이는 관습이 있음
   - 지역(Region)은 리소스 그룹 생성 시 선택  
     → 이후 리소스들이 꼭 동일 지역에 있을 필요는 없음  
     → 세팅 정보 정도로만 사용

3. **가용성 옵션**
   - 복구 범위 선택 가능  
     - 데이터 센터 수준  
     - 리전(Region) 수준  
     - 국가(Nation) 수준

4. **네트워크 트래픽 비용**
   - 인바운드(Inbound): 상대적으로 저렴
   - 아웃바운드(Outbound): 인바운드보다 비쌈

5. **가상 네트워크 (Virtual Network)**
   - 이름에 `vnet`으로 시작하는 관습
   - 구조  
     1. 클라우드: 거대한 자원 풀  
     2. 테넌트: 여러 사용자/조직이 공유 → 각자 사용하도록 `vnet` 생성  
     3. `vnet`이 다르면 완전히 다른 네트워크 (팀/서비스 단위로도 큼)  
     4. `vnet` 내부를 `subnet`으로 세분화하여 관리
    
6. **전송 요청**
   - 서비스 호출 시 key, endpoint 를 넘기지 않고 최초만 넘기고 토큰으로 돌려준다
   - 예전에는 토큰이라 부르는데 key credential이라 많이 부른다(탈취 당해도 시간 제한)

7.  **이미지 가공**
   - 이미지(jpg, png 등) 분석해서 그리거나 다루려면 bitmap으로 나눠야 한다

8. **AI 서치와 AI 서비스는 같은 리전에 만들어야함**

9. **cli**
   - Command Line Interface
   - 자체 툴이 있음 > window는 MSI 파일로 설치
   - az 명령어 사용 가능해짐
   - 
10. **COSMOS DB**
   - 여러 디비 있음 postgre 등 다 있음
   - 실시간 복제
   - 로그 담지마라 돈 엄청 나옴

10. **파인 튜닝**
   - 맛집정보를 써야할까 절대 NO 맛집 바뀔때마다 계속 함
   - 컨텍스트랑 파인튜닝 같이 쓸대도 있다
   - 돈이 엄청든다 우리나라는 네이버 빼고 없고(한국어, 중국어, 일본, 영어 정도만 으로 줄인다)

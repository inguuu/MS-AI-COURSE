

## ⚙️ 초기 설정

#### 1. Azure OpenAI 만들기
- Azure OpenAI 만들고
- Azure AI Foundry 보거나 키에서 확인
- Azure AI Foundry 배포 내용 확인 후 `.env` 파일 환경 변수 맞추기

#### 2. VSCode에 Python 설정
- 필요 시 `pip install`로 패키지 설치
- 터미널에서 `where python`으로 경로 확인
- VSCode 명령 팔레트에서 `> Python: Select Interpreter` 검색 후 경로 입력하여 설치된 Python 추가

#### 3. Streamlit 설정
- [https://streamlit.io/](https://streamlit.io/) 접속
- 회원가입 시 메일 입력은 건너뛰어도 됨
- [가이드](https://learn.microsoft.com/ko-kr/training/paths/create-custom-copilots-ai-studio/) 참조: 김영욱 강사님 https://github.com/KoreaEva

- 실행
```bash
streamlit run app.py
```

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
   

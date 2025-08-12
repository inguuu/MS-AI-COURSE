

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

#### 4. Streamlit 배포

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
bash /home/sit/wwwroot/streamlit.sh
```
- Azure 포탈 > App Service > 개요 > 다시시작
- 로그 스트림으로 확인하기

## 📘 강의 통해 배운 것

1. **테넌트 (Tenant) = 디렉토리 (Directory)**
   - 아이디들의 집합
   - LIMIT 단위는 테넌트 기준
   - 구독(Subscription)들의 집합 → 비용 관리 단위

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

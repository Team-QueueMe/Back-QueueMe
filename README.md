# Back-QueueMe
클라우드시스템(001) 수업 QueueMe 프로젝트 백엔드 레포지토리 

## 실행 가이드 (for FE!)

### 필요한 것들
* Docker Desktop 설치 

### 환경 변수 세팅 
노션에 .env 파일 참고해주세요 

### backend server 실행 
터미널에서 프로젝트 루트 경로로 이동한 뒤 아래 명령어 실행 

```bash
docker-compose up --build
```
* **Swagger UI** [http://localhost:8000/docs](http://localhost:8000/docs)
* **API base:** `http://localhost:8000`

### 서버 종료하기 

```bash
docker-compose down
```

---
### 참고 
- **database**: PostgreSQL이 Docker 컨테이너로 함께 실행됩니다 (Port: 5432)
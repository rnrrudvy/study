## Flask Board

간단한 게시판 예제 애플리케이션입니다. `Flask`와 `SQLite`를 사용하며, 로컬 가상환경 실행과 Docker 컨테이너 실행을 모두 지원합니다.

### 요구 사항

- Python 3.13 (로컬 실행 시)
- Docker (컨테이너 실행 시)

### 로컬 실행 (가상환경)

```bash
cd "/Users/kpkuk/Library/CloudStorage/Dropbox/works/study/flask-board"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt  # 없으면 Flask 설치됨
python app.py
# 브라우저: http://127.0.0.1:5000
```

#### 시작/종료 스크립트 (로컬)

프로젝트에 로컬 개발용 스크립트가 포함되어 있습니다.

```bash
# 실행 (백그라운드, PID는 .flask.pid 저장)
./scripts/local-start.sh

# 종료 (PID 파일 우선, 없으면 5000 포트 기준)
./scripts/local-stop.sh
```

### Docker로 실행 (운영 권장 경로)

이미 만들어둔 `Dockerfile`을 사용해 이미지를 빌드하고 컨테이너로 실행할 수 있습니다.

```bash
cd "/Users/kpkuk/Library/CloudStorage/Dropbox/works/study/flask-board"

# 이미지 빌드
docker build -t flask-board:local .

# 컨테이너 실행 (호스트 5001 -> 컨테이너 5000)
docker run -d --name flask-board -p 5001:5000 --rm flask-board:local

# 로그 확인
docker logs -f flask-board

# 중지
docker stop flask-board

# 접속: http://127.0.0.1:5001
```

환경변수 `PORT`를 사용해 컨테이너 내부 포트를 변경할 수 있습니다. 기본값은 5000입니다.

```bash
docker run -d --name flask-board -e PORT=5000 -p 5001:5000 --rm flask-board:local
```

### 프로젝트 구조

```text
flask-board/
  app.py              # Flask 앱 및 라우트, DB 초기화
  templates/
    index.html        # 목록 페이지
    write.html        # 작성 페이지
  requirements.txt    # Python 의존성 (Flask)
  Dockerfile          # 컨테이너 빌드 정의
  .dockerignore       # 빌드 컨텍스트 제외 파일
  scripts/
    local-start.sh    # 로컬 실행 스크립트 (백그라운드)
    local-stop.sh     # 로컬 종료 스크립트
    container-start.sh# 컨테이너 실행 (이미지 없으면 자동 빌드)
    container-stop.sh # 컨테이너 중지
  tests/              # Python 단위 테스트
  tests-ui/           # Playwright E2E 테스트 (TypeScript)
  result/             # 테스트 결과 리포트 및 아티팩트
  requirements-dev.txt# 개발용 의존성 (테스트 등)
  node_modules/       # Node.js 의존성 (E2E 테스트용)
  .venv/              # Python 가상환경
```

### 주요 라우트

- `GET /`: 게시글 목록 조회
- `GET /write`: 글 작성 폼
- `POST /write`: 글 저장 후 목록으로 리다이렉트

### 데이터베이스

- `SQLite` 사용, 파일명은 `board.db`
- 앱 시작 시 테이블이 없으면 자동 생성됩니다.

### 참고

- 로컬 개발은 `flask` 개발 서버(`debug=True`), 컨테이너는 `gunicorn`으로 구동됩니다.
- 운영 배포 시에는 `gunicorn` 워커/스레드 수, 타임아웃, 로깅 등을 환경에 맞게 조정하세요.

#### 컨테이너 실행/중지 스크립트

```bash
# 실행 (이미지 없으면 자동 빌드)
./scripts/container-start.sh              # 기본: 5001 -> 5000
./scripts/container-start.sh 8080 5000    # 호스트/컨테이너 포트 지정

# 중지
./scripts/container-stop.sh
```

### 테스트

#### Python 단위 테스트

```bash
source .venv/bin/activate
pytest
```

#### E2E UI 테스트 (Playwright)

```bash
# Playwright 설치 (최초 1회)
npm install
# 테스트 실행
npx playwright test
# 리포트 보기
npx playwright show-report result/ui-report
```

- E2E 테스트는 회원가입, 로그인, 글쓰기, 삭제 등 주요 플로우를 자동화합니다.
- 결과 리포트는 result/ui-report 폴더에 생성됩니다.

### 개발 환경 참고

- Python 패키지는 requirements.txt, requirements-dev.txt로 관리합니다.
- Node.js 기반 E2E 테스트는 package.json, node_modules로 관리합니다.
- .venv, node_modules 등은 git에 포함되지 않습니다.

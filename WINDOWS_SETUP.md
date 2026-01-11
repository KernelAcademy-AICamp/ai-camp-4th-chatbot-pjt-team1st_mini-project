# 🪟 Windows 환경 설정 가이드

Mac에서 Windows로 환경을 변경하신 경우, 다음 단계를 따라주세요.

## 📋 필수 작업

### 1. 기존 가상환경 삭제 (Mac용 venv는 Windows에서 작동하지 않음)

```powershell
# PowerShell에서 실행
Remove-Item -Recurse -Force venv
```

또는 파일 탐색기에서 `venv` 폴더를 직접 삭제하세요.

### 2. Python 설치 확인

```powershell
python --version
```

Python 3.8 이상이 설치되어 있어야 합니다. 없다면 [python.org](https://www.python.org/downloads/)에서 다운로드하세요.

### 3. 가상환경 생성 및 패키지 설치

```powershell
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 패키지 설치
pip install -r requirements.txt
```

**참고**: PowerShell 실행 정책 오류가 발생하면:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. 앱 실행

#### 방법 1: run.bat 사용 (권장)
```powershell
.\run.bat
```

이 스크립트는 자동으로:
- 최신 코드를 가져옵니다 (git pull)
- 가상환경을 활성화합니다
- Streamlit 앱을 실행합니다

#### 방법 2: 수동 실행
```powershell
# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 앱 실행
python -m streamlit run app.py
```

## 🔧 추가 설정

### 자동 업데이트 (선택사항)

5분마다 자동으로 코드를 확인하고 업데이트하려면:
```powershell
.\auto_update.bat
```

## ⚠️ 주의사항

1. **경로 차이**: Windows는 `\`를 사용하고, Mac/Linux는 `/`를 사용합니다. 하지만 Python 코드는 대부분 자동으로 처리하므로 문제없습니다.

2. **가상환경 활성화**:
   - PowerShell: `.\venv\Scripts\Activate.ps1`
   - CMD: `venv\Scripts\activate.bat`

3. **한글 경로**: 현재 프로젝트 경로에 한글이 포함되어 있어도 Python은 잘 처리합니다.

## 🐛 문제 해결

### 가상환경 활성화가 안 될 때
```powershell
# PowerShell 실행 정책 확인
Get-ExecutionPolicy

# 실행 정책 변경 (필요시)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 패키지 설치 오류
```powershell
# pip 업그레이드
python -m pip install --upgrade pip

# 다시 설치
pip install -r requirements.txt
```

### Streamlit 실행 오류
```powershell
# Streamlit 재설치
pip install --upgrade streamlit

# 포트 변경 (기본 8501이 사용 중일 때)
streamlit run app.py --server.port 8502
```

## ✅ 확인 사항

설정이 완료되면 다음을 확인하세요:

- [ ] `python --version` 실행 시 Python 3.8+ 표시
- [ ] `venv` 폴더가 새로 생성됨
- [ ] `pip list` 실행 시 streamlit, anthropic 등 패키지 설치 확인
- [ ] `.\run.bat` 실행 시 브라우저에서 앱이 열림

## 📞 도움이 필요하신가요?

문제가 발생하면 다음 정보를 확인해주세요:
- Python 버전
- 에러 메시지 전체 내용
- 실행한 명령어

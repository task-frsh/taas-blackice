# 🧊 TAAS 결빙(블랙아이스) 교통사고 분석

TAAS 결빙 교통사고 다발지역 공공데이터를 지도·차트·표로 보여주는 무료 분석 웹사이트.

**🌐 라이브: https://taas-blackice.streamlit.app/**

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

브라우저에서 http://localhost:8501 자동 오픈.

## 현재 상태 (v1 MVP)
- [x] 스캐폴딩 + 샘플 데이터 렌더 검증
- [x] 실데이터(결빙사고 다발지역 95건, 2019~2023) 연결
- [x] GitHub 저장소: https://github.com/task-frsh/taas-blackice
- [x] Streamlit Community Cloud 배포 완료 → https://taas-blackice.streamlit.app/

## 데이터 갱신 방법
```bash
python src/collect.py   # TAAS API 재수집 → data/blackice.csv 갱신
```
(이 작업만 .env 의 TAAS_API_KEY 필요. 앱 실행/배포에는 키 불필요)

## 배포 (Streamlit Community Cloud)
1. https://share.streamlit.io 접속 → GitHub 로그인
2. "New app" → Repository: `task-frsh/taas-blackice`, Branch: `main`
3. **Main file path: `src/app.py`**
4. Deploy. (앱이 CSV만 읽으므로 Secrets 설정 불필요)

## 구조
```
taas_blackice/
├── src/app.py          # Streamlit 앱 (지도/차트/표)
├── data/
│   └── sample_blackice.csv   # 렌더 검증용 샘플
├── requirements.txt
├── PRD.md
└── README.md
```

## 데이터 출처
도로교통공단 TAAS / 공공데이터포털(data.go.kr). 공공데이터 이용약관 준수.

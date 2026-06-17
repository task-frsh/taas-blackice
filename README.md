# 🧊 TAAS 결빙(블랙아이스) 교통사고 분석

TAAS 결빙 교통사고 다발지역 공공데이터를 지도·차트·표로 보여주는 무료 분석 웹사이트.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

브라우저에서 http://localhost:8501 자동 오픈.

## 현재 상태 (v1 MVP)
- [x] 스캐폴딩 + 샘플 데이터 렌더 검증
- [ ] 실데이터(결빙사고 다발지역) 연결
- [ ] Streamlit Community Cloud 배포

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

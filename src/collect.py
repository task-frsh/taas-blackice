"""TAAS 결빙(노면) 교통사고 다발지역 수집기.

검증된 결빙 다발 지역(중부·산간 중심) × 최근 5년을 순회해 data/blackice.csv 로 저장.
결빙사고는 경기·강원·충청·경북 등 추운 내륙에 집중되어, 이 범위로 실데이터 대부분을 담는다.

실행:  python src/collect.py
"""
import sys
import time
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import get_taas_api_key  # noqa: E402

API_URL = "http://apis.data.go.kr/B552061/frequentzoneFreezing/getRestFrequentzoneFreezing"
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "blackice.csv"
YEARS = ["2023", "2022", "2021", "2020", "2019"]

# 법정동 시도(2자리) → 시군구(3자리) 코드. 결빙 다발 중부·산간권 위주.
REGION_CODES = {
    "11": ["110", "140", "170", "200", "215", "230", "260", "290", "305", "320",
           "350", "380", "410", "440", "470", "500", "530", "545", "560", "590",
           "620", "650", "680", "710", "740"],  # 서울
    "41": ["110", "130", "150", "170", "190", "210", "220", "250", "270", "280",
           "290", "310", "360", "370", "390", "410", "430", "450", "460", "480",
           "500", "550", "570", "590", "610", "630", "650", "670"],  # 경기
    "42": ["110", "130", "150", "170", "190", "210", "230", "720", "730", "750",
           "760", "770", "780", "790", "800", "810", "820", "830"],  # 강원
    "43": ["110", "130", "150", "720", "730", "740", "745", "750", "760", "770",
           "800"],  # 충북
    "44": ["130", "150", "180", "200", "210", "230", "250", "270", "710", "760",
           "770", "790", "800", "810", "825"],  # 충남
    "45": ["110", "130", "140", "180", "190", "210", "710", "720", "730", "740",
           "750", "770", "790", "800"],  # 전북
    "47": ["110", "130", "150", "170", "190", "210", "230", "250", "280", "290",
           "720", "730", "750", "760", "770", "820", "830", "840", "850", "900",
           "920", "930", "940"],  # 경북
    "48": ["120", "170", "220", "240", "250", "310", "330", "720", "730", "740",
           "820", "840", "850", "860", "870", "880", "890"],  # 경남
}

COLS = {
    "spot_nm": "지점명",
    "sido_sgg_nm": "시도시군구",
    "occrrnc_cnt": "발생건수",
    "caslt_cnt": "사상자수",
    "dth_dnv_cnt": "사망자수",
    "se_dnv_cnt": "중상자수",
    "sl_dnv_cnt": "경상자수",
    "la_crd": "위도",
    "lo_crd": "경도",
    "geom_json": "구역폴리곤",
}


def fetch(key: str, year: str, sido: str, gugun: str) -> list[dict]:
    params = {
        "serviceKey": key,
        "searchYearCd": year,
        "siDo": sido,
        "guGun": gugun,
        "type": "json",
        "numOfRows": "100",
        "pageNo": "1",
    }
    r = requests.get(API_URL, params=params, timeout=15)
    data = r.json()
    if int(data.get("totalCount") or 0) == 0:
        return []
    items = data["items"]["item"]
    rows = []
    for it in items:
        row = {dst: it.get(src) for src, dst in COLS.items()}
        row["연도"] = year
        rows.append(row)
    return rows


def main() -> None:
    key = get_taas_api_key()
    all_rows: list[dict] = []
    total_calls = sum(len(g) for g in REGION_CODES.values()) * len(YEARS)
    done = 0
    for year in YEARS:
        for sido, guguns in REGION_CODES.items():
            for gg in guguns:
                done += 1
                try:
                    rows = fetch(key, year, sido, gg)
                    if rows:
                        all_rows.extend(rows)
                        print(f"  [{done}/{total_calls}] {year} {sido}-{gg}: {len(rows)}건")
                except Exception as e:  # 일시 오류는 건너뛰고 계속
                    print(f"  [{done}/{total_calls}] {year} {sido}-{gg}: ERR {str(e)[:50]}")
                time.sleep(0.05)

    df = pd.DataFrame(all_rows)
    # 숫자 컬럼 정리
    for c in ["발생건수", "사상자수", "사망자수", "중상자수", "경상자수"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    for c in ["위도", "경도"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["위도", "경도"]).reset_index(drop=True)

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
    print(f"\n저장 완료: {DATA_PATH}")
    print(f"총 {len(df)}건 / 연도 {sorted(df['연도'].unique())} / 시도 {sorted(df['시도시군구'].str.split().str[0].unique())}")


if __name__ == "__main__":
    main()

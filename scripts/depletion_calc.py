#!/usr/bin/env python3
"""재고 소진 예상일과 변경 입고 예정일 대비 여유일수를 계산한다.

사용 예:
    python3 depletion_calc.py --current-stock 500 --daily-usage 40 \
        --safety-stock 50 --changed-eta 2026-08-10
"""
import argparse
import math
from datetime import date, datetime, timedelta


def main():
    parser = argparse.ArgumentParser(description="재고 소진일 / 생산 차질 가능성 계산")
    parser.add_argument("--current-stock", type=float, required=True, help="현재 재고 수량")
    parser.add_argument("--daily-usage", type=float, required=True, help="일평균 사용량")
    parser.add_argument("--safety-stock", type=float, default=0, help="안전재고 수준 (기본값 0)")
    parser.add_argument("--changed-eta", type=str, required=True, help="변경 입고 예정일 YYYY-MM-DD")
    parser.add_argument("--today", type=str, default=None, help="기준일 YYYY-MM-DD (기본값: 오늘)")
    args = parser.parse_args()

    today = datetime.strptime(args.today, "%Y-%m-%d").date() if args.today else date.today()
    changed_eta = datetime.strptime(args.changed_eta, "%Y-%m-%d").date()

    available_stock = args.current_stock - args.safety_stock

    if args.daily_usage <= 0:
        print("일평균 사용량이 0 이하라 재고 소진일을 계산할 수 없습니다. 입력값을 확인하세요.")
        return

    days_left = math.floor(available_stock / args.daily_usage)
    depletion_date = today + timedelta(days=max(days_left, 0))
    buffer_days = (depletion_date - changed_eta).days

    if available_stock < 0:
        severity = "위험"
        risk = "있음 (이미 안전재고 이하로 소진된 상태)"
    elif buffer_days >= 3:
        severity = "안전"
        risk = "낮음"
    elif buffer_days >= 0:
        severity = "주의"
        risk = "있음"
    else:
        severity = "위험"
        risk = "있음 (이미 공백 발생 예상)"

    print(f"가용재고(안전재고 차감): {available_stock:g}")
    print(f"재고 소진 예상일: {depletion_date.isoformat()}")
    print(f"변경 입고 예정일: {changed_eta.isoformat()}")
    print(f"여유일수: {buffer_days}일")
    print(f"생산 차질 가능성: {risk}")
    print(f"심각도: {severity}")


if __name__ == "__main__":
    main()

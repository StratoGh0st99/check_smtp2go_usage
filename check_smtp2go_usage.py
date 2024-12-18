#!/usr/bin/env python3

#Author: StratoGh0st99
#GitHub: https://github.com/StratoGh0st99/check_smtp2go_usage
#Icingaexchange: https://exchange.icinga.com/StratoGh0st99/check_smtp2go_usage

import sys
import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description="Check SMTP2Go current mail usage.")
    parser.add_argument("-a", "--api-key", required=True, help="SMTP2Go API key")
    parser.add_argument("-w", "--warn", required=True, type=float, help="Warn Percent")
    parser.add_argument("-c", "--crit", required=True, type=float, help="Crit Percent")
    args = parser.parse_args()

    api_key = args.api_key
    warn_percent = args.warn
    crit_percent = args.crit
    url = "https://api.smtp2go.com/v3/stats/email_summary"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-Smtp2go-Api-Key": api_key
    }

    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"CRITICAL - Error making request to SMTP2Go API: {e}")
        sys.exit(2)

    data = response.json()
    if "data" not in data:
        print("CRITICAL - Unexpected data format from SMTP2Go API.")
        sys.exit(2)

    stats = data["data"]
    mails_max = stats.get("cycle_max")
    mails_used = stats.get("cycle_used")

    if mails_max is None or mails_used is None:
        print("CRITICAL - Could not extract cycle_max or cycle_used.")
        sys.exit(2)

    usage_percentage = (mails_used / mails_max) * 100

    warn_mails = int(mails_max * (warn_percent / 100))
    crit_mails = int(mails_max * (crit_percent / 100))

    if usage_percentage >= crit_percent:
        status = "CRITICAL"
        exit_code = 2
    elif usage_percentage >= warn_percent:
        status = "WARNING"
        exit_code = 1
    else:
        status = "OK"
        exit_code = 0

    perf_data = (
        f"mails_used={mails_used};{warn_mails};{crit_mails};0;{mails_max} "
        f"usage_percent={usage_percentage:.2f}%;{warn_percent};{crit_percent};0;100"
    )

    print(f"{status} - {mails_used} of {mails_max} mails used ({usage_percentage:.2f}%) | {perf_data}")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
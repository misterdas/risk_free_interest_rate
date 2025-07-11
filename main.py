try:
    import requests
    import pandas as pd
    from selectolax.parser import HTMLParser
    from io import StringIO
except (ImportError, ModuleNotFoundError):
    __import__("os").system(
        f"{__import__('sys').executable} -m pip install -U requests selectolax pandas json"
    )
    import requests
    import pandas as pd
    from selectolax.parser import HTMLParser
    from io import StringIO

user_agent = requests.get(
    "https://misterdas.github.io/risk_free_interest_rate/user_agents.json"
).json()[-2]

headers = {
    "user-agent": user_agent,
}

def riskFreeInetrestRate(
    url: str = "https://www.rbi.org.in/",
) -> None:
    response = HTMLParser(requests.get(url, headers=headers).content)

    gov_sec_data = []

    for table in response.css("table"):
        if "91 day T-bills" in table.text():
            for row in table.css("tr"):
                cells = row.css("th, td")
                if len(cells) == 2:
                    name = cells[0].text().strip()
                    rate = cells[1].text().strip().replace(":", "").replace("%", "").replace("*", "").replace("#", "")
                    
                    if "as on" not in name.lower() and "cut-off" not in name.lower():
                        try:
                            gov_sec_data.append({
                                "GovernmentSecurityName": name,
                                "Percent": float(rate)
                            })
                        except ValueError:
                            pass
            break

    df = pd.DataFrame(gov_sec_data)

    # Save to JSON
    with open("RiskFreeInterestRate.json", "w") as jsonFile:
        jsonFile.write(df.to_json(orient='records'))

    # Optional: preview raw HTML if needed
    # print(df.to_string(index=False))

if __name__ == "__main__":
    riskFreeInetrestRate()

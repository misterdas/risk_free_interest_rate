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
    selector = "#wrapper > div:nth-child(10) > table"
    data = [node.html for node in response.css(selector)]

    # Fix FutureWarning with StringIO
    df = pd.read_html(StringIO(data[0]))[0].iloc[4:13]
    df.columns = ["GovernmentSecurityName", "Percent"]
    df.reset_index(inplace=True, drop=True)

    # Clean whitespace and symbols
    df["GovernmentSecurityName"] = df["GovernmentSecurityName"].str.strip()
    df["Percent"] = df["Percent"].str.strip('%#* :')

    # Remove rows where 'Percent' is not a valid float
    df = df[pd.to_numeric(df["Percent"], errors="coerce").notna()]

    # Now safely convert to float
    df = df.astype({'GovernmentSecurityName': 'str', 'Percent': 'float32'}, copy=False)

    # Save to JSON
    with open("RiskFreeInterestRate.json", "w") as jsonFile:
        jsonFile.write(df.to_json(orient='records'))

if __name__ == "__main__":
    riskFreeInetrestRate()

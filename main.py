try:
    import requests
    import pandas as pd
    from selectolax.parser import HTMLParser
except (ImportError, ModuleNotFoundError):
    __import__("os").system(
        f"{__import__('sys').executable} -m pip install -U requests selectolax pandas json"
    )
    import requests
    import pandas as pd
    from selectolax.parser import HTMLParser

user_agent = requests.get(
    "https://misterdas.github.io/risk_free_interest_rate/user_agents.json"
).json()[-2]

headers = {
    "user-agent": user_agent,
}
    
def riskFreeInetrestRate(
    url: str = "https://www.rbi.org.in/",
) -> None:
    response = HTMLParser(requests.get(url,headers=headers).content)
    selector = "#wrapper > div:nth-child(10) > table"
    data = [node.html for node in response.css(selector)]
    df = (pd.read_html(data[0])[0][4:13])
    df.columns = ["GovernmentSecurityName", "Percent"]
    df.reset_index(inplace=True,drop=True)
    df["GovernmentSecurityName"] = df["GovernmentSecurityName"].str.rstrip(' ').str.lstrip(' ')
    df["Percent"] = df["Percent"].str.rstrip('% #').str.rstrip('%*').str.lstrip(':  ')
    df = df.astype({'GovernmentSecurityName': 'str', 'Percent': 'float32'}, copy=False)
    with open("RiskFreeInterestRate.json", "w") as jsonFile:
        jsonFile.write(df.to_json(orient='records'))

if __name__ == "__main__":
    riskFreeInetrestRate()
    

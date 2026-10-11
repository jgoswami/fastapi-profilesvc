from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_create_and_get_portfolio_monthly_balance():
    payload = {
        "portfolio_month": "2026-10",
        "portfolio_date": "2026-10-11",
        "description": "Monthly snapshot",
        "robinhood_value": 1000.0,
        "schwab_jay_investment_value": 2000.0,
        "schwab_jay_ira_value": 3000.0,
        "alo_401k_value": 4000.0,
        "gap_401k_value": 5000.0,
        "chevron_401k_value": 6000.0,
        "schwab_varsha_investment_value": 7000.0,
        "schwab_jay_roth_value": 8000.0,
        "_529_kush_value": 9000.0,
        "_529_aadya_value": 10000.0,
        "marcus_account_value": 11000.0,
        "wells_fargo_value": 12000.0,
        "citibank_varsha_value": 13000.0,
        "axisbank_value": 14000.0,
        "mortgage_balance": 15000.0,
        "coinbase_value": 16000.0,
        "schwab_varsha_roth_value": 17000.0,
        "healthequity_fund_value": 18000.0,
        "gap_etrade_value": 19000.0,
        "monthly_expenses": 2000.0,
        "varsha_monthly_expenses": 2500.0,
        "india_home_value": 26000.0,
        "alo_ms_value": 27000.0,
        "networth": 0.0,
        "total_assets": 0.0,
        "total_liabilities": 0.0,
        "retirement_value": 0.0,
        "investment_amount": 0.0,
        "cash": 0.0,
        "distribution": 0.0,
        "potential_annual_earning": 0.0,
        "retirement_jay_amount": 0.0,
        "retirement_varsha_amount": 0.0,
        "investment_jay_amount": 0.0,
        "investment_varsha_amount": 0.0,
    }

    create_response = client.post("/portfolio-monthly-balance", json=payload)
    assert create_response.status_code == 200
    created = create_response.json()

    assert created["portfolio_month"] == "2026-10"
    assert created["retirement_jay_amount"] == 20000.0
    assert created["retirement_varsha_amount"] == 17000.0
    assert created["investment_jay_amount"] == 3000.0 + 2000.0 + 19000.0
    assert created["investment_varsha_amount"] == 7000.0 + 17000.0
    assert created["total_assets"] > 0
    assert created["total_liabilities"] > 0
    assert created["networth"] == created["total_assets"] - created["total_liabilities"]

    list_response = client.get("/portfolio-monthly-balance")
    assert list_response.status_code == 200
    assert any(item["portfolio_month"] == "2026-10" for item in list_response.json())


def test_jay_retirement_endpoint():
    payload = {
        "portfolio_month": "2026-11",
        "portfolio_date": "2026-11-01",
        "description": "Retirement check",
        "robinhood_value": 100.0,
        "schwab_jay_investment_value": 200.0,
        "schwab_jay_ira_value": 300.0,
        "alo_401k_value": 400.0,
        "gap_401k_value": 500.0,
        "chevron_401k_value": 600.0,
        "schwab_varsha_investment_value": 700.0,
        "schwab_jay_roth_value": 800.0,
        "_529_kush_value": 900.0,
        "_529_aadya_value": 1000.0,
        "marcus_account_value": 1100.0,
        "wells_fargo_value": 1200.0,
        "citibank_varsha_value": 1300.0,
        "axisbank_value": 1400.0,
        "mortgage_balance": 1500.0,
        "coinbase_value": 1600.0,
        "schwab_varsha_roth_value": 1700.0,
        "healthequity_fund_value": 1800.0,
        "gap_etrade_value": 1900.0,
        "monthly_expenses": 2000.0,
        "varsha_monthly_expenses": 2500.0,
        "india_home_value": 2600.0,
        "alo_ms_value": 2700.0,
        "networth": 0.0,
        "total_assets": 0.0,
        "total_liabilities": 0.0,
        "retirement_value": 0.0,
        "investment_amount": 0.0,
        "cash": 0.0,
        "distribution": 0.0,
        "potential_annual_earning": 0.0,
        "retirement_jay_amount": 0.0,
        "retirement_varsha_amount": 0.0,
        "investment_jay_amount": 0.0,
        "investment_varsha_amount": 0.0,
    }

    created = client.post("/portfolio-monthly-balance", json=payload).json()
    response = client.get(f"/portfolio-monthly-balance/{created['id']}/jay-retirement")
    assert response.status_code == 200
    assert response.json()["jay_retirement_value"] == 2000.0

import sqlite3
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

DB_PATH = "personal.db"

app = FastAPI()

# Serve static files (CSS, JS)
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

PORTFOLIO_MONTHLY_BALANCE_COLUMNS = [
    "portfolio_month",
    "portfolio_date",
    "description",
    "robinhood_value",
    "schwab_jay_investment_value",
    "schwab_jay_ira_value",
    "alo_401k_value",
    "gap_401k_value",
    "chevron_401k_value",
    "schwab_varsha_investment_value",
    "schwab_jay_roth_value",
    "_529_kush_value",
    "_529_aadya_value",
    "marcus_account_value",
    "wells_fargo_value",
    "citibank_varsha_value",
    "axisbank_value",
    "mortgage_balance",
    "coinbase_value",
    "schwab_varsha_roth_value",
    "healthequity_fund_value",
    "gap_etrade_value",
    "monthly_expenses",
    "varsha_monthly_expenses",
    "india_home_value",
    "alo_ms_value",
    "networth",
    "total_assets",
    "total_liabilities",
    "retirement_value",
    "investment_amount",
    "cash",
    "distribution",
    "potential_annual_earning",
    "retirement_jay_amount",
    "retirement_varsha_amount",
    "investment_jay_amount",
    "investment_varsha_amount",
]


class PortfolioCreate(BaseModel):
    id: int | None = None
    portfolio_month: str
    portfolio_date: date | None = None
    description: str | None = None
    robinhood_value: float = 0.0
    schwab_jay_investment_value: float = 0.0
    schwab_jay_ira_value: float = 0.0
    alo_401k_value: float = 0.0
    gap_401k_value: float = 0.0
    chevron_401k_value: float = 0.0
    schwab_varsha_investment_value: float = 0.0
    schwab_jay_roth_value: float = 0.0
    _529_kush_value: float = 0.0
    _529_aadya_value: float = 0.0
    marcus_account_value: float = 0.0
    wells_fargo_value: float = 0.0
    citibank_varsha_value: float = 0.0
    axisbank_value: float = 0.0
    mortgage_balance: float = 0.0
    coinbase_value: float = 0.0
    schwab_varsha_roth_value: float = 0.0
    healthequity_fund_value: float = 0.0
    gap_etrade_value: float = 0.0
    monthly_expenses: float = 0.0
    varsha_monthly_expenses: float = 0.0
    india_home_value: float = 0.0
    alo_ms_value: float = 0.0
    networth: float = 0.0
    total_assets: float = 0.0
    total_liabilities: float = 0.0
    retirement_value: float = 0.0
    investment_amount: float = 0.0
    cash: float = 0.0
    distribution: float = 0.0
    potential_annual_earning: float = 0.0
    retirement_jay_amount: float = 0.0
    retirement_varsha_amount: float = 0.0
    investment_jay_amount: float = 0.0
    investment_varsha_amount: float = 0.0


class PortfolioItem(PortfolioCreate):
    id: int


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def portfolio_row_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "portfolio_month": row["portfolio_month"],
        "portfolio_date": row["portfolio_date"],
        "description": row["description"],
        "robinhood_value": row["robinhood_value"],
        "schwab_jay_investment_value": row["schwab_jay_investment_value"],
        "schwab_jay_ira_value": row["schwab_jay_ira_value"],
        "alo_401k_value": row["alo_401k_value"],
        "gap_401k_value": row["gap_401k_value"],
        "chevron_401k_value": row["chevron_401k_value"],
        "schwab_varsha_investment_value": row["schwab_varsha_investment_value"],
        "schwab_jay_roth_value": row["schwab_jay_roth_value"],
        "_529_kush_value": row["_529_kush_value"],
        "_529_aadya_value": row["_529_aadya_value"],
        "marcus_account_value": row["marcus_account_value"],
        "wells_fargo_value": row["wells_fargo_value"],
        "citibank_varsha_value": row["citibank_varsha_value"],
        "axisbank_value": row["axisbank_value"],
        "mortgage_balance": row["mortgage_balance"],
        "coinbase_value": row["coinbase_value"],
        "schwab_varsha_roth_value": row["schwab_varsha_roth_value"],
        "healthequity_fund_value": row["healthequity_fund_value"],
        "gap_etrade_value": row["gap_etrade_value"],
        "monthly_expenses": row["monthly_expenses"],
        "varsha_monthly_expenses": row["varsha_monthly_expenses"],
        "india_home_value": row["india_home_value"],
        "alo_ms_value": row["alo_ms_value"],
        "networth": row["networth"],
        "total_assets": row["total_assets"],
        "total_liabilities": row["total_liabilities"],
        "retirement_value": row["retirement_value"],
        "investment_amount": row["investment_amount"],
        "cash": row["cash"],
        "distribution": row["distribution"],
        "potential_annual_earning": row["potential_annual_earning"],
        "retirement_jay_amount": row["retirement_jay_amount"],
        "retirement_varsha_amount": row["retirement_varsha_amount"],
        "investment_jay_amount": row["investment_jay_amount"],
        "investment_varsha_amount": row["investment_varsha_amount"],
    }


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio_monthly_balance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_month TEXT NOT NULL,
                portfolio_date TEXT,
                description TEXT,
                robinhood_value REAL NOT NULL DEFAULT 0,
                schwab_jay_investment_value REAL NOT NULL DEFAULT 0,
                schwab_jay_ira_value REAL NOT NULL DEFAULT 0,
                alo_401k_value REAL NOT NULL DEFAULT 0,
                gap_401k_value REAL NOT NULL DEFAULT 0,
                chevron_401k_value REAL NOT NULL DEFAULT 0,
                schwab_varsha_investment_value REAL NOT NULL DEFAULT 0,
                schwab_jay_roth_value REAL NOT NULL DEFAULT 0,
                _529_kush_value REAL NOT NULL DEFAULT 0,
                _529_aadya_value REAL NOT NULL DEFAULT 0,
                marcus_account_value REAL NOT NULL DEFAULT 0,
                wells_fargo_value REAL NOT NULL DEFAULT 0,
                citibank_varsha_value REAL NOT NULL DEFAULT 0,
                axisbank_value REAL NOT NULL DEFAULT 0,
                mortgage_balance REAL NOT NULL DEFAULT 0,
                coinbase_value REAL NOT NULL DEFAULT 0,
                schwab_varsha_roth_value REAL NOT NULL DEFAULT 0,
                healthequity_fund_value REAL NOT NULL DEFAULT 0,
                gap_etrade_value REAL NOT NULL DEFAULT 0,
                monthly_expenses REAL NOT NULL DEFAULT 0,
                varsha_monthly_expenses REAL NOT NULL DEFAULT 0,
                india_home_value REAL NOT NULL DEFAULT 0,
                alo_ms_value REAL NOT NULL DEFAULT 0,
                networth REAL NOT NULL DEFAULT 0,
                total_assets REAL NOT NULL DEFAULT 0,
                total_liabilities REAL NOT NULL DEFAULT 0,
                retirement_value REAL NOT NULL DEFAULT 0,
                investment_amount REAL NOT NULL DEFAULT 0,
                cash REAL NOT NULL DEFAULT 0,
                distribution REAL NOT NULL DEFAULT 0,
                potential_annual_earning REAL NOT NULL DEFAULT 0,
                retirement_jay_amount REAL NOT NULL DEFAULT 0,
                retirement_varsha_amount REAL NOT NULL DEFAULT 0,
                investment_jay_amount REAL NOT NULL DEFAULT 0,
                investment_varsha_amount REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


def _value(item: PortfolioCreate | PortfolioItem | dict, field_name: str) -> float:
    if isinstance(item, dict):
        return float(item.get(field_name, 0.0) or 0.0)
    return float(getattr(item, field_name, 0.0) or 0.0)


def compute_jay_retirement(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return (
        _value(item, "schwab_jay_ira_value")
        + _value(item, "alo_401k_value")
        + _value(item, "gap_401k_value")
        + _value(item, "schwab_jay_roth_value")
    )


def compute_varsha_retirement(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return _value(item, "schwab_varsha_roth_value")


def compute_jay_investment(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return (
        _value(item, "schwab_jay_ira_value")
        + _value(item, "schwab_jay_investment_value")
        + _value(item, "gap_etrade_value")
    )


def compute_varsha_investment(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return (
        _value(item, "schwab_varsha_investment_value")
        + _value(item, "schwab_varsha_roth_value")
    )


def compute_retirement_total(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return compute_jay_retirement(item) + compute_varsha_retirement(item)


def compute_investment_total(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return compute_jay_investment(item) + compute_varsha_investment(item)


def compute_networth(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return _value(item, "total_assets") - _value(item, "total_liabilities")


def compute_total_assets(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return (
        _value(item, "robinhood_value")
        + _value(item, "schwab_jay_investment_value")
        + _value(item, "schwab_jay_ira_value")
        + _value(item, "alo_401k_value")
        + _value(item, "gap_401k_value")
        + _value(item, "chevron_401k_value")
        + _value(item, "schwab_varsha_investment_value")
        + _value(item, "schwab_jay_roth_value")
        + _value(item, "_529_kush_value")
        + _value(item, "_529_aadya_value")
        + _value(item, "marcus_account_value")
        + _value(item, "wells_fargo_value")
        + _value(item, "citibank_varsha_value")
        + _value(item, "axisbank_value")
        + _value(item, "coinbase_value")
        + _value(item, "schwab_varsha_roth_value")
        + _value(item, "healthequity_fund_value")
        + _value(item, "gap_etrade_value")
        + _value(item, "india_home_value")
        + _value(item, "alo_ms_value")
    )


def compute_total_liabilities(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return _value(item, "mortgage_balance") + _value(item, "monthly_expenses") + _value(item, "varsha_monthly_expenses")


def compute_cash(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return (
        _value(item, "wells_fargo_value")
        + _value(item, "citibank_varsha_value")
        + _value(item, "axisbank_value")
        + _value(item, "coinbase_value")
    )


def compute_distribution(item: PortfolioCreate | PortfolioItem | dict) -> float:
    return _value(item, "retirement_value") + _value(item, "investment_amount") + _value(item, "cash")


@app.post("/portfolio-monthly-balance", response_model=PortfolioItem)
def create_portfolio_item(item: PortfolioCreate):
    item.retirement_jay_amount = compute_jay_retirement(item)
    item.retirement_varsha_amount = compute_varsha_retirement(item)
    item.investment_jay_amount = compute_jay_investment(item)
    item.investment_varsha_amount = compute_varsha_investment(item)
    item.retirement_value = compute_retirement_total(item)
    item.investment_amount = compute_investment_total(item)
    item.total_assets = compute_total_assets(item)
    item.total_liabilities = compute_total_liabilities(item)
    item.cash = compute_cash(item)
    item.distribution = compute_distribution(item)
    item.networth = compute_networth(item)

    with get_db_connection() as conn:
        columns_sql = ", ".join(PORTFOLIO_MONTHLY_BALANCE_COLUMNS)
        placeholders_sql = ", ".join(["?"] * len(PORTFOLIO_MONTHLY_BALANCE_COLUMNS))
        cursor = conn.execute(
            f"""
            INSERT INTO portfolio_monthly_balance ({columns_sql})
            VALUES ({placeholders_sql})
            """,
            (
                item.portfolio_month,
                item.portfolio_date.isoformat() if item.portfolio_date else None,
                item.description,
                item.robinhood_value,
                item.schwab_jay_investment_value,
                item.schwab_jay_ira_value,
                item.alo_401k_value,
                item.gap_401k_value,
                item.chevron_401k_value,
                item.schwab_varsha_investment_value,
                item.schwab_jay_roth_value,
                item._529_kush_value,
                item._529_aadya_value,
                item.marcus_account_value,
                item.wells_fargo_value,
                item.citibank_varsha_value,
                item.axisbank_value,
                item.mortgage_balance,
                item.coinbase_value,
                item.schwab_varsha_roth_value,
                item.healthequity_fund_value,
                item.gap_etrade_value,
                item.monthly_expenses,
                item.varsha_monthly_expenses,
                item.india_home_value,
                item.alo_ms_value,
                item.networth,
                item.total_assets,
                item.total_liabilities,
                item.retirement_value,
                item.investment_amount,
                item.cash,
                item.distribution,
                item.potential_annual_earning,
                item.retirement_jay_amount,
                item.retirement_varsha_amount,
                item.investment_jay_amount,
                item.investment_varsha_amount,
            ),
        )
        conn.commit()

    return {
        "id": cursor.lastrowid,
        **item.model_dump(exclude={"id"}),
    }


@app.get("/portfolio-monthly-balance", response_model=list[PortfolioItem])
def list_portfolio():
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM portfolio_monthly_balance ORDER BY id"
        ).fetchall()
        return [portfolio_row_to_dict(row) for row in rows]


@app.get("/portfolio-monthly-balance/{portfolio_id}", response_model=PortfolioItem)
def read_portfolio_item(portfolio_id: int):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM portfolio_monthly_balance WHERE id = ?",
            (portfolio_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Portfolio monthly balance record not found")

    return portfolio_row_to_dict(row)


@app.put("/portfolio-monthly-balance/{portfolio_id}", response_model=PortfolioItem)
def update_portfolio_item(portfolio_id: int, item: PortfolioCreate):
    with get_db_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM portfolio_monthly_balance WHERE id = ?",
            (portfolio_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Portfolio monthly balance record not found")

        conn.execute(
            """
            UPDATE portfolio_monthly_balance
            SET portfolio_month = ?,
                portfolio_date = ?,
                description = ?,
                robinhood_value = ?,
                schwab_jay_investment_value = ?,
                schwab_jay_ira_value = ?,
                alo_401k_value = ?,
                gap_401k_value = ?,
                chevron_401k_value = ?,
                schwab_varsha_investment_value = ?,
                schwab_jay_roth_value = ?,
                _529_kush_value = ?,
                _529_aadya_value = ?,
                marcus_account_value = ?,
                wells_fargo_value = ?,
                citibank_varsha_value = ?,
                axisbank_value = ?,
                mortgage_balance = ?,
                coinbase_value = ?,
                schwab_varsha_roth_value = ?,
                healthequity_fund_value = ?,
                gap_etrade_value = ?,
                monthly_expenses = ?,
                varsha_monthly_expenses = ?,
                india_home_value = ?,
                alo_ms_value = ?,
                networth = ?,
                total_assets = ?,
                total_liabilities = ?,
                retirement_value = ?,
                investment_amount = ?,
                cash = ?,
                distribution = ?,
                potential_annual_earning = ?,
                retirement_jay_amount = ?,
                retirement_varsha_amount = ?,
                investment_jay_amount = ?,
                investment_varsha_amount = ?
            WHERE id = ?
            """,
            (
                item.portfolio_month,
                item.portfolio_date.isoformat() if item.portfolio_date else None,
                item.description,
                item.robinhood_value,
                item.schwab_jay_investment_value,
                item.schwab_jay_ira_value,
                item.alo_401k_value,
                item.gap_401k_value,
                item.chevron_401k_value,
                item.schwab_varsha_investment_value,
                item.schwab_jay_roth_value,
                item._529_kush_value,
                item._529_aadya_value,
                item.marcus_account_value,
                item.wells_fargo_value,
                item.citibank_varsha_value,
                item.axisbank_value,
                item.mortgage_balance,
                item.coinbase_value,
                item.schwab_varsha_roth_value,
                item.healthequity_fund_value,
                item.gap_etrade_value,
                item.monthly_expenses,
                item.varsha_monthly_expenses,
                item.india_home_value,
                item.alo_ms_value,
                item.networth,
                item.total_assets,
                item.total_liabilities,
                item.retirement_value,
                item.investment_amount,
                item.cash,
                item.distribution,
                item.potential_annual_earning,
                item.retirement_jay_amount,
                item.retirement_varsha_amount,
                item.investment_jay_amount,
                item.investment_varsha_amount,
                portfolio_id,
            ),
        )
        conn.commit()

    updated = {**item.model_dump(), "id": portfolio_id}
    return updated


@app.get("/portfolio-monthly-balance/{portfolio_id}/jay-retirement")
def get_jay_retirement(portfolio_id: int):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM portfolio_monthly_balance WHERE id = ?",
            (portfolio_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Portfolio monthly balance record not found")

    item = portfolio_row_to_dict(row)
    retirement_value = compute_jay_retirement(item)
    return {
        "portfolio_id": portfolio_id,
        "portfolio_month": row["portfolio_month"],
        "jay_retirement_value": retirement_value,
        "components": {
            "schwab_jay_ira_value": item["schwab_jay_ira_value"],
            "alo_401k_value": item["alo_401k_value"],
            "gap_401k_value": item["gap_401k_value"],
            "schwab_jay_roth_value": item["schwab_jay_roth_value"],
        },
    }


@app.get("/portfolio-monthly-balance/summary")
def get_monthly_balance_summary():
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM portfolio_monthly_balance ORDER BY portfolio_month DESC, id DESC"
        ).fetchall()

    if not rows:
        return {
            "latest_record": None,
            "total_records": 0,
            "latest_month": None,
            "summary": {
                "retirement_value": 0.0,
                "investment_amount": 0.0,
                "cash": 0.0,
                "total_assets": 0.0,
                "total_liabilities": 0.0,
                "networth": 0.0,
                "distribution": 0.0,
            },
        }

    latest = portfolio_row_to_dict(rows[0])
    summary = {
        "retirement_value": compute_retirement_total(latest),
        "investment_amount": compute_investment_total(latest),
        "cash": compute_cash(latest),
        "total_assets": compute_total_assets(latest),
        "total_liabilities": compute_total_liabilities(latest),
        "networth": compute_networth(latest),
        "distribution": compute_distribution(latest),
    }

    return {
        "latest_record": latest,
        "total_records": len(rows),
        "latest_month": latest["portfolio_month"],
        "summary": summary,
    }


@app.delete("/portfolio-monthly-balance/{portfolio_id}")
def delete_portfolio_item(portfolio_id: int):
    with get_db_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM portfolio_monthly_balance WHERE id = ?",
            (portfolio_id,),
        ).fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Portfolio monthly balance record not found")

        conn.execute(
            "DELETE FROM portfolio_monthly_balance WHERE id = ?",
            (portfolio_id,),
        )
        conn.commit()

    return {"message": "Portfolio monthly balance record deleted", "id": portfolio_id}


@app.get("/ui", response_class=HTMLResponse)
def portfolio_ui():
    html_file = Path(__file__).parent / "static" / "portfolio.html"
    return html_file.read_text()
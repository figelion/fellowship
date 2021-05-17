import pandas as pd
import numpy as np
from numpy import inf
from typing import Any

def nopat(ebit:float, podatek:float, efektywna_stawka_podatkowa:float = None) -> float:
    """
    Zysk operacyjny netto po opodatkowaniu (ang. Net Operating Profit After Tax)

    Parameters
    ----------
    ebit:float
        Zysk operacyjny, czyli zysk przed odliczeniem podatkow i odsetek (ang. earnings
        before deducting interest and taxes)
    podatek:float
        Równa się odroczony + bieżący
    efektywna_stawka_podatkowa:float


    Returns
    -------
    results: float
        nopat
    """
    if efektywna_stawka_podatkowa is None:
        return (ebit - podatek).values
    else:
        return (ebit * (1 - efektywna_stawka_podatkowa)).values


def efektywna_stawka_podatkowa():
    pass


def podatek(zysk_przed_opodatkowaniem: float, zysk_netto: float) -> float:
    """
    Różnica zysku przed opodatkowaniem i zysku netto.

    Parameters
    ----------
    zysk_przed_opodatkowaniem: float
    zysk_netto: float

    Returns
    -------
    results: float
        podatek
    """
    return zysk_przed_opodatkowaniem - zysk_netto


def kapital_staly(kapital_wlasny: float, zobowiązania_dlugoterminowe: float) -> float:
    """

    Parameters
    ----------
    kapital_wlasny:float
    zobowiązania_dlugoterminowe:float

    Returns
    -------
    results: float
    """
    return kapital_wlasny + zobowiązania_dlugoterminowe


# TODO 25.02.2021 figelion: Optimize computation
def convert_indicators_to_multiple_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dataframe from database to database with indicators as separated columns
    with deleting id column
    Parameters
    ----------
    df:pd.DataFrame
        DataFrame created from database

    Returns
    -------
    results: pd.DataFrame
        Dataframe with indicators as separated columns
    """

    lista_indicators = list(df.indicator.unique())
    list_period = list(df.period.unique())
    list_ticker = list(df.ticker.unique())


    data = []
    for single_period in list_period:
        for single_ticker in list_ticker:

            df_date = df[df['period'] == single_period]
            df_ticker_date = df_date[df_date["ticker"] == single_ticker]
            # print(df_ticker_date["id"].values)
            # row_id = df_ticker_date["id"].values
            data_row = [single_ticker, single_period]
            # print(df_ticker_date)
            if df_ticker_date["indicator"].empty:
                # print("empty")
                continue

            for single_indicator in lista_indicators:
                # try:
                row_indicator = df_ticker_date[df_ticker_date["indicator"] == single_indicator]
                if row_indicator.empty:
                    indicator_value = 0.0
                else:
                    indicator_value = row_indicator["value"].values[0]
                    # print(indicator_value)
                data_row.append(indicator_value)
            data.append(data_row)

    df_indicator_as_columns = pd.DataFrame(data, columns=['ticker', 'period'] + lista_indicators)
    return df_indicator_as_columns

def replace_inf(data: np.ndarray, replace_value: Any = None) -> np.ndarray:
    data[data == inf] = replace_value
    data[data == -inf] = replace_value
    return data
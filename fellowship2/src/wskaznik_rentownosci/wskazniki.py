from src.wskazniki_rentownosci import utils
import numpy as np
import utils

def compute_roic(nopat: float, kapital_staly: float) -> float:
    """
    Wskaźnik stopy zwrotu zainwestowanego kapitalu (ang. return on invested capital)

    Parameters
    ----------
    nopat:float
        Zysk operacyjny netto po opodatkowaniu (ang. Net Operating Profi After Tax)
    kapital_staly:float
        Równa się kapital wlasny + zobowiazania dlugoterminowe

    Returns
    -------
    result: float
        roic
    """

    if isinstance(nopat, np.ndarray) and isinstance(kapital_staly, np.ndarray):
        roic_value = nopat / kapital_staly
        roic_value = utils.replace_inf(roic_value, replace_value=None)
        return roic_value
    else:
        if kapital_staly is None or kapital_staly == 0 or nopat is None:
            return None
        else:
            return nopat / kapital_staly


def compute_roce(ebit: float, kapital_staly: float) -> float:
    """
    Wskaznik stopy zwrotu z zaangazowanego kapitalu (ang. return on capital employed)

    Parameters
    ----------
    ebit: float
        Zysk operacyjny, czyli zysk przed odliczeniem podatkow i odsetek (ang. earnings
        before deducting interest and taxes)
    kapital_staly: float
        Równa się kapital wlasny + zobowiazania dlugoterminowe

    Returns
    -------
    result: float
        roce
    """
    if isinstance(ebit, np.ndarray) and isinstance(kapital_staly, np.ndarray):
        roce_value = ebit / kapital_staly
        roce_value = utils.replace_inf(roce_value, replace_value=None)
        return roce_value

    if kapital_staly is None or kapital_staly == 0 or ebit is None:
        return None
    else:
        return ebit / kapital_staly


def compute_ros(zysk_netto: float, przychody_ze_sprzedazy: float) -> float:
    """
    Wskaznik rentownosci aktywow (ang. return on sales)

    Parameters
    ----------
    zysk_netto:float
    przychody_ze_sprzedazy:float


    Returns
    -------
    result: float
        ros
    """
    if isinstance(zysk_netto, np.ndarray) and isinstance(przychody_ze_sprzedazy, np.ndarray):
        ros_value = zysk_netto / przychody_ze_sprzedazy * 100
        ros_value = utils.replace_inf(ros_value, replace_value=None)
        return ros_value
    if przychody_ze_sprzedazy is None or przychody_ze_sprzedazy == 0 or zysk_netto is None:
        return None
    else:
        return zysk_netto / przychody_ze_sprzedazy * 100


def compute_roa(zysk_netto: float, aktywa: float) -> float:
    """
    Wskaznik rentownosci aktywow (ang. return on assets)

    Parameters
    ----------
    zysk_netto:float
    aktywa:float

    Returns
    -------
    results: float
        roa
    """
    if isinstance(zysk_netto, np.ndarray) and isinstance(aktywa, np.ndarray):
        roa_value = zysk_netto / aktywa
        roa_value = utils.replace_inf(roa_value, replace_value=None)
        return roa_value
    if aktywa is None or aktywa == 0 or zysk_netto is None:
        return None
    else:
        return zysk_netto / aktywa


def compute_roe(zysk_netto: float, kapital_wlasny: float) -> float:
    """
    Wskaznik rentownosci kapitalu wlasnego (ang. return on equity)

    Parameters
    ----------
    zysk_netto:float
    kapital_wlasny:float

    Returns
    -------
    results: float
        roe
    """
    if isinstance(zysk_netto, np.ndarray) and isinstance(kapital_wlasny, np.ndarray):
        roe_value = zysk_netto / kapital_wlasny
        roe_value = utils.replace_inf(roe_value, replace_value=None)
        return roe_value
    if kapital_wlasny is None or kapital_wlasny == 0 or zysk_netto is None:
        return None
    else:
        return zysk_netto / kapital_wlasny

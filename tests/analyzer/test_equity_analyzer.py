import pytest
import numpy as np
import numpy.testing as npt


from portana.analyzer.equity_analyzer import EquityAnalyzer
from portana.timeseries.simtimeseries import SimTimeSeries
from portana.data.simulated import Equity


@pytest.fixture
def security_1_fixture():
    dates = np.array("2020-01-01", dtype=np.datetime64)
    dates = dates + np.arange(6)

    isin = "1"
    prices = np.array([200, 202, 204, 206, 208, 215], dtype=np.float64)
    tot_ret_idx = np.array([200, 202, 204, 206, 208, 215], dtype=np.float64)
    timeseries = SimTimeSeries(dates, prices, tot_ret_idx)

    return Equity(isin, timeseries, {}, {})


@pytest.fixture
def security_2_fixture():
    dates = np.array("2020-01-01", dtype=np.datetime64)
    dates = dates + np.arange(6)

    isin = "2"
    prices = np.array([100, 98, 97, 99, 100, 101], dtype=np.float64)
    tot_ret_idx = np.array([100, 98, 97, 99, 100, 101], dtype=np.float64)
    timeseries = SimTimeSeries(dates, prices, tot_ret_idx)

    return Equity(isin, timeseries, {}, {})


@pytest.fixture
def index_fixture():
    dates = np.array("2020-01-01", dtype=np.datetime64)
    dates = dates + np.arange(6)

    isin = "0"
    prices = np.array([100, 101, 102, 103, 102, 105], dtype=np.float64)
    tot_ret_idx = np.array([100, 101, 102, 103, 102, 105], dtype=np.float64)
    timeseries = SimTimeSeries(dates, prices, tot_ret_idx)

    return Equity(isin, timeseries, {}, {})


def test_add_security(security_1_fixture, security_2_fixture, index_fixture):
    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    assert analyzer.securities == [security_1_fixture, security_2_fixture]


def test_set_comp_index(security_1_fixture, security_2_fixture, index_fixture):
    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    assert analyzer.comp_index == index_fixture


def test_earliest_common_date(security_1_fixture, security_2_fixture, index_fixture):
    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    assert analyzer._earliest_common_date == np.datetime64("2020-01-01")


def test_latest_common_date(security_1_fixture, security_2_fixture, index_fixture):
    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    assert analyzer._latest_common_date == np.datetime64("2020-01-06")


def test_date_series(security_1_fixture, security_2_fixture, index_fixture):
    dates = np.array("2020-01-01", dtype=np.datetime64)
    dates = dates + np.arange(6)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer._date_series, dates)


def test_price_series(security_1_fixture, security_2_fixture, index_fixture):
    price_series = np.array(
        [[200, 100], [202, 98], [204, 97], [206, 99], [208, 100], [215, 101]],
        dtype=np.float64,
    )
    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer._price_series.results, price_series)


def test_tot_ret_series(security_1_fixture, security_2_fixture, index_fixture):
    tot_ret_series = np.array(
        [[200, 100], [202, 98], [204, 97], [206, 99], [208, 100], [215, 101]],
        dtype=np.float64,
    )
    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer._tot_ret_idx_series.results, tot_ret_series)


def test_col_names(security_1_fixture, security_2_fixture, index_fixture):
    col_names = ["1", "2"]

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    assert analyzer._col_names == col_names


# Test Rebased Index
def test_rebased_index_securities_px(
    security_1_fixture, security_2_fixture, index_fixture
):
    rebased_index_securities = np.array(
        [
            [1000, 1000],
            [1010, 980],
            [1020, 970],
            [1030, 990],
            [1040, 1000],
            [1075, 1010],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_rebased_index("px", 1000)[0].results,
        rebased_index_securities,
        1e-8,
        0,
    )


def test_rebased_index_securities_tr(
    security_1_fixture, security_2_fixture, index_fixture
):
    rebased_index_securities = np.array(
        [
            [1000, 1000],
            [1010, 980],
            [1020, 970],
            [1030, 990],
            [1040, 1000],
            [1075, 1010],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_rebased_index("tr", 1000)[0].results,
        rebased_index_securities,
        1e-8,
        0,
    )


def test_rebased_index_index_px(security_1_fixture, security_2_fixture, index_fixture):
    rebased_index_index = np.array(
        [
            1000,
            1010,
            1020,
            1030,
            1020,
            1050,
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_rebased_index("px", 1000)[1].results,
        rebased_index_index,
        1e-8,
        0,
    )


def test_rebased_index_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    rebased_index_index = np.array(
        [
            1000,
            1010,
            1020,
            1030,
            1020,
            1050,
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_rebased_index("tr", 1000)[1].results,
        rebased_index_index,
        1e-8,
        0,
    )


def test_rebased_index_dates_desired(
    security_1_fixture, security_2_fixture, index_fixture
):
    dates = np.array("2020-01-01", dtype=np.datetime64)
    dates = dates + np.arange(6)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_rebased_index("px", 1000)[0].dates, dates)
    npt.assert_equal(analyzer.get_rebased_index("tr", 1000)[0].dates, dates)
    npt.assert_equal(analyzer.get_rebased_index("px", 1000)[1].dates, dates)
    npt.assert_equal(analyzer.get_rebased_index("tr", 1000)[1].dates, dates)


# Test Returns
def test_returns_securities_px(security_1_fixture, security_2_fixture, index_fixture):
    returns_securities = np.array(
        [
            [0.01000, -0.02000],
            [0.00990, -0.01020],
            [0.00980, 0.02062],
            [0.00971, 0.01010],
            [0.03365, 0.01000],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_returns("px")[0].results,
        returns_securities,
        1e-3,
        0,
    )


def test_returns_securities_tr(security_1_fixture, security_2_fixture, index_fixture):
    returns_securities = np.array(
        [
            [0.01000, -0.02000],
            [0.00990, -0.01020],
            [0.00980, 0.02062],
            [0.00971, 0.01010],
            [0.03365, 0.01000],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_returns("tr")[0].results,
        returns_securities,
        1e-3,
        0,
    )


def test_returns_index_px(security_1_fixture, security_2_fixture, index_fixture):
    returns_index = np.array(
        [
            0.01000,
            0.00990,
            0.00980,
            -0.00971,
            0.02941,
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_returns("px")[1].results,
        returns_index,
        1e-3,
        0,
    )


def test_returns_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    returns_index = np.array(
        [
            0.01000,
            0.00990,
            0.00980,
            -0.00971,
            0.02941,
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_returns("tr")[1].results,
        returns_index,
        1e-3,
        0,
    )


def test_returns_dates_desired(security_1_fixture, security_2_fixture, index_fixture):
    dates = np.array("2020-01-02", dtype=np.datetime64)
    dates = dates + np.arange(5)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_returns("px")[0].dates, dates)
    npt.assert_equal(analyzer.get_returns("tr")[0].dates, dates)
    npt.assert_equal(analyzer.get_returns("px")[1].dates, dates)
    npt.assert_equal(analyzer.get_returns("tr")[1].dates, dates)


# Test Betas
def test_betas_securities_px(security_1_fixture, security_2_fixture, index_fixture):
    betas_securities = np.array(
        [
            [0.611167, -0.008818],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_betas("px")[0].results,
        betas_securities,
        1e-3,
        0,
    )


def test_betas_securities_tr(security_1_fixture, security_2_fixture, index_fixture):
    betas_securities = np.array(
        [
            [0.611167, -0.008818],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_betas("tr")[0].results,
        betas_securities,
        1e-3,
        0,
    )


def test_betas_index_px(security_1_fixture, security_2_fixture, index_fixture):
    betas_index = np.array(
        [1.0],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_betas("px")[1].results,
        betas_index,
        1e-3,
        0,
    )


def test_betas_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    betas_index = np.array(
        [
            1.0,
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_betas("tr")[1].results,
        betas_index,
        1e-3,
        0,
    )


def test_betas_dates_desired(security_1_fixture, security_2_fixture, index_fixture):
    dates = np.array(["2020-01-06"], dtype=np.datetime64)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_betas("px")[0].dates, dates)
    npt.assert_equal(analyzer.get_betas("tr")[0].dates, dates)
    npt.assert_equal(analyzer.get_betas("px")[1].dates, dates)
    npt.assert_equal(analyzer.get_betas("tr")[1].dates, dates)


# Test Volatilities
def test_vol_securities_px(security_1_fixture, security_2_fixture, index_fixture):
    vol_securities = np.array(
        [
            [0.168975, 0.264343],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_volatilities("px", 252)[0].results,
        vol_securities,
        1e-3,
        0,
    )


def test_vol_securities_tr(security_1_fixture, security_2_fixture, index_fixture):
    vol_securities = np.array(
        [
            [0.168975, 0.264343],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_volatilities("tr", 252)[0].results,
        vol_securities,
        1e-3,
        0,
    )


def test_vol_index_px(security_1_fixture, security_2_fixture, index_fixture):
    vol_index = np.array(
        [0.219566],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_volatilities("px", 252)[1].results,
        vol_index,
        1e-3,
        0,
    )


def test_vol_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    vol_index = np.array(
        [0.219566],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_volatilities("tr", 252)[1].results,
        vol_index,
        1e-3,
        0,
    )


def test_vol_dates_desired(security_1_fixture, security_2_fixture, index_fixture):
    dates = np.array(["2020-01-06"], dtype=np.datetime64)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_volatilities("px", 252)[0].dates, dates)
    npt.assert_equal(analyzer.get_volatilities("tr", 252)[0].dates, dates)
    npt.assert_equal(analyzer.get_volatilities("px", 252)[1].dates, dates)
    npt.assert_equal(analyzer.get_volatilities("tr", 252)[1].dates, dates)


# Test Sharpes
def test_sharpes_securities_px(security_1_fixture, security_2_fixture, index_fixture):
    sharpes_securities = np.array(
        [
            [0.325491735, -0.037829617],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_sharpes("px", 252, 0.02)[0].results,
        sharpes_securities,
        1e-3,
        0,
    )


def test_sharpes_securities_tr(security_1_fixture, security_2_fixture, index_fixture):
    sharpes_securities = np.array(
        [
            [0.325491735, -0.037829617],
        ],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_sharpes("tr", 252, 0.02)[0].results,
        sharpes_securities,
        1e-3,
        0,
    )


def test_sharpes_index_px(security_1_fixture, security_2_fixture, index_fixture):
    sharpes_index = np.array(
        [0.136632886],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_sharpes("px", 252, 0.02)[1].results,
        sharpes_index,
        1e-3,
        0,
    )


def test_sharpes_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    sharpes_index = np.array(
        [0.136632886],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_sharpes("tr", 252, 0.02)[1].results,
        sharpes_index,
        1e-3,
        0,
    )


def test_sharpes_dates_desired(security_1_fixture, security_2_fixture, index_fixture):
    dates = np.array(["2020-01-06"], dtype=np.datetime64)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_sharpes("px", 252, 0.02)[0].dates, dates)
    npt.assert_equal(analyzer.get_sharpes("tr", 252, 0.02)[0].dates, dates)
    npt.assert_equal(analyzer.get_sharpes("px", 252, 0.02)[1].dates, dates)
    npt.assert_equal(analyzer.get_sharpes("tr", 252, 0.02)[1].dates, dates)


# Test Drawdowns
def test_drawdowns_securities_px(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array(
        [[0.0, 0.0], [0, -0.02], [0, -0.03], [0, -0.01], [0, 0], [0, 0]],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_drawdowns("px")[0].results,
        desired,
        1e-3,
        0,
    )


def test_drawdowns_securities_tr(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array(
        [[0.0, 0.0], [0, -0.02], [0, -0.03], [0, -0.01], [0, 0], [0, 0]],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_drawdowns("tr")[0].results,
        desired,
        1e-3,
        0,
    )


def test_drawdowns_index_px(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array(
        [0, 0, 0, 0, -0.009708738, 0],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_drawdowns("px")[1].results,
        desired,
        1e-3,
        0,
    )


def test_drawdowns_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array(
        [0, 0, 0, 0, -0.009708738, 0],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_drawdowns("tr")[1].results,
        desired,
        1e-3,
        0,
    )


def test_drawdowns_dates_desired(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array("2020-01-01", dtype=np.datetime64)
    desired = desired + np.arange(6)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_drawdowns("px")[0].dates, desired)
    npt.assert_equal(analyzer.get_drawdowns("tr")[0].dates, desired)
    npt.assert_equal(analyzer.get_drawdowns("px")[1].dates, desired)
    npt.assert_equal(analyzer.get_drawdowns("tr")[1].dates, desired)


# Test Max Drawdowns
def test_max_drawdowns_securities_px(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(
        [[0.0, -0.03]],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_max_drawdowns("px")[0].results,
        desired,
        1e-3,
        0,
    )


def test_max_drawdowns_securities_tr(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(
        [[0.0, -0.03]],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_max_drawdowns("tr")[0].results,
        desired,
        1e-3,
        0,
    )


def test_max_drawdowns_index_px(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array(
        [-0.009708738],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_max_drawdowns("px")[1].results,
        desired,
        1e-3,
        0,
    )


def test_max_drawdowns_index_tr(security_1_fixture, security_2_fixture, index_fixture):
    desired = np.array(
        [-0.009708738],
        dtype=np.float64,
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_allclose(
        analyzer.get_max_drawdowns("tr")[1].results,
        desired,
        1e-3,
        0,
    )


def test_max_drawdowns_dates_desired(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(["2020-01-06"], dtype=np.datetime64)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_max_drawdowns("px")[0].dates, desired)
    npt.assert_equal(analyzer.get_max_drawdowns("tr")[0].dates, desired)
    npt.assert_equal(analyzer.get_max_drawdowns("px")[1].dates, desired)
    npt.assert_equal(analyzer.get_max_drawdowns("tr")[1].dates, desired)


# Test Max Drawdowns Dates
def test_max_drawdowns_dates_securities_px(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(
        [[np.datetime64("2020-01-01"), np.datetime64("2020-01-03")]],
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(
        analyzer.get_max_drawdowns_dates("px")[0].results,
        desired,
    )


def test_max_drawdowns_dates_securities_tr(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(
        [[np.datetime64("2020-01-01"), np.datetime64("2020-01-03")]],
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(
        analyzer.get_max_drawdowns_dates("tr")[0].results,
        desired,
    )


def test_max_drawdowns_dates_index_px(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(
        [np.datetime64("2020-01-05")],
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(
        analyzer.get_max_drawdowns_dates("px")[1].results,
        desired,
    )


def test_max_drawdowns_dates_index_tr(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(
        [np.datetime64("2020-01-05")],
    )

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(
        analyzer.get_max_drawdowns_dates("tr")[1].results,
        desired,
    )


def test_max_drawdowns_dates_dates_desired(
    security_1_fixture, security_2_fixture, index_fixture
):
    desired = np.array(["2020-01-06"], dtype=np.datetime64)

    analyzer = EquityAnalyzer()
    analyzer.add_security(security_1_fixture)
    analyzer.add_security(security_2_fixture)
    analyzer.set_comp_index(index_fixture)

    npt.assert_equal(analyzer.get_max_drawdowns_dates("px")[0].dates, desired)
    npt.assert_equal(analyzer.get_max_drawdowns_dates("tr")[0].dates, desired)
    npt.assert_equal(analyzer.get_max_drawdowns_dates("px")[1].dates, desired)
    npt.assert_equal(analyzer.get_max_drawdowns_dates("tr")[1].dates, desired)

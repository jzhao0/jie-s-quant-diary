"""
finance_utils.py 的单元测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import numpy as np
import pandas as pd
from finance_utils import (
    calculate_returns,
    calculate_volatility,
    calculate_sharpe_ratio,
    calculate_max_drawdown
)


def test_calculate_returns():
    """测试收益率计算"""
    prices = pd.Series([100, 110, 105, 115])
    returns = calculate_returns(prices)
    assert len(returns) == 3
    assert np.isclose(returns.iloc[0], 0.10)
    print("✅ calculate_returns 测试通过")


def test_calculate_volatility():
    """测试波动率计算"""
    returns = pd.Series([0.01, -0.02, 0.015, -0.01, 0.005])
    vol = calculate_volatility(returns, periods=252)
    assert vol > 0
    print("✅ calculate_volatility 测试通过")


if __name__ == "__main__":
    test_calculate_returns()
    test_calculate_volatility()
    print("\n🎉 所有测试通过!")

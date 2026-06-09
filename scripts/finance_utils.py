"""
金融量化工具函数库

包含常用的金融计算函数:
- 收益率计算
- 波动率计算
- 夏普比率
- 最大回撤
"""

import numpy as np
import pandas as pd


def calculate_returns(prices: pd.Series) -> pd.Series:
    """计算简单收益率"""
    return prices.pct_change().dropna()


def calculate_volatility(returns: pd.Series, periods: int = 252) -> float:
    """
    计算年化波动率
    
    Args:
        returns: 收益率序列
        periods: 年化周期 (默认252个交易日)
    
    Returns:
        年化波动率
    """
    return returns.std() * np.sqrt(periods)


def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.03) -> float:
    """
    计算夏普比率
    
    Args:
        returns: 收益率序列
        risk_free_rate: 无风险利率 (默认3%)
    
    Returns:
        夏普比率
    """
    excess_returns = returns.mean() * 252 - risk_free_rate
    volatility = calculate_volatility(returns)
    return excess_returns / volatility if volatility != 0 else 0


def calculate_max_drawdown(prices: pd.Series) -> tuple:
    """
    计算最大回撤
    
    Args:
        prices: 价格序列
    
    Returns:
        (最大回撤比例, 回撤开始日期, 回撤结束日期)
    """
    cummax = prices.cummax()
    drawdown = (prices - cummax) / cummax
    
    max_dd = drawdown.min()
    end_date = drawdown.idxmin()
    start_date = prices[:end_date].idxmax()
    
    return max_dd, start_date, end_date


def calculate_moving_average(prices: pd.Series, window: int) -> pd.Series:
    """计算移动平均线"""
    return prices.rolling(window=window).mean()


if __name__ == "__main__":
    # 测试代码
    print("✅ finance_utils.py 加载成功")
    print("可用函数:")
    print("  - calculate_returns()")
    print("  - calculate_volatility()")
    print("  - calculate_sharpe_ratio()")
    print("  - calculate_max_drawdown()")
    print("  - calculate_moving_average()")

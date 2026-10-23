import pandas as pd
import akshare as ak

print("正在获取贵州茅台数据...")
df = ak.stock_zh_a_hist(
    symbol="600519",
    period="daily",
    start_date="20240101",
    end_date="20240614",
    adjust="qfq"
)

print("\n数据预览：")
print(df.head())

print(f"\n数据形状: {df.shape}")

from pathlib import Path

output_path = Path(__file__).resolve().parents[1] / "data" / "maotai_2024.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"\n数据已保存到: {output_path}")

# HousePriceAnalysis 项目说明

本项目为成都二手房数据分析与可视化系统，包含数据采集、清洗、分析、机器学习建模和Web可视化全流程。

## 目录结构

- `scraper.py`         —— 爬取链家成都各区二手房数据，生成原始数据csv
- `data_cleaner.py`    —— 对原始数据进行清洗、异常值处理、标准化，生成可视化和建模数据集
- `analysis.py`        —— 生成各类可视化图表（地图、柱状图、饼图、散点图、箱线图、词云等）
- `machine_learning.py`—— K-Means聚类分析与房价预测回归建模
- `verify_districts.py`—— 检查区县名称标准化情况
- `app.py`             —— Flask Web应用入口，集成所有可视化和机器学习结果
- `chengdu_raw_data.csv`      —— 原始爬取数据
- `chengdu_cleaned_data.csv`  —— 清洗后用于可视化的数据
- `chengdu_ml_data.csv`       —— 用于机器学习的数据

## 主要功能流程

1. **数据采集**：运行`scraper.py`，抓取链家成都各区二手房信息，生成`chengdu_raw_data.csv`
2. **数据清洗**：运行`data_cleaner.py`，处理缺失、异常、标准化，生成`chengdu_cleaned_data.csv`和`chengdu_ml_data.csv`
3. **可视化分析**：运行`analysis.py`，可在Jupyter或Web端生成各类图表
4. **机器学习建模**：运行`machine_learning.py`，完成K-Means聚类和房价回归预测
5. **Web展示**：运行`app.py`，在浏览器访问 http://127.0.0.1:5000 查看所有分析和建模结果

## 依赖环境

- Python 3.7+
- pandas
- numpy
- flask
- pyecharts
- scikit-learn
- beautifulsoup4
- requests

## 快速开始

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 按顺序运行：
   - `python scraper.py`
   - `python data_cleaner.py`
   - `python app.py`
3. 浏览器访问 http://127.0.0.1:5000 查看结果

## 说明
- 若数据量较大，建议适当调整`scraper.py`中的`MAX_PAGES_PER_DISTRICT`参数。
- 若区县名称不标准，可用`verify_districts.py`检查并重新清洗。
- 所有可视化和机器学习结果均可在Web端一站式查看。

---
如有问题欢迎反馈！
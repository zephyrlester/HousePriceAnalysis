# 2_data_cleaner.py (完整最终版)
# ------------------------------------------
# 本脚本用于对原始爬取的成都二手房数据进行清洗、转换和标准化。
# 主要功能：
# 1. 数据类型转换与单位去除
# 2. 缺失值与异常值处理
# 3. 生成可视化和机器学习两份数据集
# 依赖库：pandas, numpy
# ------------------------------------------

import pandas as pd
import numpy as np

def clean_data(input_path='chengdu_raw_data.csv', viz_output='chengdu_cleaned_data.csv', ml_output='chengdu_ml_data.csv'):
    """
    读取原始数据，进行完整的清洗、转换和标准化流程。
    最终生成两个文件：
    1. chengdu_cleaned_data.csv: 用于数据可视化。
    2. chengdu_ml_data.csv: 用于机器学习，包含独热编码。
    """
    try:
        df = pd.read_csv(input_path)
        print("原始数据加载成功，开始清洗...")
        print(f"原始数据形状: {df.shape}")
    except FileNotFoundError:
        print(f"错误: 未找到原始数据文件 '{input_path}'。请先运行 1_scraper.py。")
        return

    # --- Part 1: 数据类型转换和单位去除 ---
    print("正在进行数据类型转换和单位去除...")
    df['TotalPrice'] = df['TotalPrice'].str.replace('万', '').astype(float)
    df['UnitPrice'] = df['UnitPrice'].str.extract('(\d+)').astype(float)
    df['Area'] = df['Area'].str.replace('平米', '').astype(float)
    df['Followers'] = df['Followers'].str.replace('人关注', '').astype(int)
    
    # --- Part 2: 处理建成年代 ---
    print("正在处理'建成年代'列...")
    df['YearBuilt'] = df['YearBuilt'].str.extract('(\d{4})').astype(float)
    year_median = df['YearBuilt'].median()
    df['YearBuilt'].fillna(year_median, inplace=True)
    df['YearBuilt'] = df['YearBuilt'].astype(int)

    # --- Part 3: 处理异常值 (基于面积的IQR方法) ---
    print("正在处理异常值...")
    Q1_area = df['Area'].quantile(0.25)
    Q3_area = df['Area'].quantile(0.75)
    IQR_area = Q3_area - Q1_area
    lower_bound = Q1_area - 1.5 * IQR_area
    upper_bound = Q3_area + 1.5 * IQR_area
    df = df[(df['Area'] >= lower_bound) & (df['Area'] <= upper_bound)]

    # --- Part 4: 地名标准化 (终极版) ---
    print("正在进行地名精确标准化...")
    DISTRICT_MAP = {
        # 标准名称
        '武侯': '武侯区', '锦江': '锦江区', '青羊': '青羊区', '金牛': '金牛区',
        '成华': '成华区', '龙泉驿': '龙泉驿区', '双流': '双流区', '温江': '温江区',
        '郫都': '郫都区', '新都': '新都区', '青白江': '青白江区', '都江堰': '都江堰市',
        '彭州': '彭州市', '邛崃': '邛崃市', '崇州': '崇州市', '简阳': '简阳市',
        '金堂': '金堂县', '大邑': '大邑县', '蒲江': '蒲江县', '新津': '新津区',
        
        # 网站上常见的高新区变体
        '高新': '高新区',
        '高新南区': '高新区',
        '高新西区': '高新区',
        '高新东区': '高新区', # 以防万一
        
        # 网站上常见的天府新区变体
        '天府新区': '四川天府新区',
        '天府新区南区': '四川天府新区',
        
        # 其他可能的简称或别名
        '龙泉': '龙泉驿区'
    }

    def standardize_district(name):
        """使用非常全面的映射字典进行地名标准化"""
        if name in DISTRICT_MAP:
            return DISTRICT_MAP[name]
        if not any(suffix in name for suffix in ['区', '市', '县']):
            return name + '区'
        return name

    df['District'] = df['District'].apply(standardize_district)
    print("地名精确标准化完成。")

    # --- Part 5: 特征工程 ---
    print("正在进行特征工程...")
    # 清理户型，提取“室”的数量
    df['RoomCount'] = df['Layout'].str.extract('(\d)室').astype(int)

    # 保存用于可视化的数据
    df_viz = df.copy()
    df_viz.to_csv(viz_output, index=False, encoding='utf-8-sig')
    print(f"\n可视化数据已保存至: {viz_output}")
    print(f"可视化数据形状: {df_viz.shape}")

    # --- Part 6: 准备用于机器学习的数据 ---
    print("\n正在准备机器学习数据...")
    df_ml = df.copy()

    # 选择用于独热编码的类别特征
    features_to_encode = ['District', 'SubDistrict','Orientation', 'Decoration', 'Elevator']
    
    # 执行独热编码，drop_first=True 可以减少共线性
    df_ml = pd.get_dummies(df_ml, columns=features_to_encode, drop_first=True)
    
    # 移除不再需要的原始文本列和对预测无用的列
    df_ml = df_ml.drop(['Title', 'Community', 'Layout', 'BuildingType', 'Floor'], axis=1)

    # 再次检查并确保所有列都是数值类型
    for col in df_ml.select_dtypes(include=['object']).columns:
        print(f"警告：机器学习数据中仍存在非数值列 '{col}'，将尝试移除。")
        df_ml = df_ml.drop(col, axis=1)

    # 保存用于机器学习的数据
    df_ml.to_csv(ml_output, index=False, encoding='utf-8-sig')
    print(f"机器学习数据已保存至: {ml_output}")
    print(f"机器学习数据形状: {df_ml.shape}")
    
    print("\n数据清洗与准备全部完成！")

if __name__ == '__main__':
    clean_data()
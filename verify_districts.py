# verify_districts.py
# ------------------------------------------
# 本脚本用于检查清洗后数据中的行政区名称标准化情况。
# 主要功能：
# 1. 读取清洗后数据，打印所有唯一行政区名称
# 2. 提示用户是否存在未标准化的区名
# 依赖库：pandas
# ------------------------------------------

import pandas as pd

def check_district_names(filepath='chengdu_cleaned_data.csv'):
    """
    读取清洗后的数据文件，并打印出所有唯一的区县名称。
    """
    try:
        df = pd.read_csv(filepath)
        unique_districts = df['District'].unique()
        
        print("-" * 50)
        print(f"在文件 '{filepath}' 中找到的唯一区县名称如下：")
        print("-" * 50)
        
        for district in sorted(unique_districts):
            print(district)
            
        print("-" * 50)
        print("请检查以上列表，是否存在未被标准化的名称（如 '武侯', '高新' 等）。")
        print("如果存在，说明您需要重新运行 2_data_cleaner.py 脚本。")
        
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{filepath}'。请先运行 2_data_cleaner.py。")
    except KeyError:
        print(f"错误: 文件 '{filepath}' 中找不到 'District' 列。")

if __name__ == '__main__':
    check_district_names()
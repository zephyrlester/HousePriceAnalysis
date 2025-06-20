# 3b_machine_learning.py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import numpy as np

def run_kmeans_clustering(data_path='chengdu_cleaned_data.csv', n_clusters=4):
    """执行K-Means聚类分析"""
    df = pd.read_csv(data_path)
    
    # 选择聚类特征
    features = ['Area', 'TotalPrice', 'UnitPrice']
    X = df[features]
    
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 训练K-Means模型
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)
    
    # 分析聚类结果
    cluster_summary = df.groupby('Cluster')[features].mean().round(2)
    
    print("\nK-Means 聚类结果分析:")
    print(cluster_summary)
    
    return df, cluster_summary

def run_price_prediction_model(data_path='chengdu_ml_data.csv'):
    """执行房价预测回归模型训练与评估"""
    df = pd.read_csv(data_path)
    
    # 定义特征和目标
    X = df.drop('TotalPrice', axis=1)
    y = df['TotalPrice']
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 选择并训练模型（随机森林回归）
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    print("\n正在训练随机森林回归模型...")
    model.fit(X_train, y_train)
    
    # 在测试集上进行预测
    y_pred = model.predict(X_test)
    
    # 评估模型
    evaluation_results = {
        'R-squared': metrics.r2_score(y_test, y_pred),
        'Mean Absolute Error (MAE)': metrics.mean_absolute_error(y_test, y_pred),
        'Mean Squared Error (MSE)': metrics.mean_squared_error(y_test, y_pred),
        'Root Mean Squared Error (RMSE)': np.sqrt(metrics.mean_squared_error(y_test, y_pred))
    }
    
    print("\n回归模型评估结果:")
    for metric, value in evaluation_results.items():
        print(f"{metric}: {value:.4f}")
        
    # 获取特征重要性
    feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False).head(10)
    print("\n特征重要性 Top 10:")
    print(feature_importances)
    
    return evaluation_results, feature_importances
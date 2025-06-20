# 4_app.py
from flask import Flask, render_template
from pyecharts.charts import Page

# 导入所有需要的函数
from analysis import (
    load_data, create_price_map, create_district_bar, create_layout_pie,
    create_area_price_scatter, create_decoration_boxplot, create_community_wordcloud,
    create_kmeans_scatter  # 新增
)
from machine_learning import (
    run_kmeans_clustering, run_price_prediction_model # 新增
)

app = Flask(__name__)

# --- 一次性加载数据和运行模型 ---
print("Web应用启动，正在加载数据和运行模型...")
# 加载可视化数据
df_viz = load_data('chengdu_cleaned_data.csv')

# 执行K-Means聚类
df_clustered, cluster_summary = run_kmeans_clustering()

# 执行回归模型
model_eval, feature_imp = run_price_prediction_model()
print("数据和模型准备就绪！")
# --- 结束 ---

@app.route('/')
def index():
    if df_viz is None:
        return "数据文件未找到，请先运行抓取和清洗脚本。"

    # 1. 创建可视化图表
    page = Page(layout=Page.SimplePageLayout)
    page.add(
        create_price_map(df_viz),
        create_district_bar(df_viz),
        create_kmeans_scatter(df_clustered),  # 使用新的聚类散点图
        create_layout_pie(df_viz),
        create_community_wordcloud(df_viz),
    )
    
    # 2. 将所有结果传递给模板
    return render_template(
        'index.html',
        chart_component=page.render_embed(),
        # 传递机器学习结果
        cluster_summary_html=cluster_summary.to_html(classes='table table-striped text-center'),
        model_eval=model_eval,
        feature_imp_html=feature_imp.to_frame(name='Importance').to_html(classes='table table-striped text-center')
    )

if __name__ == '__main__':
    print("请在浏览器中打开 http://127.0.0.1:5000")
    app.run(debug=False) # 建议使用非debug模式，避免模型重复运行
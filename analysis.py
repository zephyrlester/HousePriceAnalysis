# 3_analysis.py
import pandas as pd

from pyecharts import options as opts

from pyecharts.charts import Map, Bar,Pie, Scatter, Boxplot, WordCloud,Line

def load_data(filepath='chengdu_cleaned_data.csv'):
    """加载清洗后的数据"""
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"错误: 未找到清洗后的数据文件 '{filepath}'。请先运行 2_data_cleaner.py。")
        return None

def create_price_map(df):
    """生成成都各区平均单价地图"""
    district_price = df.groupby('District')['UnitPrice'].mean().round(0).sort_values(ascending=False)
    
    c = (
        Map()
        .add("平均单价(元/平米)", [list(z) for z in zip(district_price.index, district_price.values)], "成都")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="成都各区二手房平均单价"),
            visualmap_opts=opts.VisualMapOpts(max_=district_price.max(), is_piecewise=True),
        )
    )
    return c

def create_district_bar(df):
    """生成各区房源数量(柱状图)与平均总价(折线图)的混合图 (修正版)"""
    district_count = df['District'].value_counts()
    # 确保价格数据与数量数据的顺序一致
    district_total_price = df.groupby('District')['TotalPrice'].mean().round(2).loc[district_count.index]

    bar = (
        Bar()
        .add_xaxis(district_count.index.tolist())
        .add_yaxis(
            "房源数量",
            district_count.values.tolist(),
            yaxis_index=0, # 使用主Y轴
            label_opts=opts.LabelOpts(is_show=False),
        )
        .extend_axis( # 新增一个Y轴（次Y轴）
            yaxis=opts.AxisOpts(
                name="平均总价",
                type_="value",
                min_=0,
                axislabel_opts=opts.LabelOpts(formatter="{value} 万元"),
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各区房源数量与平均总价"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            yaxis_opts=opts.AxisOpts(
                name="房源数量",
                type_="value",
                min_=0,
                axislabel_opts=opts.LabelOpts(formatter="{value} 套"),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            legend_opts=opts.LegendOpts(pos_left="center")
        )
    )

    # 创建一个折线图，用于展示平均总价
    line = (
        Line()
        .add_xaxis(district_total_price.index.tolist())
        .add_yaxis(
            "平均总价(万元)",
            district_total_price.values.tolist(),
            yaxis_index=1, # 指定使用次Y轴
        )
    )

    # 将折线图叠加到柱状图上
    bar.overlap(line)
    return bar

def create_layout_pie(df):
    """生成户型分布饼图 (简化版)"""
    layout_count = df['Layout'].value_counts().head(10)
    
    # 显式地将数据转换为 (key, value) 元组的列表
    data_pair = [
        (name, int(count)) for name, count in zip(layout_count.index, layout_count.values)
    ]
    
    c = (
        Pie()
        .add(
            series_name="户型分布",
            data_pair=data_pair,
            rosetype="area",
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="热门户型分布"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    return c
def create_area_price_scatter(df):
    """生成面积与总价关系散点图"""
    c = (
        Scatter()
        .add_xaxis(df['Area'].tolist())
        .add_yaxis("总价(万)", df['TotalPrice'].tolist(), label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="房屋面积与总价关系散点图"),
            xaxis_opts=opts.AxisOpts(type_="value", name="面积(平米)"),
            yaxis_opts=opts.AxisOpts(type_="value", name="总价(万元)"),
            tooltip_opts=opts.TooltipOpts(formatter="{c0}平米, {c1}万元")
        )
    )
    return c

def create_decoration_boxplot(df):
    """生成不同装修情况的房价箱线图 (修正版)"""
    # 1. 创建一个空的箱线图对象
    boxplot_chart = Boxplot()
    
    # 2. 准备X轴数据
    decorations = df['Decoration'].unique().tolist()
    boxplot_chart.add_xaxis(xaxis_data=decorations)
    
    # 3. 准备Y轴数据
    data_by_decoration = [df[df['Decoration'] == d]['TotalPrice'].tolist() for d in decorations]
    
    # 4. 使用箱线图对象自己的 prepare_data 方法处理数据
    prepared_data = boxplot_chart.prepare_data(data_by_decoration)
    
    # 5. 添加Y轴数据
    boxplot_chart.add_yaxis(series_name="总价(万元)", y_axis=prepared_data)
    
    # 6. 设置全局选项
    boxplot_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="不同装修情况的房价分布"),
        tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow")
    )
    
    # 7. 返回完整的图表对象
    return boxplot_chart

def create_community_wordcloud(df):
    """生成热门小区词云 (修正版)"""
    community_counts = df['Community'].value_counts().head(100)
    
    # 显式地将数据转换为 (key, value) 元组的列表
    data_pair = [
        (name, int(count)) for name, count in zip(community_counts.index, community_counts.values)
    ]
    
    c = (
        WordCloud()
        .add(
            series_name="热门小区", 
            data_pair=data_pair, 
            # 调整字体大小范围，确保是合理的整数
            word_size_range=[20, 100],
            # 可以尝试添加 shape 参数，有时能改善渲染效果
            shape='circle' 
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="热门小区词云图",
                title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return c
def create_kmeans_scatter(df_clustered):
    """创建K-Means聚类结果的散点图"""
    scatter = Scatter(init_opts=opts.InitOpts(width="100%", height="600px"))
    scatter.add_xaxis(df_clustered['Area'].tolist())
    
    # 为每个聚类添加一个系列
    for i in sorted(df_clustered['Cluster'].unique()):
        cluster_data = df_clustered[df_clustered['Cluster'] == i]
        scatter.add_yaxis(
            series_name=f'聚类 {i}',
            y_axis=cluster_data['TotalPrice'].tolist(),
            symbol_size=8,
            label_opts=opts.LabelOpts(is_show=False),
        )

    scatter.set_global_opts(
        title_opts=opts.TitleOpts(title="K-Means聚类分析 (面积 vs 总价)"),
        xaxis_opts=opts.AxisOpts(type_="value", name="面积 (平米)"),
        yaxis_opts=opts.AxisOpts(type_="value", name="总价 (万元)"),
        tooltip_opts=opts.TooltipOpts(formatter="面积: {b}平米 <br/> 总价: {c}万元"),
        legend_opts=opts.LegendOpts(pos_left="center"),
    )
    return scatter
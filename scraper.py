# 1_scraper.py (最终稳定版 - 硬编码行政区URL)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin

# ==================== 配置区 ====================
MAX_PAGES_PER_DISTRICT = 3 # 调整此处以控制每个区抓取的页数
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://cd.lianjia.com/ershoufang/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

# --- 核心修改：硬编码行政区URL，不再从首页动态获取 ---
DISTRICT_URLS = {
    '锦江': 'https://cd.lianjia.com/ershoufang/jinjiang/',
    '青羊': 'https://cd.lianjia.com/ershoufang/qingyang/',
    '武侯': 'https://cd.lianjia.com/ershoufang/wuhou/',
    '高新': 'https://cd.lianjia.com/ershoufang/gaoxin7/',
    '成华': 'https://cd.lianjia.com/ershoufang/chenghua/',
    '金牛': 'https://cd.lianjia.com/ershoufang/jinniu/',
    '天府新区': 'https://cd.lianjia.com/ershoufang/tianfuxinqu/',
    '高新西': 'https://cd.lianjia.com/ershoufang/gaoxinxi/',
    '双流': 'https://cd.lianjia.com/ershoufang/shuangliu/',
    '温江': 'https://cd.lianjia.com/ershoufang/wenjiang/',
    '郫都': 'https://cd.lianjia.com/ershoufang/pidou/',
    '龙泉驿': 'https://cd.lianjia.com/ershoufang/longquanyi/',
    '新都': 'https://cd.lianjia.com/ershoufang/xindou/',
    '都江堰': 'https://cd.lianjia.com/ershoufang/doujiangyan/',
    '青白江': 'https://cd.lianjia.com/ershoufang/qingbaijiang/',
}
# ===============================================

def parse_page(html, guaranteed_district):
    """解析单个页面的HTML，并使用已知的正确行政区进行标注"""
    soup = BeautifulSoup(html, 'lxml')
    house_list = soup.select('ul.sellListContent > li.clear')
    
    if not house_list:
        return []

    data = []
    for house in house_list:
        try:
            title = house.select_one('div.title > a').text.strip()
            community = house.select_one('div.positionInfo > a').text.strip()
            position_links = house.select('div.positionInfo > a')
            sub_district = position_links[0].text.strip() if len(position_links) >= 1 else '未知'
            
            house_info_str = house.select_one('div.houseInfo').text.strip()
            parts = house_info_str.split('|')
            layout, area, orientation, decoration, floor, year_built, building_type = (parts + ['未知'] * 7)[:7]

            total_price = house.select_one('div.totalPrice > span').text.strip() + '万'
            unit_price = house.select_one('div.unitPrice > span').text.strip()
            
            follow_info = house.select_one('div.followInfo').text.strip()
            followers = follow_info.split('/')[0].strip()
            elevator = '有电梯' if house.select_one('div.tag > span.elevator') else '无电梯'

            data.append({
                'Title': title, 'Community': community, 'District': guaranteed_district, 'SubDistrict': sub_district.strip(),
                'Layout': layout.strip(), 'Area': area.strip(), 'Orientation': orientation.strip(), 'Decoration': decoration.strip(),
                'Floor': floor.strip(), 'YearBuilt': year_built.strip(), 'BuildingType': building_type.strip(),
                'TotalPrice': total_price, 'UnitPrice': unit_price, 'Followers': followers, 'Elevator': elevator
            })
        except Exception as e:
            print(f"解析房源时出错: {e}")
            continue
    return data

def main():
    """主函数，基于硬编码的URL列表进行分区域爬取"""
    all_data = []
    print("\n" + "="*20 + " 开始基于预设列表进行分区域爬取 " + "="*20)
    
    # --- 核心修改：直接遍历硬编码的字典 ---
    for district_name, district_url in DISTRICT_URLS.items():
        print(f"\n--- 正在处理行政区: {district_name} ---")
        for page in range(1, MAX_PAGES_PER_DISTRICT + 1):
            page_url = f"{district_url.rstrip('/')}/pg{page}/"
            print(f"  正在抓取第 {page} 页: {page_url}")
            
            try:
                response = requests.get(page_url, headers=HEADERS, timeout=10)
                if response.status_code == 404:
                    print(f"  第 {page} 页不存在 (404)，结束抓取 {district_name} 区。")
                    break
                response.raise_for_status()
                
                page_data = parse_page(response.text, district_name)
                
                if not page_data:
                    print(f"  第 {page} 页没有数据，结束抓取 {district_name} 区。")
                    break
                    
                all_data.extend(page_data)
                print(f"  成功抓取 {len(page_data)} 条数据。当前总数: {len(all_data)}")
                
                sleep_time = random.uniform(1.5, 3.5)
                time.sleep(sleep_time)
                
            except requests.RequestException as e:
                print(f"  请求第 {page} 页失败: {e}")
                break

    if all_data:
        df = pd.DataFrame(all_data)
        cols_order = [
            'Title', 'Community', 'District', 'SubDistrict', 'TotalPrice', 'UnitPrice', 'Area', 
            'Layout', 'Orientation', 'Decoration', 'Floor', 'YearBuilt', 'BuildingType', 
            'Followers', 'Elevator'
        ]
        df = df.reindex(columns=cols_order)
        
        df.to_csv('chengdu_raw_data.csv', index=False, encoding='utf-8-sig')
        print(f"\n" + "="*20 + " 全部抓取完成 " + "="*20)
        print(f"共抓取 {len(df)} 条房源信息。")
        print("原始数据已保存至 chengdu_raw_data.csv")
        print("\n数据预览:")
        print(df.head())
    else:
        print("未能抓取到任何数据。")

if __name__ == '__main__':
    main()
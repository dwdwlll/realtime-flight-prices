#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示执行脚本 / Demo Execution Script

演示航班查询系统的完整功能，包括模拟数据和爬虫框架
Demonstrates the complete flight query system functionality
"""

import sys
from datetime import datetime

def demo_basic_search():
    """演示基本搜索功能"""
    print("=" * 70)
    print("演示1：基本航班搜索")
    print("=" * 70)
    
    try:
        from Main import FlightSearchEngine
        
        engine = FlightSearchEngine()
        
        # 搜索单程航班
        print("\n[搜索] 北京 -> 上海 (2025-01-15)")
        flights = engine.search_flights("北京", "上海", "2025-01-15")
        
        print(f"\n找到 {len(flights)} 个航班：")
        for i, flight in enumerate(flights[:5], 1):
            print(f"{i}. {flight}")
        
        if len(flights) > 5:
            print(f"... 还有 {len(flights) - 5} 个航班")
        
        return True
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_multi_city():
    """演示多城市行程规划"""
    print("\n" + "=" * 70)
    print("演示2：多城市行程规划")
    print("=" * 70)
    
    try:
        from Main import FlightSearchEngine
        
        engine = FlightSearchEngine()
        
        # 多城市行程
        cities = ["北京", "上海", "广州", "深圳"]
        dates = ["2025-01-15", "2025-01-16", "2025-01-17"]
        
        print(f"\n[规划] 行程路线: {' -> '.join(cities)}")
        print(f"[日期] {', '.join(dates)}")
        print("\n正在搜索...")
        
        itineraries = engine.plan_itinerary(cities, dates)
        
        print(f"\n找到 {len(itineraries)} 个可行方案")
        
        # 显示前3个最便宜的方案
        print("\n【Top 3 最便宜方案】")
        for i, itinerary in enumerate(itineraries[:3], 1):
            print(f"\n方案 {i}:")
            print(itinerary)
            print("-" * 70)
        
        return True
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_price_comparison():
    """演示价格排序功能"""
    print("\n" + "=" * 70)
    print("演示3：价格排序和比较")
    print("=" * 70)
    
    try:
        from Main import FlightSearchEngine
        
        engine = FlightSearchEngine()
        
        # 搜索并比较价格
        cities = ["北京", "上海", "广州"]
        itineraries = engine.plan_itinerary(cities)
        
        if not itineraries:
            print("未找到航班")
            return False
        
        print(f"\n[分析] 共 {len(itineraries)} 个方案")
        
        # 价格统计
        prices = [it.total_price for it in itineraries]
        min_price = min(prices)
        max_price = max(prices)
        avg_price = sum(prices) / len(prices)
        
        print(f"\n价格范围:")
        print(f"  最低价: ¥{min_price:.2f}")
        print(f"  最高价: ¥{max_price:.2f}")
        print(f"  平均价: ¥{avg_price:.2f}")
        print(f"  价差:   ¥{max_price - min_price:.2f}")
        
        # 显示最便宜和最贵的方案
        print(f"\n【最便宜方案】 ¥{itineraries[0].total_price:.2f}")
        print(itineraries[0])
        
        print(f"\n【最贵方案】 ¥{itineraries[-1].total_price:.2f}")
        print(itineraries[-1])
        
        return True
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_cache_mechanism():
    """演示缓存机制"""
    print("\n" + "=" * 70)
    print("演示4：缓存机制")
    print("=" * 70)
    
    try:
        from Main import FlightSearchEngine
        import time
        
        engine = FlightSearchEngine()
        
        print(f"\n缓存超时时间: {engine.CACHE_TIMEOUT_SECONDS} 秒")
        
        # 第一次搜索
        print("\n[第1次搜索] 北京 -> 上海")
        start = time.time()
        flights1 = engine.search_flights("北京", "上海", "2025-01-15")
        time1 = time.time() - start
        print(f"用时: {time1:.3f}秒, 找到{len(flights1)}个航班")
        
        # 第二次搜索（应该使用缓存）
        print("\n[第2次搜索] 北京 -> 上海 (应使用缓存)")
        start = time.time()
        flights2 = engine.search_flights("北京", "上海", "2025-01-15")
        time2 = time.time() - start
        print(f"用时: {time2:.3f}秒, 找到{len(flights2)}个航班")
        
        # 验证缓存
        if len(flights1) == len(flights2):
            print("\n✓ 缓存机制工作正常")
            print(f"  加速比: {time1/time2:.1f}x")
        else:
            print("\n⚠ 缓存可能未生效")
        
        # 等待缓存过期
        print(f"\n[等待] {engine.CACHE_TIMEOUT_SECONDS + 1}秒后缓存将过期...")
        time.sleep(engine.CACHE_TIMEOUT_SECONDS + 1)
        
        # 第三次搜索（缓存已过期）
        print("\n[第3次搜索] 北京 -> 上海 (缓存已过期)")
        start = time.time()
        flights3 = engine.search_flights("北京", "上海", "2025-01-15")
        time3 = time.time() - start
        print(f"用时: {time3:.3f}秒, 找到{len(flights3)}个航班")
        
        print("\n✓ 缓存过期后重新获取数据")
        
        return True
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_data_source_switching():
    """演示数据源切换"""
    print("\n" + "=" * 70)
    print("演示5：数据源切换")
    print("=" * 70)
    
    print("""
系统支持三种数据源模式：

【模式1】模拟数据 (当前)
  - 使用: _generate_mock_flights()
  - 特点: 随机生成，无需网络
  - 用途: 演示和开发测试
  - 状态: ✓ 已启用

【模式2】网页爬虫
  - 使用: _fetch_flights_by_web_scraping()
  - 特点: 爬取真实网站数据
  - 依赖: requests + beautifulsoup4 或 selenium
  - 状态: ✗ 需要配置
  - 配置步骤:
    1. 安装依赖: pip install requests beautifulsoup4 lxml
    2. 在Main.py中取消注释爬虫代码
    3. 调整CSS选择器匹配目标网站
    4. 切换数据源调用

【模式3】API集成
  - 使用: _fetch_real_flights_from_api()
  - 特点: 调用官方API
  - 依赖: requests + API密钥
  - 状态: ✗ 需要配置
  - 配置步骤:
    1. 获取API密钥 (如Amadeus)
    2. 设置环境变量
    3. 在Main.py中取消注释API代码
    4. 切换数据源调用

切换示例（在Main.py的search_flights方法中）:
```python
# 当前使用模拟数据
flights = self._generate_mock_flights(departure, arrival, date)

# 切换到爬虫
# flights = self._fetch_flights_by_web_scraping(departure, arrival, date)

# 切换到API
# flights = self._fetch_real_flights_from_api(departure, arrival, date)
```
""")
    return True


def show_scraping_status():
    """显示爬虫配置状态"""
    print("\n" + "=" * 70)
    print("网页爬虫配置状态")
    print("=" * 70)
    
    # 检查依赖
    dependencies = {
        "requests": "HTTP请求库",
        "bs4": "BeautifulSoup (HTML解析)",
        "lxml": "lxml (HTML解析器)",
        "selenium": "Selenium (浏览器自动化)",
        "webdriver_manager": "WebDriver管理器"
    }
    
    print("\n【依赖检查】")
    for module, desc in dependencies.items():
        try:
            __import__(module)
            print(f"  ✓ {module:20s} - {desc}")
        except ImportError:
            print(f"  ✗ {module:20s} - {desc} (未安装)")
    
    # 显示安装命令
    print("\n【安装命令】")
    print("  静态爬虫: pip install requests beautifulsoup4 lxml")
    print("  动态爬虫: pip install selenium webdriver-manager")
    print("  完整安装: pip install requests beautifulsoup4 lxml selenium webdriver-manager")
    
    # 显示配置文件
    print("\n【配置文件】")
    print("  Main.py              - 主程序（包含爬虫框架）")
    print("  WEB_SCRAPING_GUIDE.md - 爬虫详细指南")
    print("  test_web_scraping.py  - 爬虫测试脚本")


def main():
    """主演示流程"""
    print("\n" + "=" * 70)
    print("       航班查询系统 - 功能演示")
    print("   Flight Query System - Feature Demo")
    print("=" * 70)
    print(f"演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    demos = [
        ("基本搜索", demo_basic_search),
        ("多城市规划", demo_multi_city),
        ("价格比较", demo_price_comparison),
        ("缓存机制", demo_cache_mechanism),
        ("数据源切换", demo_data_source_switching),
    ]
    
    results = []
    
    for name, demo_func in demos:
        try:
            print(f"\n正在运行: {name}...")
            result = demo_func()
            results.append((name, result))
        except KeyboardInterrupt:
            print("\n\n用户中断")
            break
        except Exception as e:
            print(f"演示异常: {e}")
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 70)
    print("演示结果总结")
    print("=" * 70)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    # 显示爬虫状态
    show_scraping_status()
    
    # 使用指南
    print("\n" + "=" * 70)
    print("使用指南")
    print("=" * 70)
    print("""
【运行主程序】
  python Main.py
  
【测试爬虫功能】
  python test_web_scraping.py
  
【查看文档】
  - README.md              - 项目说明
  - WEB_SCRAPING_GUIDE.md  - 爬虫指南
  - API_INTEGRATION_GUIDE.md - API指南
  
【配置真实数据源】
  1. 选择数据源（爬虫或API）
  2. 安装相应依赖
  3. 修改Main.py配置
  4. 测试验证
""")
    
    print("=" * 70)
    passed = sum(1 for _, r in results if r)
    print(f"完成: {passed}/{len(results)} 个演示成功")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n程序已退出")
        sys.exit(0)

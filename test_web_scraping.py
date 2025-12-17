#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页爬虫测试脚本 / Web Scraping Test Script

测试网页爬虫功能，验证爬虫框架是否正常工作
Test web scraping functionality to verify the framework works correctly
"""

import sys
import time
from datetime import datetime

def test_static_scraping():
    """测试静态页面爬虫 (requests + BeautifulSoup)"""
    print("=" * 70)
    print("测试方案A：静态页面爬虫 (requests + BeautifulSoup)")
    print("=" * 70)
    
    try:
        import requests
        from bs4 import BeautifulSoup
        print("✓ 依赖已安装: requests, beautifulsoup4")
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请安装: pip install requests beautifulsoup4 lxml")
        return False
    
    # 测试1：检查基本功能
    print("\n[测试1] 基本HTTP请求...")
    try:
        # 使用一个公开的测试API来验证网络连接
        response = requests.get('https://httpbin.org/get', timeout=10)
        if response.status_code == 200:
            print("✓ HTTP请求成功")
        else:
            print(f"✗ HTTP请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ 网络连接失败: {e}")
        print("提示：请检查网络连接")
        return False
    
    # 测试2：HTML解析
    print("\n[测试2] HTML解析功能...")
    try:
        html_sample = """
        <html>
            <div class="flight-card">
                <span class="flight-number">CA1234</span>
                <span class="airline-name">中国国航</span>
                <span class="departure-time">08:30</span>
                <span class="arrival-time">10:45</span>
                <span class="price-value">¥850</span>
            </div>
        </html>
        """
        soup = BeautifulSoup(html_sample, 'html.parser')
        
        # 测试选择器
        flight_card = soup.select_one('.flight-card')
        flight_no = flight_card.select_one('.flight-number').text
        airline = flight_card.select_one('.airline-name').text
        price_text = flight_card.select_one('.price-value').text
        
        if flight_no == "CA1234" and airline == "中国国航":
            print("✓ HTML解析和CSS选择器工作正常")
            print(f"  提取结果: {flight_no} | {airline} | {price_text}")
        else:
            print("✗ HTML解析失败")
            return False
    except Exception as e:
        print(f"✗ HTML解析错误: {e}")
        return False
    
    # 测试3：价格提取
    print("\n[测试3] 价格数据清洗...")
    try:
        test_prices = ["¥850", "850元", "850.50", "RMB 1,250.00"]
        for price_text in test_prices:
            # 清洗价格
            price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
            print(f"  '{price_text}' -> {price}")
        print("✓ 价格提取功能正常")
    except Exception as e:
        print(f"✗ 价格提取失败: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✓ 静态页面爬虫测试通过")
    print("=" * 70)
    return True


def test_selenium_scraping():
    """测试动态页面爬虫 (Selenium)"""
    print("\n" + "=" * 70)
    print("测试方案B：动态页面爬虫 (Selenium)")
    print("=" * 70)
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        print("✓ 依赖已安装: selenium")
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请安装: pip install selenium webdriver-manager")
        return False
    
    # 测试1：Chrome配置
    print("\n[测试1] Chrome浏览器配置...")
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        print("✓ Chrome选项配置成功")
    except Exception as e:
        print(f"✗ 配置失败: {e}")
        return False
    
    # 测试2：WebDriver初始化
    print("\n[测试2] WebDriver初始化...")
    driver = None
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✓ WebDriver初始化成功")
    except Exception as e:
        print(f"✗ WebDriver初始化失败: {e}")
        print("提示：可能需要安装Chrome浏览器或ChromeDriver")
        print("      或安装: pip install webdriver-manager")
        return False
    
    try:
        # 测试3：页面访问
        print("\n[测试3] 访问测试页面...")
        try:
            # 使用一个简单的测试页面
            driver.get('https://httpbin.org/html')
            time.sleep(2)
            
            # 获取页面标题
            page_source = driver.page_source
            if 'html' in page_source.lower():
                print("✓ 页面访问成功")
                print(f"  页面内容长度: {len(page_source)} 字符")
            else:
                print("✗ 页面访问失败")
                return False
        except Exception as e:
            print(f"✗ 页面访问错误: {e}")
            return False
        
        # 测试4：元素查找
        print("\n[测试4] 元素查找功能...")
        try:
            # 尝试查找页面元素
            elements = driver.find_elements(By.TAG_NAME, 'p')
            if elements:
                print(f"✓ 成功找到 {len(elements)} 个段落元素")
            else:
                print("⚠ 未找到元素（可能是正常的）")
        except Exception as e:
            print(f"✗ 元素查找错误: {e}")
            return False
        
        print("\n" + "=" * 70)
        print("✓ Selenium爬虫测试通过")
        print("=" * 70)
        return True
    
    finally:
        if driver:
            driver.quit()
            print("\n[清理] WebDriver已关闭")


def test_main_integration():
    """测试Main.py集成"""
    print("\n" + "=" * 70)
    print("测试Main.py爬虫集成")
    print("=" * 70)
    
    try:
        # 导入Main模块
        import Main
        print("✓ Main.py模块导入成功")
        
        # 检查关键类
        print("\n[检查] 关键类和方法...")
        engine = Main.FlightSearchEngine()
        
        # 检查方法是否存在
        methods = [
            '_fetch_flights_by_web_scraping',
            '_fetch_real_flights_from_api',
            '_generate_mock_flights',
            'search_flights',
            'plan_itinerary'
        ]
        
        for method in methods:
            if hasattr(engine, method):
                print(f"  ✓ {method}")
            else:
                print(f"  ✗ {method} 不存在")
                return False
        
        # 测试模拟数据生成（作为基准）
        print("\n[测试] 模拟数据生成...")
        flights = engine._generate_mock_flights("北京", "上海", "2025-01-15")
        if flights and len(flights) > 0:
            print(f"✓ 生成了 {len(flights)} 个模拟航班")
            print(f"  示例: {flights[0]}")
        else:
            print("✗ 模拟数据生成失败")
            return False
        
        print("\n" + "=" * 70)
        print("✓ Main.py集成测试通过")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_next_steps():
    """显示下一步操作指南"""
    print("\n" + "=" * 70)
    print("下一步操作指南")
    print("=" * 70)
    
    print("""
要启用实际网站爬虫，请按以下步骤操作：

【步骤1】选择目标网站并分析结构
  1. 打开目标网站（如携程、去哪儿）
  2. 按F12打开开发者工具
  3. 使用选择器工具（Ctrl+Shift+C）分析HTML结构
  4. 记录航班信息的CSS选择器

【步骤2】修改Main.py
  在 _fetch_flights_by_web_scraping() 方法中：
  
  方案A (静态页面):
    - 取消注释第117-190行的代码
    - 修改URL格式和选择器
  
  方案B (动态页面):
    - 取消注释第192-254行的代码
    - 修改URL格式和选择器

【步骤3】调整选择器示例
  # 根据实际网页结构调整
  flight_items = soup.select('.flight-card')  # 或其他选择器
  flight_no = item.select_one('.flight-number').text
  airline = item.select_one('.airline-name').text
  dep_time = item.select_one('.dep-time').text
  arr_time = item.select_one('.arr-time').text
  price_text = item.select_one('.price').text

【步骤4】切换数据源
  在 search_flights() 方法中（约第106行）：
  
  # 注释掉模拟数据
  # flights = self._generate_mock_flights(departure, arrival, date)
  
  # 启用爬虫
  flights = self._fetch_flights_by_web_scraping(departure, arrival, date)

【步骤5】测试运行
  python Main.py

【注意事项】
  ⚠ 遵守网站服务条款和robots.txt
  ⚠ 控制爬取频率（建议1-3秒间隔）
  ⚠ 处理反爬虫机制（验证码、IP封禁等）
  ⚠ 仅用于个人学习和研究

【详细文档】
  参考 WEB_SCRAPING_GUIDE.md 获取完整示例和故障排查指南
""")


def main():
    """主测试流程"""
    print("\n" + "=" * 70)
    print("           航班爬虫功能测试")
    print("    Flight Scraping Functionality Test")
    print("=" * 70)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = []
    
    # 测试1：静态爬虫
    print("\n开始测试...")
    try:
        result = test_static_scraping()
        results.append(("静态页面爬虫", result))
    except Exception as e:
        print(f"测试异常: {e}")
        results.append(("静态页面爬虫", False))
    
    # 测试2：Selenium爬虫
    try:
        result = test_selenium_scraping()
        results.append(("Selenium爬虫", result))
    except Exception as e:
        print(f"测试异常: {e}")
        results.append(("Selenium爬虫", False))
    
    # 测试3：Main.py集成
    try:
        result = test_main_integration()
        results.append(("Main.py集成", result))
    except Exception as e:
        print(f"测试异常: {e}")
        results.append(("Main.py集成", False))
    
    # 显示测试总结
    print("\n" + "=" * 70)
    print("测试结果总结")
    print("=" * 70)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("\n" + "=" * 70)
    print(f"总计: {passed}/{total} 项测试通过")
    print("=" * 70)
    
    # 显示下一步指南
    show_next_steps()
    
    # 返回状态码
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

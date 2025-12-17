#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时航班价格查询系统
Real-time Flight Price Query System

支持多城市行程规划，实时价格查询，按价格排序
Supports multi-city itinerary planning, real-time price queries, and price sorting
"""

import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import os
import sys


class Flight:
    """航班信息类"""
    def __init__(self, flight_no: str, airline: str, departure: str, 
                 arrival: str, dep_time: str, arr_time: str, price: float,
                 date: str = None):
        self.flight_no = flight_no
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.price = price
        self.date = date  # 日期
    
    def __repr__(self):
        date_str = f"{self.date} " if self.date else ""
        return (f"航班{self.flight_no} | {self.airline} | "
                f"{self.departure}->{self.arrival} | "
                f"{date_str}{self.dep_time}-{self.arr_time} | ¥{self.price:.2f}")


class Itinerary:
    """行程方案类"""
    def __init__(self, flights: List[Flight]):
        self.flights = flights
        self.total_price = sum(f.price for f in flights)
    
    def __repr__(self):
        route = " -> ".join([self.flights[0].departure] + 
                           [f.arrival for f in self.flights])
        flights_str = "\n    ".join([str(f) for f in self.flights])
        return (f"\n行程路线: {route}\n"
                f"总价: ¥{self.total_price:.2f}\n"
                f"航班详情:\n    {flights_str}")


class FlightSearchEngine:
    """航班搜索引擎"""
    
    # 模拟航空公司数据
    AIRLINES = [
        "中国国航", "南方航空", "东方航空", "海南航空", "厦门航空",
        "深圳航空", "四川航空", "山东航空", "春秋航空", "吉祥航空"
    ]
    
    # 常见城市数据
    CITIES = [
        "北京", "上海", "广州", "深圳", "成都", "杭州", "西安", 
        "重庆", "武汉", "南京", "天津", "郑州", "长沙", "沈阳",
        "青岛", "厦门", "大连", "昆明", "哈尔滨", "济南"
    ]
    
    # 配置常量
    CACHE_TIMEOUT_SECONDS = 5  # 缓存超时时间（秒）
    MAX_ITINERARIES = 50  # 最多返回的行程方案数量
    
    def __init__(self):
        self.cache = {}  # 缓存查询结果
        self.last_update = {}  # 记录上次更新时间
    
    def search_flights(self, departure: str, arrival: str, 
                      date: str = None) -> List[Flight]:
        """
        搜索航班
        
        Args:
            departure: 出发地
            arrival: 目的地
            date: 日期（可选）
        
        Returns:
            航班列表
        """
        # 生成缓存key
        cache_key = f"{departure}-{arrival}-{date or 'no_date'}"
        
        # 检查缓存
        current_time = time.time()
        if (cache_key in self.cache and 
            current_time - self.last_update.get(cache_key, 0) < self.CACHE_TIMEOUT_SECONDS):
            return self.cache[cache_key]
        
        # 模拟API查询延迟（实际API调用时可以移除此行）
        time.sleep(random.uniform(0.1, 0.3))
        
        # 获取航班数据（可切换数据源）
        # 方法1：使用模拟数据（当前默认）
        flights = self._generate_mock_flights(departure, arrival, date)
        
        # 方法2：使用网页爬虫（需要安装依赖并配置）
        # flights = self._fetch_flights_by_web_scraping(departure, arrival, date)
        
        # 方法3：使用真实API（配置API密钥后可启用）
        # flights = self._fetch_real_flights_from_api(departure, arrival, date)
        
        # 更新缓存
        self.cache[cache_key] = flights
        self.last_update[cache_key] = current_time
        
        return flights
    
    def _fetch_flights_by_web_scraping(self, departure: str, arrival: str, date: str = None) -> List[Flight]:
        """
        通过网页爬虫获取航班数据（模拟网页搜索）
        
        支持的网站：
        1. 携程 (Ctrip) - 需要安装 selenium
        2. 去哪儿 (Qunar) - 需要安装 requests + beautifulsoup4
        3. 飞猪 (Fliggy) - 需要安装 selenium
        
        依赖安装：
        pip install selenium beautifulsoup4 requests webdriver-manager
        
        注意：网页爬虫可能受到以下限制：
        - 网站反爬虫机制（需要设置User-Agent、代理等）
        - 页面结构变化导致爬虫失效
        - 需要处理动态加载的内容（JavaScript渲染）
        - 可能需要验证码识别
        """
        # 方案1：使用 requests + BeautifulSoup 爬取静态页面
        # 适用于页面结构简单、无需JavaScript渲染的网站
        # try:
        #     import requests
        #     from bs4 import BeautifulSoup
        #     
        #     # 城市名称到拼音的映射（用于URL构建）
        #     city_pinyin = {
        #         "北京": "beijing", "上海": "shanghai", "广州": "guangzhou",
        #         "深圳": "shenzhen", "成都": "chengdu", "杭州": "hangzhou"
        #     }
        #     
        #     dep_py = city_pinyin.get(departure, "beijing")
        #     arr_py = city_pinyin.get(arrival, "shanghai")
        #     search_date = date or datetime.now().strftime("%Y-%m-%d")
        #     
        #     # 构建搜索URL（示例：去哪儿网格式）
        #     url = f"https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport={dep_py}&searchArrivalAirport={arr_py}&searchDepartureTime={search_date}"
        #     
        #     headers = {
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        #     }
        #     
        #     response = requests.get(url, headers=headers, timeout=15)
        #     response.raise_for_status()
        #     
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     
        #     # 解析航班信息（需要根据实际网页结构调整选择器）
        #     flights = []
        #     flight_items = soup.select('.flight-item')  # 示例选择器
        #     
        #     for item in flight_items[:10]:  # 限制返回数量
        #         try:
        #             flight_no = item.select_one('.flight-number').text.strip()
        #             airline = item.select_one('.airline-name').text.strip()
        #             dep_time = item.select_one('.dep-time').text.strip()
        #             arr_time = item.select_one('.arr-time').text.strip()
        #             price_text = item.select_one('.price').text.strip()
        #             price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
        #             
        #             flight = Flight(flight_no, airline, departure, arrival,
        #                           dep_time, arr_time, price, date)
        #             flights.append(flight)
        #         except Exception as e:
        #             continue
        #     
        #     if flights:
        #         return flights
        # except Exception as e:
        #     print(f"网页爬取失败: {e}")
        
        # 方案2：使用 Selenium 爬取动态页面
        # 适用于需要JavaScript渲染的网站（如携程、飞猪）
        # try:
        #     from selenium import webdriver
        #     from selenium.webdriver.common.by import By
        #     from selenium.webdriver.support.ui import WebDriverWait
        #     from selenium.webdriver.support import expected_conditions as EC
        #     from selenium.webdriver.chrome.options import Options
        #     from webdriver_manager.chrome import ChromeDriverManager
        #     
        #     # 配置浏览器选项
        #     chrome_options = Options()
        #     chrome_options.add_argument('--headless')  # 无头模式
        #     chrome_options.add_argument('--no-sandbox')
        #     chrome_options.add_argument('--disable-dev-shm-usage')
        #     chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        #     chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        #     
        #     # 初始化浏览器
        #     from selenium.webdriver.chrome.service import Service
        #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        #     
        #     try:
        #         # 构建搜索URL（示例：携程格式）
        #         search_date = date or datetime.now().strftime("%Y-%m-%d")
        #         url = f"https://flights.ctrip.com/online/list/oneway-{departure}-{arrival}?depdate={search_date}"
        #         
        #         driver.get(url)
        #         
        #         # 等待页面加载
        #         wait = WebDriverWait(driver, 10)
        #         wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'flight-list')))
        #         
        #         # 解析航班信息
        #         flights = []
        #         flight_elements = driver.find_elements(By.CLASS_NAME, 'flight-item')
        #         
        #         for elem in flight_elements[:10]:
        #             try:
        #                 flight_no = elem.find_element(By.CLASS_NAME, 'flight-number').text
        #                 airline = elem.find_element(By.CLASS_NAME, 'airline-name').text
        #                 dep_time = elem.find_element(By.CLASS_NAME, 'dep-time').text
        #                 arr_time = elem.find_element(By.CLASS_NAME, 'arr-time').text
        #                 price_text = elem.find_element(By.CLASS_NAME, 'price').text
        #                 price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
        #                 
        #                 flight = Flight(flight_no, airline, departure, arrival,
        #                               dep_time, arr_time, price, date)
        #                 flights.append(flight)
        #             except Exception:
        #                 continue
        #         
        #         driver.quit()
        #         
        #         if flights:
        #             return flights
        #     finally:
        #         driver.quit()
        # except Exception as e:
        #     print(f"Selenium爬取失败: {e}")
        
        # 爬虫未配置或失败，回退到模拟数据
        print("提示：网页爬虫未配置或失败，使用模拟数据。")
        print("如需启用爬虫，请：")
        print("1. 安装依赖: pip install selenium beautifulsoup4 requests webdriver-manager")
        print("2. 在上述代码中取消注释并根据目标网站调整选择器")
        return self._generate_mock_flights(departure, arrival, date)
    
    def _fetch_real_flights_from_api(self, departure: str, arrival: str, date: str = None) -> List[Flight]:
        """
        从真实API获取航班数据（需要配置API密钥）
        
        集成示例：
        1. Amadeus API: https://developers.amadeus.com/
        2. Skyscanner API: https://partners.skyscanner.net/
        3. 携程API: 需商业合作
        
        使用方法：
        - 在环境变量中设置 API_KEY 和 API_SECRET
        - 取消下面代码的注释并根据API文档调整
        """
        # 示例：使用 requests 库调用API（需先安装：pip install requests）
        # import requests
        # 
        # api_key = os.environ.get('FLIGHT_API_KEY', '')
        # if not api_key:
        #     raise ValueError("请设置环境变量 FLIGHT_API_KEY")
        # 
        # # API请求示例（以Amadeus为例）
        # url = "https://api.amadeus.com/v2/shopping/flight-offers"
        # headers = {
        #     "Authorization": f"Bearer {api_key}"
        # }
        # params = {
        #     "originLocationCode": departure,
        #     "destinationLocationCode": arrival,
        #     "departureDate": date or datetime.now().strftime("%Y-%m-%d"),
        #     "adults": 1,
        #     "max": 10
        # }
        # 
        # try:
        #     response = requests.get(url, headers=headers, params=params, timeout=10)
        #     response.raise_for_status()
        #     data = response.json()
        #     
        #     # 解析API响应并创建Flight对象
        #     flights = []
        #     for offer in data.get('data', []):
        #         for itinerary in offer.get('itineraries', []):
        #             for segment in itinerary.get('segments', []):
        #                 flight_no = segment.get('carrierCode', '') + segment.get('number', '')
        #                 airline = segment.get('carrier', {}).get('name', '')
        #                 dep_time = segment.get('departure', {}).get('at', '').split('T')[1][:5]
        #                 arr_time = segment.get('arrival', {}).get('at', '').split('T')[1][:5]
        #                 price = float(offer.get('price', {}).get('total', 0))
        #                 
        #                 flight = Flight(flight_no, airline, departure, arrival,
        #                               dep_time, arr_time, price, date)
        #                 flights.append(flight)
        #     
        #     return flights
        # except Exception as e:
        #     print(f"API调用失败: {e}")
        #     # 失败时回退到模拟数据
        #     return self._generate_mock_flights(departure, arrival, date)
        
        # 当前未配置API，使用模拟数据
        print("提示：当前使用模拟数据。如需真实数据，请配置API密钥并启用上述代码。")
        return self._generate_mock_flights(departure, arrival, date)
    
    def _generate_mock_flights(self, departure: str, arrival: str, date: str = None) -> List[Flight]:
        """生成模拟航班数据（用于演示和测试）"""
        num_flights = random.randint(3, 8)
        flights = []
        
        for i in range(num_flights):
            # 生成航班号
            airline = random.choice(self.AIRLINES)
            flight_no = f"{airline[:2]}{random.randint(1000, 9999)}"
            
            # 生成时间
            dep_hour = random.randint(6, 22)
            dep_minute = random.choice([0, 15, 30, 45])
            dep_time = f"{dep_hour:02d}:{dep_minute:02d}"
            
            flight_duration = random.randint(1, 4)
            arr_hour = (dep_hour + flight_duration) % 24
            arr_minute = (dep_minute + random.randint(0, 45)) % 60
            arr_time = f"{arr_hour:02d}:{arr_minute:02d}"
            
            # 生成价格（基础价格 + 随机浮动）
            base_price = random.uniform(500, 2000)
            # 添加价格波动模拟实时变化
            price_fluctuation = random.uniform(-50, 50)
            price = base_price + price_fluctuation
            
            flight = Flight(flight_no, airline, departure, arrival,
                          dep_time, arr_time, price, date)
            flights.append(flight)
        
        return flights
    
    def plan_itinerary(self, cities: List[str], dates: List[str] = None) -> List[Itinerary]:
        """
        规划多城市行程
        
        Args:
            cities: 城市列表，按顺序包含出发地、途径地、目的地
            dates: 日期列表，每段行程的日期（可选）
        
        Returns:
            可行的行程方案列表
        """
        if len(cities) < 2:
            return []
        
        # 获取每段航班
        all_segments = []
        for i in range(len(cities) - 1):
            date = dates[i] if dates and i < len(dates) else None
            date_str = f" ({date})" if date else ""
            print(f"正在搜索 {cities[i]} -> {cities[i+1]}{date_str} 的航班...")
            flights = self.search_flights(cities[i], cities[i+1], date)
            all_segments.append(flights)
        
        # 生成所有可能的组合
        itineraries = self._generate_combinations(all_segments)
        
        # 按价格排序
        itineraries.sort(key=lambda x: x.total_price)
        
        return itineraries
    
    def _generate_combinations(self, segments: List[List[Flight]]) -> List[Itinerary]:
        """生成所有航班组合"""
        if not segments:
            return []
        
        if len(segments) == 1:
            return [Itinerary([flight]) for flight in segments[0]]
        
        # 递归生成组合
        result = []
        first_segment = segments[0]
        remaining_combinations = self._generate_combinations(segments[1:])
        
        for flight in first_segment:
            for combo in remaining_combinations:
                result.append(Itinerary([flight] + combo.flights))
        
        # 限制返回数量以避免组合爆炸
        return result[:self.MAX_ITINERARIES]


class FlightPriceApp:
    """航班价格查询应用主类"""
    
    # 配置常量
    AUTO_REFRESH_INTERVAL_SECONDS = 10  # 自动刷新间隔（秒）
    
    def __init__(self):
        self.engine = FlightSearchEngine()
        self.current_cities = []
        self.current_dates = []
        self.current_itineraries = []
    
    def clear_screen(self):
        """清空屏幕"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """打印标题"""
        print("=" * 70)
        print(" " * 20 + "实时航班价格查询系统")
        print(" " * 15 + "Real-time Flight Price Query System")
        print("=" * 70)
        print()
    
    def get_cities_input(self) -> Tuple[List[str], List[str]]:
        """获取城市和日期输入"""
        print("请输入行程城市（至少2个城市，用逗号或空格分隔）")
        print("例如：北京,上海,广州  或  北京 上海 广州")
        print("支持多个途径地（大于3个城市）")
        print()
        
        user_input = input("请输入城市列表: ").strip()
        
        # 支持逗号或空格分隔
        if ',' in user_input:
            cities = [city.strip() for city in user_input.split(',')]
        else:
            cities = [city.strip() for city in user_input.split()]
        
        # 过滤空字符串
        cities = [city for city in cities if city]
        
        if len(cities) < 2:
            print("\n错误：至少需要输入2个城市！")
            time.sleep(2)
            return [], []
        
        # 获取每段行程的日期
        print()
        print("请输入每段行程的日期（格式：YYYY-MM-DD，用逗号或空格分隔）")
        print(f"需要输入 {len(cities)-1} 个日期（对应 {len(cities)-1} 段行程）")
        print("例如：2025-01-15,2025-01-16  或  2025-01-15 2025-01-16")
        print("（如果不输入日期，直接按回车跳过）")
        print()
        
        date_input = input("请输入日期列表: ").strip()
        
        dates = []
        if date_input:
            # 支持逗号或空格分隔
            if ',' in date_input:
                dates = [date.strip() for date in date_input.split(',')]
            else:
                dates = [date.strip() for date in date_input.split()]
            
            # 过滤空字符串
            dates = [date for date in dates if date]
            
            # 验证日期格式
            valid_dates = []
            for date in dates:
                try:
                    # 验证日期格式
                    datetime.strptime(date, "%Y-%m-%d")
                    valid_dates.append(date)
                except ValueError:
                    print(f"\n警告：日期格式错误 '{date}'，应为 YYYY-MM-DD 格式，已忽略")
                    time.sleep(1)
            
            dates = valid_dates
            
            # 检查日期数量
            if len(dates) != len(cities) - 1:
                print(f"\n警告：有效日期数量({len(dates)})与行程段数({len(cities)-1})不匹配")
                print("将按顺序使用已输入的日期，缺少的将不显示")
                time.sleep(2)
        
        return cities, dates
    
    def display_itineraries(self, itineraries: List[Itinerary], 
                           refresh_time: str = None):
        """显示行程方案"""
        self.clear_screen()
        self.print_header()
        
        if refresh_time:
            print(f"最后更新时间: {refresh_time}")
        
        # 构建行程路线显示（包含日期）
        route_parts = []
        for i, city in enumerate(self.current_cities):
            if i < len(self.current_cities) - 1 and self.current_dates and i < len(self.current_dates):
                route_parts.append(f"{city}({self.current_dates[i]})")
            else:
                route_parts.append(city)
        
        print(f"行程路线: {' -> '.join(route_parts)}")
        print(f"找到 {len(itineraries)} 个可行方案（已按价格从低到高排序）")
        print("-" * 70)
        
        if not itineraries:
            print("\n未找到可行的航班组合")
            return
        
        # 显示前10个最便宜的方案
        for idx, itinerary in enumerate(itineraries[:10], 1):
            print(f"\n方案 {idx}:{itinerary}")
            print("-" * 70)
        
        if len(itineraries) > 10:
            print(f"\n... 还有 {len(itineraries) - 10} 个方案未显示 ...")
    
    def search_menu(self):
        """搜索菜单"""
        cities, dates = self.get_cities_input()
        
        if not cities:
            return
        
        self.current_cities = cities
        self.current_dates = dates
        
        # 显示加载动画
        self.clear_screen()
        self.print_header()
        print("正在搜索航班信息，请稍候...")
        print()
        
        # 搜索航班
        itineraries = self.engine.plan_itinerary(cities, dates)
        self.current_itineraries = itineraries
        
        # 显示结果
        refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.display_itineraries(itineraries, refresh_time)
    
    def refresh_prices(self):
        """刷新价格"""
        if not self.current_cities:
            print("\n请先进行搜索！")
            time.sleep(2)
            return
        
        print("\n正在刷新价格...")
        
        # 清除缓存以获取新价格
        self.engine.cache.clear()
        self.engine.last_update.clear()
        
        # 重新搜索
        itineraries = self.engine.plan_itinerary(self.current_cities, self.current_dates)
        self.current_itineraries = itineraries
        
        # 显示更新后的结果
        refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.display_itineraries(itineraries, refresh_time)
    
    def auto_refresh_mode(self):
        """自动刷新模式"""
        if not self.current_cities:
            print("\n请先进行搜索！")
            time.sleep(2)
            return
        
        print("\n进入自动刷新模式（每10秒刷新一次）")
        print("按 Ctrl+C 退出自动刷新")
        time.sleep(2)
        
        try:
            while True:
                # 清除缓存
                self.engine.cache.clear()
                self.engine.last_update.clear()
                
                # 重新搜索
                itineraries = self.engine.plan_itinerary(self.current_cities, self.current_dates)
                self.current_itineraries = itineraries
                
                # 显示结果
                refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.display_itineraries(itineraries, refresh_time)
                
                print("\n自动刷新中... (Ctrl+C 退出)")
                time.sleep(self.AUTO_REFRESH_INTERVAL_SECONDS)
        
        except KeyboardInterrupt:
            print("\n\n已退出自动刷新模式")
            time.sleep(1)
    
    def main_menu(self):
        """主菜单"""
        while True:
            self.clear_screen()
            self.print_header()
            
            if self.current_cities:
                print(f"当前行程: {' -> '.join(self.current_cities)}")
                print(f"方案数量: {len(self.current_itineraries)}")
                print()
            
            print("1. 新建搜索")
            print("2. 刷新价格")
            print("3. 自动刷新（每10秒）")
            print("4. 查看当前结果")
            print("5. 退出")
            print()
            
            choice = input("请选择操作 (1-5): ").strip()
            
            if choice == '1':
                self.search_menu()
                input("\n按回车键继续...")
            
            elif choice == '2':
                self.refresh_prices()
                input("\n按回车键继续...")
            
            elif choice == '3':
                self.auto_refresh_mode()
            
            elif choice == '4':
                if self.current_itineraries:
                    refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.display_itineraries(self.current_itineraries, refresh_time)
                    input("\n按回车键继续...")
                else:
                    print("\n尚未进行搜索！")
                    time.sleep(2)
            
            elif choice == '5':
                print("\n感谢使用！再见！")
                time.sleep(1)
                break
            
            else:
                print("\n无效的选择，请重试！")
                time.sleep(1)
    
    def run(self):
        """运行应用"""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\n程序已终止")
            sys.exit(0)
        except Exception as e:
            print(f"\n发生错误: {e}")
            input("按回车键退出...")


def main():
    """主函数"""
    # 设置控制台编码为UTF-8（Windows系统）
    if sys.platform.startswith('win'):
        os.system('chcp 65001 > nul')
    
    app = FlightPriceApp()
    app.run()


if __name__ == "__main__":
    main()

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
                 arrival: str, dep_time: str, arr_time: str, price: float):
        self.flight_no = flight_no
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.dep_time = dep_time
        self.arr_time = arr_time
        self.price = price
    
    def __repr__(self):
        return (f"航班{self.flight_no} | {self.airline} | "
                f"{self.departure}->{self.arrival} | "
                f"{self.dep_time}-{self.arr_time} | ¥{self.price:.2f}")


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
        cache_key = f"{departure}-{arrival}-{date}"
        
        # 检查缓存
        current_time = time.time()
        if (cache_key in self.cache and 
            current_time - self.last_update.get(cache_key, 0) < self.CACHE_TIMEOUT_SECONDS):
            return self.cache[cache_key]
        
        # 模拟API查询延迟（实际API调用时可以移除此行）
        time.sleep(random.uniform(0.1, 0.3))
        
        # 生成模拟航班数据
        flights = self._generate_mock_flights(departure, arrival)
        
        # 更新缓存
        self.cache[cache_key] = flights
        self.last_update[cache_key] = current_time
        
        return flights
    
    def _generate_mock_flights(self, departure: str, arrival: str) -> List[Flight]:
        """生成模拟航班数据"""
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
                          dep_time, arr_time, price)
            flights.append(flight)
        
        return flights
    
    def plan_itinerary(self, cities: List[str]) -> List[Itinerary]:
        """
        规划多城市行程
        
        Args:
            cities: 城市列表，按顺序包含出发地、途径地、目的地
        
        Returns:
            可行的行程方案列表
        """
        if len(cities) < 2:
            return []
        
        # 获取每段航班
        all_segments = []
        for i in range(len(cities) - 1):
            print(f"正在搜索 {cities[i]} -> {cities[i+1]} 的航班...")
            flights = self.search_flights(cities[i], cities[i+1])
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
    
    def get_cities_input(self) -> List[str]:
        """获取城市输入"""
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
            return []
        
        return cities
    
    def display_itineraries(self, itineraries: List[Itinerary], 
                           refresh_time: str = None):
        """显示行程方案"""
        self.clear_screen()
        self.print_header()
        
        if refresh_time:
            print(f"最后更新时间: {refresh_time}")
        print(f"行程路线: {' -> '.join(self.current_cities)}")
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
        cities = self.get_cities_input()
        
        if not cities:
            return
        
        self.current_cities = cities
        
        # 显示加载动画
        self.clear_screen()
        self.print_header()
        print("正在搜索航班信息，请稍候...")
        print()
        
        # 搜索航班
        itineraries = self.engine.plan_itinerary(cities)
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
        itineraries = self.engine.plan_itinerary(self.current_cities)
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
                itineraries = self.engine.plan_itinerary(self.current_cities)
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

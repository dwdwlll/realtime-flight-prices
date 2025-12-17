# 网页爬虫集成指南 / Web Scraping Integration Guide

本文档说明如何使用网页爬虫技术获取真实航班数据，模拟网页搜索。

This document explains how to use web scraping to fetch real flight data by simulating web searches.

## 概述 / Overview

网页爬虫通过模拟浏览器访问航空公司或旅游网站，解析HTML页面获取航班信息。

Web scraping simulates browser visits to airline or travel websites and parses HTML pages to extract flight information.

### 优点 / Advantages
✅ 无需API密钥和付费
✅ 可以访问公开的网站数据
✅ 灵活性高，可以自定义爬取逻辑

### 缺点 / Disadvantages
⚠️ 可能违反网站服务条款（需要遵守robots.txt）
⚠️ 网站结构变化会导致爬虫失效
⚠️ 需要处理反爬虫机制（验证码、IP封禁等）
⚠️ 爬取速度较慢，可能被限流
⚠️ 动态内容需要JavaScript渲染

## 技术方案 / Technical Solutions

### 方案1：requests + BeautifulSoup（静态页面）

适用于页面结构简单、无需JavaScript渲染的网站。

#### 安装依赖 / Install Dependencies

```bash
pip install requests beautifulsoup4 lxml
```

#### 代码示例 / Code Example

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_flights_static(departure, arrival, date=None):
    """使用requests + BeautifulSoup爬取航班信息"""
    
    # 城市名称到代码的映射
    city_codes = {
        "北京": "beijing", "上海": "shanghai", "广州": "guangzhou",
        "深圳": "shenzhen", "成都": "chengdu", "杭州": "hangzhou"
    }
    
    dep_code = city_codes.get(departure, "beijing")
    arr_code = city_codes.get(arrival, "shanghai")
    search_date = date or datetime.now().strftime("%Y-%m-%d")
    
    # 构建URL（示例格式）
    url = f"https://example-flight-site.com/flights?from={dep_code}&to={arr_code}&date={search_date}"
    
    # 设置请求头，模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://example-flight-site.com/'
    }
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 提取航班信息（需要根据实际网页结构调整）
        flights = []
        flight_items = soup.select('.flight-card')  # CSS选择器
        
        for item in flight_items:
            try:
                # 提取字段（示例）
                flight_no = item.select_one('.flight-number').text.strip()
                airline = item.select_one('.airline-name').text.strip()
                dep_time = item.select_one('.departure-time').text.strip()
                arr_time = item.select_one('.arrival-time').text.strip()
                price_text = item.select_one('.price-value').text.strip()
                
                # 清洗价格数据
                price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                
                flights.append({
                    'flight_no': flight_no,
                    'airline': airline,
                    'departure': departure,
                    'arrival': arrival,
                    'dep_time': dep_time,
                    'arr_time': arr_time,
                    'price': price,
                    'date': date
                })
            except Exception as e:
                print(f"解析航班项失败: {e}")
                continue
        
        return flights
    
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []
```

### 方案2：Selenium（动态页面）

适用于需要JavaScript渲染的网站（如携程、飞猪、去哪儿）。

#### 安装依赖 / Install Dependencies

```bash
pip install selenium webdriver-manager
```

#### 代码示例 / Code Example

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_flights_selenium(departure, arrival, date=None):
    """使用Selenium爬取动态加载的航班信息"""
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式（不显示浏览器窗口）
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # 设置User-Agent
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # 禁用自动化标识
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # 初始化WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 修改navigator.webdriver属性
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })
        
        # 构建搜索URL
        search_date = date or datetime.now().strftime("%Y-%m-%d")
        url = f"https://flights.ctrip.com/online/list/oneway-{departure}-{arrival}?depdate={search_date}"
        
        # 访问页面
        driver.get(url)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 15)
        
        # 等待航班列表加载
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'flight-list')))
        
        # 额外等待，确保数据完全加载
        time.sleep(3)
        
        # 提取航班信息
        flights = []
        flight_elements = driver.find_elements(By.CSS_SELECTOR, '.flight-item, .flight-card')
        
        for elem in flight_elements[:15]:  # 限制数量
            try:
                # 根据实际网页结构调整选择器
                flight_no = elem.find_element(By.CSS_SELECTOR, '.flight-number, .flight-code').text.strip()
                airline = elem.find_element(By.CSS_SELECTOR, '.airline-name, .carrier-name').text.strip()
                dep_time = elem.find_element(By.CSS_SELECTOR, '.dep-time, .departure-time').text.strip()
                arr_time = elem.find_element(By.CSS_SELECTOR, '.arr-time, .arrival-time').text.strip()
                price_text = elem.find_element(By.CSS_SELECTOR, '.price, .price-value').text.strip()
                
                # 清洗价格
                price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                
                flights.append({
                    'flight_no': flight_no,
                    'airline': airline,
                    'departure': departure,
                    'arrival': arrival,
                    'dep_time': dep_time,
                    'arr_time': arr_time,
                    'price': price,
                    'date': date
                })
            except Exception as e:
                print(f"解析航班元素失败: {e}")
                continue
        
        return flights
    
    except Exception as e:
        print(f"Selenium爬取失败: {e}")
        return []
    
    finally:
        try:
            driver.quit()
        except:
            pass
```

## 目标网站分析 / Target Website Analysis

### 1. 携程 (Ctrip.com)

**特点：**
- 需要JavaScript渲染
- 使用Selenium
- 可能有反爬虫机制

**URL格式：**
```
https://flights.ctrip.com/online/list/oneway-北京-上海?depdate=2025-01-15
```

**关键选择器（可能变化）：**
```python
flight_items = driver.find_elements(By.CLASS_NAME, 'flight-item')
flight_no = elem.find_element(By.CLASS_NAME, 'flight-number')
airline = elem.find_element(By.CLASS_NAME, 'airline-name')
price = elem.find_element(By.CLASS_NAME, 'price-cell')
```

### 2. 去哪儿 (Qunar.com)

**特点：**
- 部分内容可能是静态的
- 可以尝试requests + BeautifulSoup
- 也支持Selenium

**URL格式：**
```
https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=北京&searchArrivalAirport=上海&searchDepartureTime=2025-01-15
```

### 3. 飞猪 (Fliggy.com)

**特点：**
- 阿里旗下，反爬虫较强
- 必须使用Selenium
- 可能需要登录

**URL格式：**
```
https://www.fliggy.com/flight/search/oneway-北京-上海-2025-01-15
```

## 反爬虫应对策略 / Anti-Scraping Strategies

### 1. 设置合适的请求头

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.example.com/',
    'Cache-Control': 'max-age=0'
}
```

### 2. 使用代理IP

```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}
response = requests.get(url, headers=headers, proxies=proxies)
```

### 3. 添加随机延迟

```python
import time
import random

time.sleep(random.uniform(1, 3))  # 随机延迟1-3秒
```

### 4. 处理验证码

- 使用OCR识别（pytesseract）
- 使用验证码识别服务
- 使用Selenium模拟人工点击

### 5. 隐藏自动化特征（Selenium）

```python
# 禁用webdriver属性
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

# 使用stealth插件
from selenium_stealth import stealth
stealth(driver,
    languages=["zh-CN", "zh"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)
```

## 集成到项目中 / Integration into Project

### 步骤1：选择爬取方案

根据目标网站特点选择：
- 静态页面 → requests + BeautifulSoup
- 动态页面 → Selenium

### 步骤2：安装依赖

```bash
# 方案1
pip install requests beautifulsoup4 lxml

# 方案2  
pip install selenium webdriver-manager

# 可选：反爬虫增强
pip install selenium-stealth fake-useragent
```

### 步骤3：在Main.py中启用

找到 `_fetch_flights_by_web_scraping` 方法，取消注释相应代码。

在 `search_flights` 方法中切换：

```python
# 注释掉模拟数据
# flights = self._generate_mock_flights(departure, arrival, date)

# 启用网页爬虫
flights = self._fetch_flights_by_web_scraping(departure, arrival, date)
```

### 步骤4：调整选择器

根据目标网站的实际HTML结构，调整CSS选择器：

```python
# 示例：需要根据实际网页调整
flight_items = soup.select('.flight-card')  # 或 driver.find_elements(By.CLASS_NAME, 'flight-item')
flight_no = item.select_one('.flight-number')
airline = item.select_one('.airline-name')
```

**如何找到正确的选择器：**
1. 在浏览器中打开目标网站
2. 按F12打开开发者工具
3. 点击"Elements"标签
4. 使用选择器工具（Ctrl+Shift+C）点击航班信息
5. 查看HTML结构，找到合适的class或id

## 注意事项 / Important Notes

### 法律和道德

⚠️ **遵守法律法规**：
- 遵守网站的robots.txt规则
- 遵守网站服务条款
- 不要过度爬取造成服务器负担
- 仅用于个人学习和研究

### 技术限制

⚠️ **常见问题**：
1. **网页结构变化**：网站更新后选择器可能失效
2. **动态加载**：需要等待JavaScript执行完成
3. **反爬虫**：可能遇到IP封禁、验证码
4. **数据不准确**：爬取的数据可能不完整或有延迟

### 维护成本

⚠️ **需要定期维护**：
- 更新选择器以适应网页变化
- 更新反爬虫策略
- 处理各种异常情况

## 推荐做法 / Best Practices

1. **礼貌爬取**：
   - 控制爬取频率（每次请求间隔1-3秒）
   - 使用合理的User-Agent
   - 遵守robots.txt

2. **错误处理**：
   - 使用try-except捕获异常
   - 失败时回退到模拟数据
   - 记录错误日志

3. **数据验证**：
   - 检查爬取数据的完整性
   - 过滤无效数据
   - 验证价格范围合理性

4. **缓存机制**：
   - 缓存已爬取的数据
   - 避免重复请求
   - 设置合理的缓存过期时间

## 示例：完整的爬虫实现

参考项目中的 `_fetch_flights_by_web_scraping` 方法，其中包含：
- requests + BeautifulSoup方案的示例代码
- Selenium方案的示例代码
- 错误处理和回退机制

## 故障排查 / Troubleshooting

### 问题1：找不到元素

**解决方案：**
- 检查选择器是否正确
- 确认页面已完全加载
- 使用XPath代替CSS选择器
- 增加等待时间

### 问题2：被反爬虫拦截

**解决方案：**
- 降低爬取频率
- 使用代理IP
- 更换User-Agent
- 使用selenium-stealth

### 问题3：数据解析错误

**解决方案：**
- 打印原始HTML查看结构
- 使用更宽松的try-except
- 添加数据清洗逻辑
- 验证选择器匹配的元素数量

## 相关资源 / Related Resources

- [Selenium官方文档](https://www.selenium.dev/documentation/)
- [BeautifulSoup文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests文档](https://docs.python-requests.org/)
- [CSS选择器参考](https://www.w3schools.com/cssref/css_selectors.asp)
- [XPath教程](https://www.w3schools.com/xml/xpath_intro.asp)

## 技术支持 / Support

如需帮助实现特定网站的爬虫，请提供：
1. 目标网站URL
2. 需要爬取的信息类型
3. 遇到的具体错误信息
4. 网页HTML结构截图

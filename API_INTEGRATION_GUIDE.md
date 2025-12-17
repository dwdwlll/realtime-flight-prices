# API集成指南 / API Integration Guide

本文档说明如何将模拟数据替换为真实的航班API数据。

This document explains how to replace mock data with real flight API data.

## 可用的航班API / Available Flight APIs

### 国际API / International APIs

#### 1. Amadeus Flight API (推荐 / Recommended)
- **网站**: https://developers.amadeus.com/
- **特点**: 
  - 免费测试API（每月有限额度）
  - 完整的航班搜索、预订功能
  - 支持多种编程语言
- **申请流程**:
  1. 注册账号
  2. 创建应用获取 API Key 和 API Secret
  3. 阅读API文档: https://developers.amadeus.com/self-service/category/flights

#### 2. Skyscanner API
- **网站**: https://partners.skyscanner.net/
- **特点**: 
  - 需要商业合作
  - 提供快速价格比较
- **申请流程**: 需要联系Skyscanner商务团队

#### 3. Travelport Universal API
- **网站**: https://developers.travelport.com/
- **特点**: 企业级API，功能全面
- **申请流程**: 需要企业合作

### 国内API / Chinese APIs

#### 1. 携程API (Ctrip/Trip.com)
- **申请方式**: 需联系携程开放平台进行商务合作
- **网站**: https://www.trip.com (商务合作)

#### 2. 去哪儿API (Qunar)
- **申请方式**: 需联系去哪儿进行商务合作
- **网站**: https://www.qunar.com (商务合作)

#### 3. 飞猪API (Fliggy)
- **申请方式**: 需通过阿里云市场申请
- **网站**: https://market.aliyun.com

## 集成步骤 / Integration Steps

### 步骤1: 获取API凭证 / Step 1: Get API Credentials

以Amadeus为例：
1. 访问 https://developers.amadeus.com/
2. 注册并登录
3. 创建应用，获取：
   - API Key (Client ID)
   - API Secret (Client Secret)

### 步骤2: 安装依赖 / Step 2: Install Dependencies

```bash
pip install requests
```

更新 `requirements.txt`:
```txt
requests>=2.28.0
```

### 步骤3: 配置环境变量 / Step 3: Configure Environment Variables

#### Linux/Mac:
```bash
export FLIGHT_API_KEY="your_api_key_here"
export FLIGHT_API_SECRET="your_api_secret_here"
```

#### Windows:
```cmd
set FLIGHT_API_KEY=your_api_key_here
set FLIGHT_API_SECRET=your_api_secret_here
```

#### 或使用 .env 文件 / Or use .env file:
创建 `.env` 文件：
```
FLIGHT_API_KEY=your_api_key_here
FLIGHT_API_SECRET=your_api_secret_here
```

安装 python-dotenv:
```bash
pip install python-dotenv
```

在 `Main.py` 顶部添加:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 步骤4: 启用API集成 / Step 4: Enable API Integration

在 `Main.py` 的 `FlightSearchEngine` 类中：

1. 找到 `_fetch_real_flights_from_api` 方法
2. 取消注释示例代码
3. 根据您选择的API文档调整代码

4. 在 `search_flights` 方法中，将：
```python
flights = self._generate_mock_flights(departure, arrival, date)
```

改为：
```python
flights = self._fetch_real_flights_from_api(departure, arrival, date)
```

## Amadeus API 集成示例 / Amadeus API Integration Example

### 完整代码示例:

```python
import os
import requests
from datetime import datetime
from typing import List

def _fetch_real_flights_from_api(self, departure: str, arrival: str, date: str = None) -> List[Flight]:
    """从Amadeus API获取真实航班数据"""
    
    # 1. 获取访问令牌 (Access Token)
    api_key = os.environ.get('FLIGHT_API_KEY', '')
    api_secret = os.environ.get('FLIGHT_API_SECRET', '')
    
    if not api_key or not api_secret:
        print("警告：未配置API密钥，使用模拟数据")
        return self._generate_mock_flights(departure, arrival, date)
    
    # 获取Token
    token_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": api_secret
    }
    
    try:
        token_response = requests.post(token_url, data=token_data, timeout=10)
        token_response.raise_for_status()
        access_token = token_response.json()['access_token']
        
        # 2. 搜索航班
        search_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # 城市代码映射 (需要根据实际情况扩展)
        city_codes = {
            "北京": "PEK",
            "上海": "PVG",  # 浦东国际机场，也可用SHA(虹桥)
            "广州": "CAN",
            "深圳": "SZX",
            "成都": "CTU",
            "杭州": "HGH"
        }
        
        origin_code = city_codes.get(departure, "PEK")
        dest_code = city_codes.get(arrival, "SHA")
        flight_date = date or datetime.now().strftime("%Y-%m-%d")
        
        params = {
            "originLocationCode": origin_code,
            "destinationLocationCode": dest_code,
            "departureDate": flight_date,
            "adults": 1,
            "max": 10,
            "currencyCode": "CNY"
        }
        
        search_response = requests.get(search_url, headers=headers, params=params, timeout=10)
        search_response.raise_for_status()
        data = search_response.json()
        
        # 3. 解析响应数据
        flights = []
        for offer in data.get('data', []):
            for itinerary in offer.get('itineraries', []):
                for segment in itinerary.get('segments', []):
                    # 提取航班信息
                    carrier_code = segment.get('carrierCode', '')
                    flight_number = segment.get('number', '')
                    flight_no = f"{carrier_code}{flight_number}"
                    
                    airline = segment.get('operating', {}).get('carrierCode', carrier_code)
                    
                    dep_time_str = segment.get('departure', {}).get('at', '')
                    arr_time_str = segment.get('arrival', {}).get('at', '')
                    
                    # 解析时间 (格式: 2025-01-15T08:30:00)
                    dep_time = dep_time_str.split('T')[1][:5] if 'T' in dep_time_str else "00:00"
                    arr_time = arr_time_str.split('T')[1][:5] if 'T' in arr_time_str else "00:00"
                    
                    # 价格
                    price = float(offer.get('price', {}).get('total', 0))
                    
                    flight = Flight(flight_no, airline, departure, arrival,
                                  dep_time, arr_time, price, flight_date)
                    flights.append(flight)
        
        return flights if flights else self._generate_mock_flights(departure, arrival, date)
        
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}")
        return self._generate_mock_flights(departure, arrival, date)
    except Exception as e:
        print(f"数据解析失败: {e}")
        return self._generate_mock_flights(departure, arrival, date)
```

## 城市代码映射 / City Code Mapping

主要城市的IATA代码：

| 城市 | IATA代码 |
|------|---------|
| 北京 | PEK |
| 上海浦东 | PVG |
| 上海虹桥 | SHA |
| 广州 | CAN |
| 深圳 | SZX |
| 成都 | CTU |
| 杭州 | HGH |
| 西安 | XIY |
| 重庆 | CKG |
| 武汉 | WUH |
| 南京 | NKG |
| 天津 | TSN |

完整列表: https://www.iata.org/en/publications/directories/code-search/

## 测试API集成 / Testing API Integration

### 测试命令:
```bash
# 设置测试环境变量
export FLIGHT_API_KEY="your_test_key"
export FLIGHT_API_SECRET="your_test_secret"

# 运行程序
python Main.py
```

### 检查清单:
- [ ] API密钥配置正确
- [ ] 网络连接正常
- [ ] 城市代码映射完整
- [ ] 错误处理正常（API失败时回退到模拟数据）
- [ ] 日期格式正确 (YYYY-MM-DD)

## 注意事项 / Important Notes

1. **API配额**: 大多数免费API有请求次数限制，建议使用缓存机制
2. **错误处理**: 实现完善的错误处理，API失败时回退到模拟数据
3. **响应时间**: API调用可能较慢，考虑添加超时和重试机制
4. **数据格式**: 不同API返回格式不同，需要适配解析逻辑
5. **成本控制**: 商业API通常按请求次数计费，注意成本控制

## 故障排查 / Troubleshooting

### 问题1: API认证失败
- 检查API Key和Secret是否正确
- 确认API密钥未过期
- 检查是否在正确的环境（测试/生产）

### 问题2: 请求超时
- 增加超时时间设置
- 检查网络连接
- 考虑使用CDN或代理

### 问题3: 无法解析城市代码
- 扩展城市代码映射表
- 添加城市名称到IATA代码的转换逻辑

## 技术支持 / Support

如需帮助集成特定API，请提供：
1. API服务名称和文档链接
2. 已获取的API凭证类型
3. 具体的错误信息

## 相关资源 / Related Resources

- [Amadeus API文档](https://developers.amadeus.com/self-service)
- [IATA城市代码查询](https://www.iata.org/en/publications/directories/code-search/)
- [Python Requests文档](https://requests.readthedocs.io/)

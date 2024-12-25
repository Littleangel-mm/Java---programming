


import requests

# API接口URL
url = "https://eolink.o.apispace.com/teladress/teladress"

# 获取用户输入的手机号
mobile_number = input("请输入手机号进行查询：")

# 请求参数
payload = {"mobile": mobile_number}

# 请求头，包含API令牌和Content-Type
headers = {
    "X-APISpace-Token": "b3xkia89gq04tvlztudo8eyvjp7itmb3",  # 替换为你自己的API Token
    "Content-Type": "application/x-www-form-urlencoded"
}

# 设定保存文件路径
output_file = "电话号码归属地.txt"

try:
    # 发送POST请求
    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()  # 如果状态码不是200，将引发异常

    # 打印响应内容，调试用
    print(f"\n响应内容: {response.text}")
    
    # 尝试解析响应内容为JSON
    try:
        data = response.json()

        # 打印返回的数据结构，帮助调试
        print(f"解析后的数据: {data}")

        # 检查返回的JSON数据，判断是否成功
        if data.get('code') == '200000' and 'data' in data:
            info = data['data']
            
            # 只提取需要的信息
            province = info.get('province', '未查询到')
            city = info.get('city', '未查询到')
            isp = info.get('isp', '未查询到')
            
            # 生成输出内容
            output_text = f"""
手机号: {mobile_number}
省份: {province}
城市: {city}
运营商: {isp}
"""
            
            # 写入文本文件
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(output_text)
            
            print(f"\n查询结果已保存到 {output_file}")
        
        else:
            print("\n查询失败，API返回状态不是200000或没有数据。")
    
    except ValueError as e:
        print(f"\n解析JSON时出错: {e}")
        print(f"原始响应内容: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"\n请求失败: {e}")





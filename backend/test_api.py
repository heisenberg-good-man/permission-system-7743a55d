import urllib.request
import json

try:
    response = urllib.request.urlopen("http://localhost:8000/api/stats")
    data = json.loads(response.read().decode())
    print("API测试成功!")
    print("统计数据:", data)
except Exception as e:
    print(f"API测试失败: {e}")
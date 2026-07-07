import urllib.request
import urllib.parse
import json

print("=== 测试 Offer API ===")

print("\n1. 获取 Offer 详情 (招聘方视角):")
try:
    response = urllib.request.urlopen("http://localhost:8000/api/offers/offer-001/details?role=company")
    data = json.loads(response.read().decode())
    print(f"状态: {data['offer']['status']}")
    print(f"可用操作: {data['available_actions']}")
    print("✓ 成功")
except Exception as e:
    print(f"✗ 失败: {e}")

print("\n2. 获取 Offer 详情 (候选人视角):")
try:
    response = urllib.request.urlopen("http://localhost:8000/api/offers/offer-001/details?role=candidate")
    data = json.loads(response.read().decode())
    print(f"状态: {data['offer']['status']}")
    print(f"可用操作: {data['available_actions']}")
    print("✓ 成功")
except Exception as e:
    print(f"✗ 失败: {e}")

print("\n3. 创建 Offer 消息:")
try:
    url = "http://localhost:8000/api/offer-messages"
    data = {
        "offer_id": "offer-001",
        "sender_id": "company",
        "sender_type": "company",
        "content": "测试消息",
        "message_type": "text"
    }
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="POST")
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print(f"创建的消息ID: {result['id']}")
    print("✓ 成功")
except Exception as e:
    print(f"✗ 失败: {e}")

print("\n4. 更新 Offer 状态为 pending (发出):")
try:
    url = "http://localhost:8000/api/offers/offer-001/status"
    data = {"status": "pending"}
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method="PUT")
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print(f"新状态: {result['status']}")
    print("✓ 成功")
except Exception as e:
    print(f"✗ 失败: {e}")

print("\n5. 获取更新后的 Offer 详情 (候选人视角):")
try:
    response = urllib.request.urlopen("http://localhost:8000/api/offers/offer-001/details?role=candidate")
    data = json.loads(response.read().decode())
    print(f"状态: {data['offer']['status']}")
    print(f"可用操作: {data['available_actions']}")
    print("✓ 成功")
except Exception as e:
    print(f"✗ 失败: {e}")

print("\n=== 测试完成 ===")

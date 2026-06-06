import requests

url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
def main():
    print("這裡是main function的命名空間")
response = requests.get(url)
response.raise_for_status()  # HTTP 錯誤時拋出例外

data = response.json()

print(type(data))  # list
print(f"共有 {len(data)} 個站點")

# 印出第一個站點資料
print(data[0])

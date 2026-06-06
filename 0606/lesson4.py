import requests
import json

# YouBike 2.0 即時資料的 URL
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

try:
    # 向 API 發送 GET 請求取得資料
    response = requests.get(url)
    # 若回應狀態不是 200 系列，會拋出 HTTPError
    response.raise_for_status()

    # 解析回傳的 JSON 資料（通常是一個 list）
    bike_data = response.json()

    # 印出站點總數（list 長度）
    print(f"共有 {len(bike_data)} 個站點")
    # 顯示第一個站點的範例資料，使用 json.dumps 美化輸出並保留中文
    print("\n範例站點資料:")
    print(json.dumps(bike_data[0], indent=4, ensure_ascii=False))

except requests.exceptions.RequestException as e:
    # 處理網路或 HTTP 錯誤，並印出錯誤訊息
    print(f"擷取資料時發生錯誤: {e}")
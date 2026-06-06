import requests
from requests import Response

def main():
    # YouBike 2.0 即時資料的 JSON 檔案 URL
    
    url:str= "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    response:Response= requests.get(url)

    # 向 API 發出 GET 請求


    # 若 HTTP 回應狀態不是成功（2xx），則拋出例外
    response.raise_for_status()

    # 將回應內容解析為 JSON（此 API 回傳的是一個 list）
    data = response.json()

    # 印出站點總數
    print(f"共有 {len(data)} 個站點")

    # 若有資料則印出第一個站點的完整內容（方便檢查欄位）
    if data:
        print(data[0])


if __name__ == "__main__":
    # 當此模組被當作主程式執行時，才呼叫 main()
    main()

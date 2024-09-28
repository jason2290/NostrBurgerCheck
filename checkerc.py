import requests
import csv

# 定义请求的 URL
url = "https://market-api.lnfi.network/airdrop/check"

# 定义请求头
headers = {
    "Content-Type": "application/json"  # 根据实际需求可以调整
}

# 打开输出文件用于写入结果
with open('output.csv', mode='w', newline='') as output_file:
    fieldnames = ['amount', 'address', 'airdropId', 'msg']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    # 从 address.csv 文件中读取每一行地址
    with open('address.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            address = row[0]  # 读取地址

            # 定义请求的 payload
            payload = {
                "airdropId": "02ERC20",  # 你可以修改为需要的 airdropId
                "address": address
            }

            # 发送 POST 请求
            response = requests.post(url, json=payload, headers=headers)

            # 解析响应
            if response.status_code == 200:
                response_data = response.json()

                # 提取需要的字段
                data = response_data.get('data', {})
                amount = data.get('amount', 0) or 0  # 如果 amount 为空则填 0
                airdrop_id = data.get('airdropId', '') or payload['airdropId']  # 如果 airdropId 为空则填 payload 中的值
                msg = response_data.get('msg', '')

                # 将提取的数据写入 CSV 文件
                writer.writerow({
                    'amount': amount,
                    'address': address,
                    'airdropId': airdrop_id,
                    'msg': msg
                })

                print(f"Processed address: {address}, Status Code: {response.status_code}")
            else:
                print(f"Failed to process address: {address}, Status Code: {response.status_code}")

print("Processing completed. Results saved to output.csv.")

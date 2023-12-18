import asyncio
import aiohttp
import json
import os

async def fetch_data_api(url, output_file):
    async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    res = await response.json()
                    
                    with open(output_file, 'w') as fileContent:
                        json.dump(res, fileContent)

                    print(f"Save Json File {output_file}")
                else:
                    print("Failed")

async def upload_todo_json_data(url, input_file):
    while not os.path.exists(input_file):
        await asyncio.sleep(1)

    with open(input_file, 'r') as file:
        data = json.load(file)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                print("Json Data Uploaded")
            else:
                print("Failed")

async def main():
    url_endpoint = "https://lingopal.free.beeceptor.com/todos"

    json_output_filename = "todos-data.json"

    task_get_data = asyncio.create_task(fetch_data_api(url_endpoint, json_output_filename))
    
    task_upload_data = asyncio.create_task(upload_todo_json_data(url_endpoint, json_output_filename))

    await asyncio.gather(task_get_data, task_upload_data)




if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    

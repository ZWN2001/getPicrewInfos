import asyncio

import requests
import re
import os
import js2py
import aiohttp
import aiofiles

global virtal_id, key, url, task


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


async def download(url: str, dest_folder: str):
    mkdir(dest_folder)

    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    if os.path.exists(file_path):
        print("already saved", file_path)
        return

    async with aiohttp.ClientSession() as session:  # requests
        async with session.get(url) as r:  # resp = requests.get()
            if r.ok:
                print("saving to", os.path.abspath(file_path))
                async with aiofiles.open(file_path, mode="wb") as f:
                    await f.write(await r.content.read())
                    await f.flush()
                    os.fsync(f.fileno())

            else:
                print("Download failed: status code {}\n{}".format(r.status, r.text))


def get_release_key(pagedata):
    key_pattern = re.compile("release_key:\"([A-Za-z0-9]+)\"")
    release_key = key_pattern.findall(pagedata)[0]
    return release_key


def is_public_picrew(id):
    return not any(c.isalpha() for c in str(id))


async def main():
    global virtal_id, key, url, task
    task = []
    url = []
    id = 41
    virtal_id = id
    key = ""
    main_thumbnail_url = ""
    if is_public_picrew(id):
        main_page = requests.get("https://picrew.me/image_maker/" + str(id)).text
        key = get_release_key(main_page)
    else:
        main_page = requests.get("https://picrew.me/secret_image_maker/" + str(id)).text
        key = get_release_key(main_page)
        vid_pattern = re.compile("/app/image_maker/(.*)/icon.*.(png|jpg)")
        virtual_id = vid_pattern.findall(main_thumbnail_url)[0][0]
        print(virtual_id)

    # ======NO TOCAR======
    main_page = requests.get("https://picrew.me/image_maker/1272810").text
    nuxt_pattern = re.compile("<script>.+(__NUXT__.*\);)<\/script>")
    nuxt_data = nuxt_pattern.findall(main_page)[0]
    parsed_nuxt_data = js2py.eval_js("function getData(){ " + nuxt_data + "\n return __NUXT__}\n")

    img = {"baseUrl": "https:\/\/cdn.picrew.me", "lst": parsed_nuxt_data().to_dict()['state']['commonImages']}
    cf = parsed_nuxt_data().to_dict()['state']['config']

    base_url = "https://picrew.me"
    part_list = cf['pList']

    thumbnail_url = parsed_nuxt_data().to_dict()['state']['imageMakerInfo']['icon_url']

    print("DL: [" + thumbnail_url + "] -> [" + str(id) + "]")

    try:
        part_ctr = 0
        for p in part_list:
            part_ctr = part_ctr + 1
            path = str(id) + "/" + str(part_ctr).zfill(4) + '-' + str(p['pId']) + '-' + p['pNm']
            if p['thumbUrl']:  # Pass if thumbnail is null
                print(p['pId'], p['pNm'], base_url + p['thumbUrl'])
                mkdir(path)
                task.append(download(base_url + p['thumbUrl'], dest_folder=path))
                print("DL: [" + base_url + p['thumbUrl'] + "] -> [" + path + "]")

            item_ctr = 0
            for item in p['items']:
                item_ctr = item_ctr + 1
                item_path = path + "/" + str(item_ctr).zfill(4) + '-' + str(item['itmId'])
                if item['thumbUrl']:  # Pass if thumbnail is null
                    item_path = path + "/" + str(item_ctr).zfill(4) + '-' + str(item['itmId'])
                    task.append(download(base_url + item['thumbUrl'], dest_folder=item_path))
                    print("DL: [" + base_url + item['thumbUrl'] +
                          "] -> [" + item_path + "]")
                    print("-", item['itmId'], base_url + item['thumbUrl'])

                try:
                    item_dict = img['lst'][str(item['itmId'])]
                    for k1 in item_dict.keys():
                        for k2 in item_dict[k1].keys():
                            url = base_url + item_dict[k1][k2]['url']
                            task.append(download(url, dest_folder=item_path))
                            print("DL: [" + url + "] -> [" + item_path + "]")
                except:
                    print("parse error:", str(item['itmId']))

    except:
        import traceback
        traceback.print_exc()

    await asyncio.wait(task)


if __name__ == '__main__':
    asyncio.run(main())

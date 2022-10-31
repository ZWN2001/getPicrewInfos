import requests
import re
import os
import js2py


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def download(url: str, dest_folder: str):
    mkdir(dest_folder)

    filename = url.split('/')[-1].replace(" ", "_")
    file_path = os.path.join(dest_folder, filename)

    if os.path.exists(file_path):
        print("already saved", file_path)
        return

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))

#
# def get_release_key(pagedata):
#     key_pattern = re.compile("release_key:\"([A-Za-z0-9]+)\"")
#     release_key = key_pattern.findall(pagedata)[0]
#     return release_key


def is_public_picrew(id):
    return not any(c.isalpha() for c in str(id))


id = 41
virtal_id = id
key = ""
# main_thumbnail_url = ""
# if is_public_picrew(id):
#     main_page = requests.get("https://picrew.me/image_maker/" + str(id)).text
#     key = get_release_key(main_page)
# else:
#     main_page = requests.get("https://picrew.me/secret_image_maker/" + str(id)).text
#     key = get_release_key(main_page)
#     vid_pattern = re.compile("/app/image_maker/(.*)/icon.*.(png|jpg)")
#     virtual_id = vid_pattern.findall(main_thumbnail_url)[0][0]
#     print(virtual_id)

main_page = requests.get("https://picrew.me/image_maker/"+str(id)).text
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
            download(base_url + p['thumbUrl'], dest_folder=path)
            # icon图
            print("DL1: [" + base_url + p['thumbUrl'] + "] -> [" + path + "]")

        item_ctr = 0
        for item in p['items']:
            item_ctr = item_ctr + 1
            item_path = path + "/" + str(item_ctr).zfill(4) + '-' + str(item['itmId'])
            if item['thumbUrl']:  # Pass if thumbnail is null
                item_path = path + "/" + str(item_ctr).zfill(4) + '-' + str(item['itmId'])
                download(base_url + item['thumbUrl'], dest_folder=item_path)
                # 预览图
                print("DL2: [" + base_url + item['thumbUrl'] +
                      "] -> [" + item_path + "]")
                print("-", item['itmId'], base_url + item['thumbUrl'])

            try:
                item_dict = img['lst'][str(item['itmId'])]
                for k1 in item_dict.keys():
                    for k2 in item_dict[k1].keys():
                        url = base_url + item_dict[k1][k2]['url']
                        download(url, dest_folder=item_path)
                        print("DL3: [" + url + "] -> [" + item_path + "]")
            except:
                print("parse error:", str(item['itmId']))

except:
    import traceback
    traceback.print_exc()

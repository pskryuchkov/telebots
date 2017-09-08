import urllib2
import cv2
import glob, os
from copa import *

api_link = "https://www.instagram.com/{0}/?__a=1"


def links_chunk(max_id=None):
    if max_id is None:
        req = urllib2.Request(her_insta)
    else:
        req = urllib2.Request(her_insta + "&max_id={}".format(max_id))

    response = urllib2.urlopen(req)
    the_page = response.read()

    links = {}
    for field in json.loads(the_page)["user"]["media"]["nodes"]:
        links[field["code"]] = field["display_src"]
        last_id = field["id"]

    return links, last_id


def photos_links(min_photos=20):
    links = {}
    last_id = None
    n_chunk = 1

    while len(links.values()) < min_photos:
        try:
            print "Chunk #{}".format(n_chunk)
            chunk, last_id = links_chunk(last_id)
            links.update(chunk)
            n_chunk += 1
        except:
            print "Warning: number of links less than min_photos"
            break

    return links


def load_photos(links):
    print "Loading photos..."
    for j, key in enumerate(links.keys()):
        print "{}/{}".format(j+1, len(links.keys()))
        try:
            f = open('{0}/{1}.jpg'.format(config.pretty_girl, key), 'wb')
            data = urllib2.urlopen(links[key]).read()
            f.write(data)
            f.close()
        except:
            print "Warning: photo '{0}' didn't loaded".format(key)
            continue


def n_faces(photo_path):
    frontal_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    profile_cascade = cv2.CascadeClassifier('cascades/haarcascade_profileface.xml')

    img = cv2.imread(photo_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    frontal_faces = frontal_cascade.detectMultiScale(gray, 1.3, 5)
    profile_faces = profile_cascade.detectMultiScale(gray, 1.3, 5)

    if len(frontal_faces) > len(profile_faces):
        photo_type = "frontal"
    elif len(frontal_faces) < len(profile_faces):
        photo_type = "profile"
    else:
        photo_type = "combined"

    return max(len(frontal_faces), len(profile_faces)), photo_type


def detect_portrait(photos_list, n_persons=1):
    portrait_id = []

    for j, pic in enumerate(["{}/{}.jpg".format(config.pretty_girl, x) for x in photos_list]):
        n, photo_type = n_faces(pic)
        if n == n_persons:
            photo_id = os.path.basename(pic).split(".")[0]
            print("k={0}, id={1}, type='{2}'".format(j, photo_id, photo_type))
            portrait_id.append(photo_id),
    return portrait_id


def save_list(fn, l):
    base = open(fn, "w")
    for item in l:
        base.write("%s\n" % item)


def build_base():
    links = photos_links(config.min_posts)

    if not os.path.exists(config.pretty_girl):
        os.makedirs(config.pretty_girl)

    load_photos(links)

    print("Face detecting...")
    portraits = detect_portrait(links.keys())
    save_list("{}/portraits.txt".format(config.pretty_girl), portraits)
    print "Done!"


def update_base():
    links = photos_links(config.min_posts)
    new_ids = set(links.keys())
    old_ids = set([os.path.basename(x).split(".")[0] for x in glob.glob(config.pretty_girl + "/*.jpg")])

    if not new_ids - old_ids:
        print "No new photos"
        return

    new_links = {}
    for x in new_ids - old_ids:
        new_links[x] = links[x]

    load_photos(new_links)

    print "New photos:"
    for x in new_ids - old_ids:
        print "  id={}".format(x)

    if old_ids - new_ids:
        print "Excluded photos:"

    for x in list(old_ids - new_ids):
        print "  id={}".format(x)
        os.remove("{}/{}.jpg".format(config.pretty_girl, x))

    print("Face detecting...")
    portraits = detect_portrait(new_ids - old_ids)
    save_list("{}/portraits.txt".format(config.pretty_girl), portraits) # FIXME: save old info
    print "Done!"

if __name__ == '__main__':
    config = get_params("config.json")
    her_insta = api_link.format(config.pretty_girl)

    if not os.path.exists(config.pretty_girl):
        build_base()
    else:
        update_base()








import urllib2
import cv2
import json
import glob, os
from config import *
from pprint import pprint


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
        print j
        try:
            f = open('{0}/{1}.jpg'.format(pretty_girl, key), 'wb')
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
    print("Detecting photos with face...")

    for j, pic in enumerate(["{}/{}.jpg".format(pretty_girl, x) for x in photos_list]):
        n, photo_type = n_faces(pic)
        if n == n_persons:
            photo_id = os.path.basename(pic).split(".")[0]
            print("idx={0}, id={1}, type='{2}'".format(j, photo_id, photo_type))
            portrait_id.append(photo_id),
    return portrait_id


def save_list(fn, l):
    base = open(fn, "w")
    for item in l:
        base.write("%s\n" % item)


def build_base():
    links = photos_links(min_posts)

    if not os.path.exists(pretty_girl):
        os.makedirs(pretty_girl)

    load_photos(links)

    portraits = detect_portrait(links.keys())
    save_list("{}/portraits.txt".format(pretty_girl), portraits)


def update_base():
    links = photos_links(min_posts)
    new_ids = set(links.keys())
    old_ids = set([os.path.basename(x).split(".")[0] for x in glob.glob(pretty_girl + "/*.jpg")])

    if not new_ids - old_ids:
        print "No new photos"
        return

    load_photos(new_ids - old_ids)

    for x in list(old_ids - new_ids):
        print "{} removed".format(x)
        os.remove("{}/{}.jpg".format(pretty_girl, x))

    print "New photos ids:"
    pprint(new_ids - old_ids)

    portraits = detect_portrait(new_ids - old_ids)
    save_list("{}/portraits.txt".format(pretty_girl), portraits)

if __name__ == '__main__':
    if not os.path.exists(pretty_girl):
        print "Building photo base..."
        build_base()
        print "Done!"
    else:
        print "Updating photo base..."
        update_base()
        print "Done!"







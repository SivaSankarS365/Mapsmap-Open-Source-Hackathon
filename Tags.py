import json
import os


class Tags():
    """ Class to store tags. Tags are of three types. Whitetags are the ~950 base tags with which the base tagging model
    is trained on. Blacktags are the tags in whitelist that are ignored during prediction. Bluetags are the new tags created by the
    user apart from whitetags. """

    def __init__(self, base_path=r'Data'):
        self.base_path = base_path
        with open(os.path.join(self.base_path, 'Tags', 'Black_tags.json')) as f:
            self.black_tags = json.load(f)
        with open(os.path.join(self.base_path, 'Tags', 'Blue_tags.json')) as f:
            self.blue_tags = json.load(f)
        with open(os.path.join(self.base_path, 'Tags', 'White_tags.json')) as f:
            self.white_tags = json.load(f)
        with open(os.path.join('Database', 'conceptnet_vocab.json')) as f:
            self.available_words = json.load(f)

    def get_white_tags(self):
        """Returns latest white tag list"""
        self.reload()
        return self.white_tags

    def get_black_tags(self):
        """Returns latest black tag list"""
        self.reload()
        return self.black_tags

    def get_blue_tags(self):
        """Returns latest blue tag list. Blue tags are the extra tags that are 
        not included in the base trained DeepLearning models. This tags are assigned based on similarity to tags predicted
        by base DeepLearning models. """
        self.reload()
        return self.blue_tags

    def add(self, tag):
        " Adds tag to bluelist provided tag is not already present in white or blue or blacklist."

        tag = tag.lower().replace("-", '_')
        if tag not in self.available_words:
            print('Not in ConceptNet. Try a similar word?')
            return
        if (tag.replace("_", '-') in self.white_tags or tag in self.blue_tags) and tag not in self.black_tags:
            print('Already Exists!')
        elif tag in self.black_tags:
            print('Tag already exists in blacklist, contact admin')
        else:
            self.blue_tags.append(tag)
            print('Added')

        self.save()

    def remove(self, tag):
        """Removes a tag. If the tag is present in whitelist, then the tag is appended to blacklist."""
        tag = tag.lower().replace("-", '_')
        if tag in self.get_black_tags():
            print('Tag already exists in blacklist!')
        elif tag in self.get_blue_tags():
            self.blue_tags.remove(tag)
            print('Tag removed from blue list')
        elif tag.replace("_", '-') in self.get_white_tags():
            self.black_tags.append(tag.replace("_", '-'))
            print(tag, end=" ")
            print('Tag blacklisted')
        else:
            print('Tag not found')
        self.save()

    def remove_tag_from_blacklist(self, tag):
        """Removes a tag from blacklist"""
        if tag in self.get_black_tags():
            self.black_tags.remove(tag)
            print('Tag removed from blacklist')
            self.save()
        else:
            print('Tag not present in black listed tags')

    def save(self):
        """ Save the latest copy."""
        with open(os.path.join(self.base_path, 'Tags', 'Black_tags.json'), 'w') as f:
            json.dump(self.black_tags, f)
        with open(os.path.join(self.base_path, 'Tags', 'Blue_tags.json'), 'w') as f:
            json.dump(self.blue_tags, f)

    def reload(self):
        """Fetch the latest copy of tags"""
        with open(os.path.join(self.base_path, 'Tags', 'Black_tags.json')) as f:
            self.black_tags = json.load(f)
        with open(os.path.join(self.base_path, 'Tags', 'Blue_tags.json')) as f:
            self.blue_tags = json.load(f)
        with open(os.path.join(self.base_path, 'Tags', 'White_tags.json')) as f:
            self.white_tags = json.load(f)

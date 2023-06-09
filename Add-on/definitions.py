import re
import urllib.parse
import requests
import json
import bpy
bl_info = {
    "name": "Wiki Downloader",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Text Editor > Text > Wiki Download",
    "description": "Downloads texts from Wikipedia based on given phrases",
    "category": "Text Editor",
}


class WikiDownloadOperator(bpy.types.Operator):
    """Wiki download"""
    bl_idname = "text.wiki_download"
    bl_label = "Download Texts From Wiki"
    bl_options = {'REGISTER'}

    def execute(self, context):
        # 0. setup phrase list
        if not "Wiki Phrases" in bpy.data.texts:
            self.report(type={"ERROR"},
                        message="Create 'Wiki Phrases' text file.")
            return {"CANCELLED"}

        phrases = bpy.data.texts["Wiki Phrases"].as_string().splitlines()
        not_matched = []
        partial_matches = []
        full_matches = []
        for i, possible_title in enumerate(phrases):
            print(f"Extract {i+1}/{len(phrases)}, "+possible_title)
            # 1. search
            search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=&list=search&continue=-%7C%7Clanglinks&srsearch={urllib.parse.quote_plus(possible_title)}&srnamespace=0&srlimit=1&srinfo=&srprop="

            resp = requests.get(search_url).json()

            # 2. compare titles
            try:
                if len(resp['query']['search']) == 0:
                    print(' ##### Object not matched:', possible_title)
                    not_matched.append(possible_title)
                    continue
                title = resp['query']['search'][0]['title']
            except Exception as e:
                print(e)
                print(json.dumps(resp, indent=2))
                continue

            diff = len(set(title.lower()) ^ set(possible_title.lower()))

            if diff > 3:
                print(' ##### Object not matched:', possible_title)
                not_matched.append(possible_title)
                continue
            elif title.lower() != possible_title.lower():
                print(f' +++++ Object partial match ({diff}):', possible_title)
                partial_matches.append(possible_title)

            # 3. get extract
            # extract_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={urllib.parse.quote_plus(title)}&prop=extracts&exintro&explaintext"
            # extract
            extract_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={urllib.parse.quote_plus(title)}&prop=extracts|info&explaintext&inprop=url"

            resp = requests.get(extract_url).json()
            wiki_page = resp['query']['pages'].popitem()[1]
            extract = wiki_page['extract']
            wiki_url = wiki_page['canonicalurl']

            if extract.startswith(f"{title} may refer to:"):
                print(' ????? Object not matched (multi-results page):',
                      possible_title)
                not_matched.append(possible_title)
                continue
            full_matches.append(possible_title)

            if title in bpy.data.texts:
                text_edit = bpy.data.texts[title]
                text_edit.clear()
            else:
                text_edit = bpy.data.texts


def register():
    bpy.utils.register_class(WikiDownloadOperator)


def unregister():
    bpy.utils.unregister_class(WikiDownloadOperator)


if __name__ == "__main__":
    register()

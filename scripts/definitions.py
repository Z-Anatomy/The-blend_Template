# script for the definitions
# Download the data from wikipedia

import bpy
import json
import requests
import urllib.parse
import re


class TEXT_OT_wiki_download(bpy.types.Operator):
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
            # extract_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={urllib.parse.quote_plus(title)}&prop=extracts&explaintext"
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
                text_edit = bpy.data.texts.new(title)

            # Delete unwanted content
            extract += '\n'*3
            for paragraph in ("== Additional images ==", "== See also ==", "== References ==", "== External links =="):
                extract = re.sub(rf'{paragraph}\n+.*?\n\n\n',
                                 '', extract, flags=re.MULTILINE | re.DOTALL)

            extract = re.sub(r'( ==\n)(.?)', r'\1\n\2',
                             extract, flags=re.MULTILINE)
            extract = re.sub(r'( ===\n)(.?)', r'\1\n\2',
                             extract, flags=re.MULTILINE)
            extract = re.sub(r'  ', r' ', extract)
            extract = re.sub(r'(\. )([A-Z])', r'\1\n\n\2', extract)
            extract = re.sub(r' \[Fig\. \d+\]', r'', extract)

            body = "\n"*2 + title.upper() + "\n"*3 + extract + "\n" + wiki_url
            text_edit.write(body)
            text_edit.cursor_set(0)

            # path_to_blend = bpy.path.abspath('//')
            # Path(os.path.join(path_to_blend, 'wiki_download')).mkdir(parents=True, exist_ok=True)
            # with open(os.path.join(path_to_blend, 'wiki_download', title+'.txt'), 'w') as f:
            #     f.write(body)

        if 'Wiki Results' in bpy.data.texts:
            wiki_results = bpy.data.texts['Wiki Results']
            wiki_results.clear()
        else:
            wiki_results = bpy.data.texts.new('Wiki Results')
        body = "===== Wiki download report =====\n"
        body += " ## Partial matches (check manualy) ##\n"
        body += "\n".join(partial_matches) + "\n"*5
        body += " ## Not matched ##\n"
        body += "\n".join(not_matched) + "\n"*5
        body += " ## Fully matched ##\n"
        body += "\n".join(full_matches) + "\n"*5
        wiki_results.write(body)
        wiki_results.cursor_set(0)

        return {"FINISHED"}

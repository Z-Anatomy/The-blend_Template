import bpy


def clean_name(name):
    for ending in ('.r', '.l', '.t', '.st', '.r.t', '.l.t', '.g', '.j', ''):
        if ending == '':
            return name, ending
        elif name.endswith(ending):
            clean_name = name[:-len(ending)]
            return clean_name, ending


def first_n_bytes(string, n=63):
    byte_length = 0
    out = ''
    for char in string:
        byte_length += len(char.encode())
        if byte_length <= n:
            out += char
        else:
            return out
    return out


fonts = {
    'English': 'Bfont',
    'Latin': 'Bfont',
    'Français': 'Bfont',
    'Español': 'Bfont',
    'Portugues': 'Bfont',
}


class OBJECT_OT_translate_atlas(bpy.types.Operator):
    """Translate atlas"""
    bl_idname = "object.translate_atlas"
    bl_label = "Translate"
    bl_options = {'REGISTER', 'UNDO'}

    lang: bpy.props.EnumProperty(items=[
        ('English', 'English', '', 0),
        ('Latin', 'Latin', '', 1),
        ('Français', 'Français', '', 2),
        ('Español', 'Español', '', 3),
        ('Portugues', 'Portugues', '', 4),
    ],
        default='English',
        name="Language")

    def execute(self, context):

        if self.lang == "English":
            for ob in bpy.data.objects[:]:
                # print('# ob:', ob)
                if ob.type == "MESH":
                    _, ending = clean_name(ob.name)
                    eng_name, _ = clean_name(ob.data.name)
                    ob.name = eng_name + ending
                elif ob.type == "CURVE":
                    _, ending = clean_name(ob.name)
                    eng_name, _ = clean_name(ob.data.name)
                    ob.name = eng_name + ending
                elif ob.type == "FONT":
                    ob.name = ob.data.name
                    ob.data.body = clean_name(ob.data.name)[0].upper()
                    ob.data.font = bpy.data.fonts['Bfont']
                    if not ob.name.endswith('.st'):
                        ob.data.size = 0.003

            for col in bpy.data.collections[:]:
                # print('# col:', col)
                if 'English' in col.keys():
                    col.name = col['English']
            return {"FINISHED"}

        translations = bpy.data.texts['Translations'].as_string().splitlines()
        languages = translations[0].split(';')
        trans_dict = dict()
        for langs in translations[1:]:
            langs = list(zip(languages, langs.split(';')))
            translated_phrase = trans_dict[langs[0][1]] = dict()
            for lang in langs[1:]:
                translated_phrase[lang[0]] = lang[1]

        for ob in bpy.data.objects[:]:
            # print('# ob:', ob)
            if ob.type == "MESH":
                _, ending = clean_name(ob.name)
                eng_name, _ = clean_name(ob.data.name)
                if eng_name in trans_dict:
                    new_name = trans_dict[eng_name][self.lang]
                    new_name = first_n_bytes(new_name)
                    ob.name = new_name + ending
            elif ob.type == "FONT":
                _, ending = clean_name(ob.name)
                eng_name, _ = clean_name(ob.data.name)
                if eng_name in trans_dict:
                    new_name = trans_dict[eng_name][self.lang]
                    ob.data.body = new_name.upper()

                    new_name = first_n_bytes(new_name)
                    ob.name = new_name + ending

                    try:
                        ob.data.font = bpy.data.fonts[fonts[self.lang]]
                    except:
                        self.report(
                            type={"WARNING"}, message=f"Font {fonts[self.lang]} not found. Add it manualy.")

                    if not ob.name.endswith('.st'):
                        if self.lang == '中國人':
                            ob.data.size = 0.006
                        else:
                            ob.data.size = 0.003
            elif ob.type == "CURVE":
                _, ending = clean_name(ob.name)
                eng_name, _ = clean_name(ob.data.name)
                if eng_name in trans_dict:
                    new_name = trans_dict[eng_name][self.lang]
                    new_name = first_n_bytes(new_name)
                    ob.name = new_name + ending

        for col in bpy.data.collections[:]:
            # print('# col:', col)
            if 'English' in col.keys():
                eng_name = col['English']
                if eng_name.endswith("'"):
                    eng_name = eng_name[:-1]
                    if eng_name in trans_dict:
                        col.name = trans_dict[eng_name][self.lang] + "'"
                elif eng_name in trans_dict:
                    col.name = trans_dict[eng_name][self.lang]

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

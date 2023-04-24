import bpy

TA2list = []

Texts = []

Objs = []

Labels = []


def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(
                    override, text=str(data), type="OUTPUT")


# get the translation
translations = bpy.data.texts['Translations'].as_string().splitlines()
for line in translations[1:]:
    getfirst = line.split(";")
    TA2list.append(getfirst[0])


# get the text

for text in bpy.data.texts:
    Texts.append(text.name)


# get the obj and label
for obj in bpy.data.objects:
    # Exclude objects whose name ends with '.t', '.s', or '.g'
    if not obj.name.endswith(('.t', '.s', '.g')):
        # Remove suffixes from object names
        obj_name = obj.name.split('.')[0]
        # Remove any parts of the name following a dot that are not a space
        if '.' in obj_name and not obj_name.split('.')[1].isspace():
            obj_name = obj_name.split('.')[0]
        Objs.append(f'{obj_name}')
    else:
        Labels.append(f'{obj.name.split(".")[0]}')


# search for all the translations, create a new array of '' and x
# output into three different files => list, obj, and text

# Get or create the 'List_Definitions' text
if 'List_Definitions' in bpy.data.texts:
    List_Definitions = bpy.data.texts['List_Definitions']
    List_Definitions.clear()
else:
    List_Definitions = bpy.data.texts.new('List_Definitions')

# Get or create the 'List_3D' text
if 'List_3D' in bpy.data.texts:
    List_3D = bpy.data.texts['List_3D']
    List_3D.clear()
else:
    List_3D = bpy.data.texts.new('List_3D')

# Get or create the 'List_labels' text
if 'List_labels' in bpy.data.texts:
    List_labels = bpy.data.texts['List_labels']
    List_labels.clear()
else:
    List_labels = bpy.data.texts.new('List_labels')


LIST_3D = []
LIST_DEFINITIONS = []
LIST_LABELS = []


for i in TA2list:
    if i in Texts:
        LIST_DEFINITIONS.append("x")
    else:
        LIST_DEFINITIONS.append("")
    if i in Objs:
        LIST_3D.append("x")
    else:
        LIST_3D.append("")
    if i in Labels:
        LIST_LABELS.append("x")
    else:
        LIST_LABELS.append("")


# Write the content of the variables to the corresponding texts
List_Definitions.write(
    'Def \n \n' + ''.join(i + "\n" for i in LIST_DEFINITIONS))
List_3D.write('3D \n \n' + ''.join(i + "\n" for i in LIST_3D))
List_labels.write('Lbl \n \n' + ''.join(i + "\n" for i in LIST_LABELS))

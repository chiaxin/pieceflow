import os.path
import maya.OpenMaya as api
import maya.cmds as mc

def export_to_outside(item, directory):
    if not os.path.isdir(directory):
        api.MGlobal.displayError(
            '{} directory is not exists!'.format(directory))
        return ''
    selection_list = api.MSelectionList()
    try:
        selection_list.add(item)
    except:
        api.MGlobal.displayError('{} is not exists'.format(item))
        raise
    export_maya = '{0}/{1}.ma'.format(directory, item)
    export_log = '{0}/{1}.log'.format(directory, item)
    obj_root = api.MObject()
    selection_list.getDependNode(0, obj_root)
    obj_connected_set = api.MObjectArray()
    itDependGraph = api.MItDependencyGraph(obj_root,
        api.MFn.kInvalid, api.MItDependencyGraph.kUpstream)
    while not itDependGraph.isDone():
        obj_connected_set.append(itDependGraph.currentItem())
        itDependGraph.next()
    log = open(export_log, 'w')
    preserve_selected = api.MSelectionList()
    api.MGlobal.getActiveSelectionList(preserve_selected)
    api.MGlobal.clearSelectionList()
    for idx in range(obj_connected_set.length()):
        api.MGlobal.select(obj_connected_set[idx])
        log.write(api.MFnDependencyNode(obj_connected_set[idx]).name()+'\n')
    log.close()
    api.MFileIO.exportSelected(export_maya)
    api.MGlobal.setActiveSelectionList(preserve_selected)

def _addUnderscore(node):
    renamed_set = []
    pre_name = '_' + node.strip('_')
    while mc.objExists(pre_name):
        pre_name = '_' + pre_name
    renamed_set.append(mc.rename(node, pre_name))
    return renamed_set

def receive_from_outside(item, directory):
    import_maya = '{0}/{1}.ma'.format(directory, item)
    read_log = '{0}/{1}.log'.format(directory, item)
    if not os.path.isfile(import_maya):
        api.MGlobal.displayError('{} is not found!'.format(import_maya))
        return ''
    if not os.path.isfile(read_log):
        api.MGlobal.displayError('{} is not found!'.format(read_log))
        return ''
    with open(read_log, 'r') as log:
        data = log.read()
    items_set = data.split()
    same_name_items = [item for item in items_set if mc.objExists(item)]
    renamed_set = []
    for node in same_name_items:
        renamed_set.append(_addUnderscore(node))
    print renamed_set
    api.MFileIO.importFile(import_maya)
    return items_set

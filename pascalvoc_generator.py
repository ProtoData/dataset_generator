from lxml.etree import Element, SubElement, tostring
from xml.dom.minidom import parseString
 
 
def pascalvoc_gen(folder, image_name, image_w, image_h, name, bndbox):
    """
    :param folder: anootations dir
    :param image_name: image name
    :param image_w: image width
    :param image_h: imge height
    :param name: class name
    :param bndbox: bound box cords
    """ 
    node_root = Element('annotation')
    
    node_folder = SubElement(node_root, 'folder')
    node_folder.text = folder
    
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = image_name
    
    node_source = SubElement(node_root, 'source')
    node_database = SubElement(node_source, 'database')
    node_database.text = 'Unknown'

    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = image_w
    
    node_height = SubElement(node_size, 'height')
    node_height.text = image_h
    
    node_depth = SubElement(node_size, 'depth')
    node_depth.text = '3'
    
    node_segmented =SubElement(node_root, 'segmented')
    node_segmented.text = '0'

    node_object = SubElement(node_root, 'object')
    node_name = SubElement(node_object, 'name')
    node_name.text = name
    node_pose = SubElement(node_object, 'pose')
    node_pose.text = 'Unspecified'
    node_truncated = SubElement(node_object, 'truncated')
    node_truncated.text = '0'
    node_difficult = SubElement(node_object, 'difficult')
    node_difficult.text = '0'
    node_bndbox = SubElement(node_object, 'bndbox')
    node_xmin = SubElement(node_bndbox, 'xmin')
    node_xmin.text = bndbox[0][1]
    node_ymin = SubElement(node_bndbox, 'ymin')
    node_ymin.text = bndbox[0][0]
    node_xmax = SubElement(node_bndbox, 'xmax')
    node_xmax.text = bndbox[1][1]
    node_ymax = SubElement(node_bndbox, 'ymax')
    node_ymax.text = bndbox[1][0]
    
    return tostring(node_root)
import xml.etree.ElementTree as ET
from xml.dom import minidom
import uuid
import re

def parse_config(file_path):
    folder_hierarchy = {}
    current_path = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('SubRep='):
                path = line.split('=', 1)[1]
                parts = [p for p in path.split('\\') if p]
                current_path = parts
                
                current_node = folder_hierarchy
                for part in parts:
                    if part not in current_node:
                        current_node[part] = {'sessions': [], 'subfolders': {}}
                    current_node = current_node[part]['subfolders']
                    
            elif line and '=' in line and current_path:
                session_name, session_data = line.split('=', 1)
                if '%' in session_data:
                    ip_match = re.search(r'%(\d+\.\d+\.\d+\.\d+)%', session_data)
                    if ip_match:
                        ip = ip_match.group(1)
                        port_match = re.search(r'%(\d+)%', session_data.split(ip)[1])
                        port = port_match.group(1) if port_match else "22"
                        
                        current_node = folder_hierarchy
                        for part in current_path:
                            if part not in current_node:
                                current_node[part] = {'sessions': [], 'subfolders': {}}
                            current_node = current_node[part]['subfolders']
                        
                        parent = folder_hierarchy
                        for part in current_path[:-1]:
                            parent = parent[part]['subfolders']
                        
                        if current_path[-1] not in parent:
                            parent[current_path[-1]] = {'sessions': [], 'subfolders': {}}
                        
                        parent[current_path[-1]]['sessions'].append({
                            'name': session_name,
                            'ip': ip,
                            'port': port,
                            'protocol': 'ssh' if 'ssh' in session_name.lower() else 'telnet'
                        })
    return folder_hierarchy

def build_xml_structure(parent_node, folders):
    for folder_name, folder_data in folders.items():
        folder_node = ET.SubElement(parent_node, "Node", Type="0", Expanded="1")
        ET.SubElement(folder_node, "DisplayName").text = folder_name
        
        for session in folder_data['sessions']:
            session_node = ET.SubElement(folder_node, "Node", Type="1")
            ET.SubElement(session_node, "SavedSession").text = "Default Settings"
            ET.SubElement(session_node, "DisplayName").text = session['ip']
            ET.SubElement(session_node, "UID").text = "{" + str(uuid.uuid4()).upper() + "}"
            ET.SubElement(session_node, "ServerName").text = session['ip']
            ET.SubElement(session_node, "PuttyConType").text = "4" if session['protocol'] == 'ssh' else "2"
            ET.SubElement(session_node, "Port").text = session['port']
            ET.SubElement(session_node, "UserName").text = ""
            ET.SubElement(session_node, "Password").text = "UH+BjMijYI8="
            ET.SubElement(session_node, "PasswordDelay").text = "0"
            ET.SubElement(session_node, "CLParams").text = f"{session['ip']} -{'ssh' if session['protocol'] == 'ssh' else 'telnet'}"
            ET.SubElement(session_node, "ScriptDelay").text = "0"
        
        if folder_data['subfolders']:
            build_xml_structure(folder_node, folder_data['subfolders'])

def create_multiput_xml(folder_hierarchy, output_file):
    root = ET.Element("Servers")
    putty = ET.SubElement(root, "Putty")
    
    build_xml_structure(putty, folder_hierarchy)
    
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="\t", encoding='utf-8')
    
    with open(output_file, 'wb') as f:
        f.write(pretty_xml)

input_file = r"C:\Users\MobaXterm.mobaconf"
output_file = r"C:\Users\multiput_sessions.xml"

folder_hierarchy = parse_config(input_file)
create_multiput_xml(folder_hierarchy, output_file)

print(f"Successfully completed. {output_file}")
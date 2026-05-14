"""
DAE (Collada) 3D Model Parser
Simplified for web backend
"""
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional

class DAEParser:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = {
            "cameras": [],
            "meshes": [],
            "materials": [],
            "lights": [],
            "metadata": {
                "filename": self.filepath.name,
                "format": ".dae",
            }
        }
    
    def parse(self) -> bool:
        """Parse DAE file"""
        try:
            tree = ET.parse(self.filepath)
            root = tree.getroot()
            
            # Namespace
            ns = {'dae': 'http://www.collada.org/2005/11/COLLADASchema'}
            
            # Extract cameras
            for camera in root.findall('.//dae:camera', ns):
                name = camera.get('id', 'Camera')
                self.data['cameras'].append({'name': name})
            
            # Extract meshes
            for geometry in root.findall('.//dae:geometry', ns):
                name = geometry.get('id', 'Mesh')
                mesh_obj = geometry.find('.//dae:mesh', ns)
                if mesh_obj is not None:
                    self.data['meshes'].append({
                        'name': name,
                        'vertices': len(mesh_obj.findall('.//dae:source', ns))
                    })
            
            # Extract materials
            for material in root.findall('.//dae:material', ns):
                name = material.get('id', 'Material')
                self.data['materials'].append({'name': name})
            
            # Extract lights
            for light in root.findall('.//dae:light', ns):
                name = light.get('id', 'Light')
                self.data['lights'].append({'name': name})
            
            return len(self.data['meshes']) > 0
        
        except Exception as e:
            print(f"DAE parse error: {e}")
            return False
    
    def get_data(self) -> Dict:
        """Get parsed data"""
        return self.data
    
    def get_info(self) -> Dict:
        """Get summary info"""
        return {
            "cameras": len(self.data['cameras']),
            "meshes": len(self.data['meshes']),
            "materials": len(self.data['materials']),
            "lights": len(self.data['lights']),
            "filename": self.data['metadata']['filename']
        }

import hashlib
from dataclasses import dataclass #Evita el boilerplate o código repetitivo
from typing import List, Tuple, Optional

def sha256(data: str) -> str:
    """Calcula la huella digital criptográfica SHA-256 de un texto."""
    # Convertimos el texto a bytes UTF-8, calculamos el hash y lo retornamos en hexadecimal (64 caracteres)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

@dataclass
class MerkleNode:
    """Representa un nodo individual dentro de la estructura del árbol."""
    hash_val: str                                 # El valor Hash SHA-256 del nodo
    left: Optional['MerkleNode'] = None           # Puntero al hijo izquierdo (None si es hoja)
    right: Optional['MerkleNode'] = None          # Puntero al hijo derecho (None si es hoja)
    is_duplicated: bool = False                   # Marca si el nodo fue clonado por regla de impar

class MerkleTree:
    """Clase principal encargada de construir, dibujar y verificar el Árbol de Merkle."""
    
    def __init__(self, data_blocks: List[str]):
        # Validamos que la lista de datos no venga vacía
        if not data_blocks:
            raise ValueError("La lista de bloques no puede estar vacía.")
        
        self.data_blocks = list(data_blocks)      # Guardamos la lista de transacciones originales
        # Creamos la lista inicial de nodos hoja calculando el SHA-256 de cada transacción
        self.leaves: List[MerkleNode] = [MerkleNode(sha256(block)) for block in data_blocks]
        # Construimos el árbol recursivamente desde la base hasta la raíz
        self.root: MerkleNode = self._build_tree(list(self.leaves))

    def _build_tree(self, nodes: List[MerkleNode]) -> MerkleNode:
        """Construye el árbol de abajo hacia arriba (Bottom-Up) combinando parejas de nodos."""
        # CASO BASE: Si solo queda 1 nodo en la lista, ese único nodo es la Merkle Root
        if len(nodes) == 1:
            return nodes[0]
        
        # REGLA IMPAR: Si la cantidad de nodos es impar, clonamos el último para poder formar parejas
        if len(nodes) % 2 != 0:
            last_node = nodes[-1]
            duplicated_node = MerkleNode(
                hash_val=last_node.hash_val, 
                left=last_node.left, 
                right=last_node.right,
                is_duplicated=True
            )
            nodes.append(duplicated_node)
            
        next_level: List[MerkleNode] = []
        # Recorremos la lista de 2 en 2 para agrupar hermanos
        for i in range(0, len(nodes), 2):
            left = nodes[i]                        # Hijo izquierdo
            right = nodes[i + 1]                    # Hijo derecho
            # Concatenamos los dos hashes hijos y calculamos el hash del nodo padre
            combined_hash = sha256(left.hash_val + right.hash_val)
            # Creamos el nodo padre enlazando sus dos hijos
            parent = MerkleNode(hash_val=combined_hash, left=left, right=right)
            next_level.append(parent)
            
        # Llamamos recursivamente con el nuevo nivel superior
        return self._build_tree(next_level)

    @property
    def root_hash(self) -> str:
        """Propiedad que devuelve el hash completo de la Merkle Root."""
        return self.root.hash_val

    def print_tree(self, node: Optional[MerkleNode] = None, prefix: str = "", is_left: bool = True, is_root: bool = True, highlighted_hashes: set = None):
        """Dibuja la estructura jerárquica del árbol en consola destacando nodos de la ruta."""
        if node is None:
            node = self.root
        if highlighted_hashes is None:
            highlighted_hashes = set()

        # Resaltador visual: Si el hash del nodo pertenece a la ruta de verificación, le aplica formato activo
        is_highlighted = node.hash_val in highlighted_hashes
        color = "\033[93m\033[1m" if is_highlighted else ""  # Amarillo 
        reset = "\033[0m" if is_highlighted else ""
        mark = " ◄ [RUTA DE VERIFICACIÓN]" if is_highlighted else ""

        # Formateamos la etiqueta del nodo actual
        if is_root:
            label = f"{color}ROOT ── [{node.hash_val[:8]}...]{reset}{mark}"
        else:
            branch = "├── " if is_left else "└── "
            dup_tag = " (DUPLICADO)" if node.is_duplicated else ""
            leaf_tag = " (Hoja)" if node.left is None and node.right is None else ""
            label = f"{prefix}{branch}{color}[{node.hash_val[:8]}...]{leaf_tag}{dup_tag}{reset}{mark}"
        
        print(label)

        # Preparamos los conectores visuales para los hijos
        new_prefix = prefix + ("│   " if is_left else "    ")
        children = []
        if node.left: children.append((node.left, True))
        if node.right: children.append((node.right, False))

        # Recorremos recursivamente los hijos
        for child_node, child_is_left in children:
            self.print_tree(child_node, new_prefix, child_is_left, is_root=False, highlighted_hashes=highlighted_hashes)

    def get_proof(self, target_index: int) -> List[Tuple[str, str]]:
        """Genera la lista de nodos hermanos (camino criptográfico) para llegar a la raíz."""
        current_level = list(self.leaves)
        if len(current_level) % 2 != 0:
            current_level.append(MerkleNode(current_level[-1].hash_val, is_duplicated=True))
            
        proof = []
        idx = target_index
        
        # Recorremos ascendiendo por los niveles
        while len(current_level) > 1:
            if len(current_level) % 2 != 0:
                current_level.append(MerkleNode(current_level[-1].hash_val, is_duplicated=True))
                
            is_right = (idx % 2 == 1)               # Identificamos si el nodo actual está a la derecha
            sibling_idx = idx - 1 if is_right else idx + 1  # El hermano estará en el índice opuesto
            
            sibling_hash = current_level[sibling_idx].hash_val
            direction = 'left' if is_right else 'right'
            # Guardamos el hash del hermano y de qué lado debe combinarse
            proof.append((sibling_hash, direction))
            
            idx = idx // 2                          # Subimos al siguiente nivel dividiendo el índice por 2
            next_level = []
            for i in range(0, len(current_level), 2):
                combined = sha256(current_level[i].hash_val + current_level[i+1].hash_val)
                next_level.append(MerkleNode(combined))
            current_level = next_level
            
        return proof
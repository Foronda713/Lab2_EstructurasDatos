# Laboratorio 2: Implementación y Verificación de Árbol de Merkle

**Estudiante:** Miguel Foronda  
**Materia:** Estructuras de Datos  
**Lenguaje:** Python 3.10+  

---

## Descripción del Proyecto

Este laboratorio implementa un **Árbol de Merkle** (*Merkle Tree*) completo en Python utilizando únicamente librerías estándar (`hashlib` y `dataclasses`). El proyecto está diseñado con un menú interactivo en consola que permite visualizar en tiempo real la estructura jerárquica del árbol, la generación de la **Merkle Root**, la inmutabilidad de los datos mediante el efecto avalancha (un pequeño cambio modifica drásticamente el resultado) y la verificación criptográfica mediante **Pruebas de Inclusión** (*Merkle Proofs*).

---

## Requerimientos Técnicos Implementados

1. **Hashes en Hojas:** Cada nodo hoja contiene el hash SHA-256 de un bloque de datos o transacción individual.
2. **Nodos Internos:** Cada nodo intermedio almacena el hash SHA-256 de la concatenación en texto del hash de sus dos nodos hijos:
   Hash_padre = SHA256(Hash_izquierdo + Hash_derecho)
3. **Manejo de Impares (Duplicación):** Si en un nivel del árbol hay un número impar de nodos, el último nodo se duplica a sí mismo para completar la pareja y mantener la estructura binaria balanceada.
4. **Merkle Root:** La cúspide del árbol es un hash único de 64 caracteres hexadecimales que representa la integridad de todo el conjunto de datos.
5. **Prueba de Inclusión:** Generación de un camino criptográfico (*Audit Path*) para verificar la autenticidad de un bloque en tiempo $O(\log N)$ sin revelar todo el contenido del árbol.

---

## Nota sobre el Desarrollo y Metodología
El código completo de esta solución fue desarrollado con Inteligencia Artificial (Gémini 3.6 Flash) y detallado/refinado mediante la metodología VibeCoding, proceso en el cual se revisó minuciosamente la estructura de datos, la lógica algorítmica de los nodos, el manejo de la duplicación en hojas impares y los resultados finales en consola para garantizar el cumplimiento riguroso de las especificaciones del laboratorio.

---

## Estructura del Código
El repositorio está organizado en dos módulos principales:

### merkle_tree.py:

sha256(data): Función auxiliar para convertir cadenas de texto a hashes hexadecimales.

MerkleNode: Dataclass que representa un nodo con su hash, punteros (left, right) y banderas de control.

MerkleTree: Clase principal con lógica de construcción Bottom-Up (_build_tree), renderizado gráfico en consola (print_tree), extracción de hermanos (get_proof) y verificación (verify_proof).

### main_interactivo.py: Interfaz de línea de comandos en tiempo real para la ejecución de pruebas.

---

## Diagrama del Árbol de Merkle (5 Hojas Iniciales)

Al inicializar el proyecto con 5 bloques de datos (`Tx1` a `Tx5`), la presencia de un número impar de hojas hace que la quinta hoja se duplique para balancear el nivel inicial. Luego, al ascender al segundo nivel (3 nodos), la rama derecha vuelve a duplicarse para permitir la combinación final en la raíz:

```text
                                [ Merkle Root ]
                                H_01234444 = SHA256(H_0123 + H_4444)
                               /                                    \
                             /                                        \
               [ Nodo Interno ]                                        [ Nodo Interno ]
        H_0123 = SHA256(H_01 + H_23)                            H_4444 = SHA256(H_44 + H_44_dup)
              /            \                                          /            \
             /              \                                        /              \
    [ Nodo Interno ]     [ Nodo Interno ]                   [ Nodo Interno ]     [ Nodo Interno (Dup) ]
  H_01 = SHA256(H0+H1)   H_23 = SHA256(H2+H3)                 H_44 = SHA256(H4+H4)   H_44 = SHA256(H4+H4)
     /         \           /         \                       /         \             /         \
 [Hoja 0]   [Hoja 1]   [Hoja 2]   [Hoja 3]               [Hoja 4]   [Hoja 4 (Dup)] [Hoja 4 (Dup)] [Hoja 4 (Dup)]
   Tx1        Tx2        Tx3        Tx4                    Tx5        Tx5*          Tx5*          Tx5*

* Nota: "Tx5*" indica los nodos duplicados automáticamente por la regla de imparidad.


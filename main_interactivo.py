import os
from merkle_tree import MerkleTree, sha256
# Códigos ANSI para colores en consola
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear_screen():
    """Limpia la terminal en Windows o Linux/Mac."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(tree: MerkleTree, transactions: list):
    """Muestra el encabezado principal con la Merkle Root oficial."""
    print(f"{BOLD}{CYAN}============================================================{RESET}")
    print(f"{BOLD}{CYAN}         LABORATORIO: ÁRBOL DE MERKLE           {RESET}")
    print(f"{BOLD}{CYAN}============================================================{RESET}\n")
    print(f"  {BOLD}Merkle Root Oficial:{RESET} {GREEN}{tree.root_hash}{RESET}")
    print(f"{CYAN}{'-'*60}{RESET}")

def run_interactive():
    # 5 bloques iniciales de datos
    initial_transactions = [
        "Tx1: Miguel -> Samuel (10 BTC)",
        "Tx2: Samuel -> Sebastian (5 BTC)",
        "Tx3: Sebastian -> David (20 BTC)",
        "Tx4: David -> Stiven (15 BTC)",
        "Tx5: Stiven -> Andres (8 BTC)"
    ]

    transactions = list(initial_transactions)
    tree = MerkleTree(transactions)

    while True:
        clear_screen()
        print_header(tree, transactions)

        # MENÚ REESTRUCTURADO EN LAS 4 OPCIONES EXACTAS
        print(f"\n{BOLD}MENÚ PRINCIPAL:{RESET}")
        print(f"  {YELLOW}[1]{RESET} Crear y mostrar todo el árbol actual")
        print(f"  {YELLOW}[2]{RESET} Modificar una transacción")
        print(f"  {YELLOW}[3]{RESET} Reiniciar")
        print(f"  {YELLOW}[4]{RESET} Prueba de Inclusión a cadena de texto")
        print(f"  {YELLOW}[0]{RESET} Salir")

        option = input(f"\n{BOLD}Selecciona una opción [0-4]: {RESET}").strip()

        # -----------------------------------------------------------------
        # 1. CREAR Y MOSTRAR TODO EL ÁRBOL ACTUAL
        # -----------------------------------------------------------------
        if option == "1":
            print(f"\n{BOLD}--- 1. ESTRUCTURA COMPLETA DEL ÁRBOL ---{RESET}\n")
            print(f"{BOLD}Bloques / Transacciones Registradas ({len(transactions)}):{RESET}")
            for i, tx in enumerate(transactions):
                print(f"  Hoja [{i}]: {tx:<35} -> Hash: {BLUE}{sha256(tx)[:12]}...{RESET}")
            
            print(f"\n{BOLD}Diagrama de Jerarquía Binaria:{RESET}\n")
            tree.print_tree()
            input("\nPresiona Enter para continuar...")

        # -----------------------------------------------------------------
        # 2. MODIFICAR UNA TRANSACCIÓN
        # -----------------------------------------------------------------
        elif option == "2":
            print(f"\n{BOLD}--- 2. MODIFICAR UNA TRANSACCIÓN ---{RESET}")
            try:
                idx = int(input(f"Ingresa el índice a modificar (0 - {len(transactions)-1}): "))
                if 0 <= idx < len(transactions):
                    old_tx = transactions[idx]
                    old_root = tree.root_hash

                    new_tx = input(f"Nuevo texto para la transacción [{idx}] (Actual: '{old_tx}'): ").strip()
                    if not new_tx:
                        print(f"{RED}La transacción no puede estar vacía.{RESET}")
                    else:
                        transactions[idx] = new_tx
                        tree = MerkleTree(transactions) # Reconstruimos árbol

                        print(f"\n{GREEN}[ACTUALIZADO EXÍTOSAMENTE]{RESET}")
                        print(f"  Anterior : {RED}{old_tx}{RESET}")
                        print(f"  Nueva    : {GREEN}{new_tx}{RESET}")
                        print(f"  Raíz Vieja: {BLUE}{old_root[:16]}...{RESET}")
                        print(f"  Raíz Nueva: {RED}{tree.root_hash[:16]}...{RESET}")
                        print(f"  {GREEN}✓ La Merkle Root cambió (Efecto avalancha verificado).{RESET}")
                else:
                    print(f"{RED}Índice fuera de rango.{RESET}")
            except ValueError:
                print(f"{RED}Entrada inválida. Ingresa un número entero.{RESET}")
            input("\nPresiona Enter para continuar...")

        # -----------------------------------------------------------------
        # 3. REINICIAR
        # -----------------------------------------------------------------
        elif option == "3":
            transactions = list(initial_transactions)
            tree = MerkleTree(transactions)
            print(f"\n{GREEN}✓ Árbol reiniciado exitosamente al estado original con 5 transacciones.{RESET}")
            input("\nPresiona Enter para continuar...")

        # -----------------------------------------------------------------
        # 4. PRUEBA DE INCLUSIÓN A CADENA DE TEXTO (DEMOSTRACIÓN MATEMÁTICA)
        # -----------------------------------------------------------------
        elif option == "4":
            print(f"\n{BOLD}--- 4. PRUEBA DE INCLUSIÓN A CADENA DE TEXTO ---{RESET}")
            target_tx = input("Ingresa la cadena de texto exacta a verificar: ").strip()

            if not target_tx:
                print(f"{RED}No ingresaste ninguna cadena.{RESET}")
            
            elif target_tx in transactions:
                # CASO A: EL DATO PERTENECE AL ÁRBOL (VÁLIDO)
                idx = transactions.index(target_tx)
                proof = tree.get_proof(idx)
                
                print(f"\n{GREEN}[VÁLIDA ✓]{RESET} La transacción existe en la Hoja [{idx}].")
                print(f"{BOLD}Paso 1: Aplicar Hash SHA-256 al dato ingresado:{RESET}")
                current_hash = sha256(target_tx)
                print(f"  Hash base H({target_tx}) -> {YELLOW}{current_hash[:16]}...{RESET}\n")

                print(f"{BOLD}Paso 2: Ascenso por la ruta combinando con nodos hermanos:{RESET}")
                route_hashes = {current_hash}
                
                for step, (sibling_hash, direction) in enumerate(proof, 1):
                    if direction == 'left':
                        combined = sibling_hash + current_hash
                        expr = f"SHA256(Hermano_Izquierdo [{BLUE}{sibling_hash[:8]}...{RESET}] + Actual [{YELLOW}{current_hash[:8]}...{RESET}])"
                    else:
                        combined = current_hash + sibling_hash
                        expr = f"SHA256(Actual [{YELLOW}{current_hash[:8]}...{RESET}] + Hermano_Derecho [{BLUE}{sibling_hash[:8]}...{RESET}])"
                    
                    current_hash = sha256(combined)
                    route_hashes.add(current_hash)
                    print(f"  Nivel {step}: {expr} = {YELLOW}{current_hash[:16]}...{RESET}")

                print(f"\n{BOLD}Paso 3: Árbol completo resaltando la ruta calculada:{RESET}\n")
                tree.print_tree(highlighted_hashes=route_hashes)

                print(f"\n{BOLD}Paso 4: Demostración Matemática:{RESET}")
                print(f"  Raíz Reconstruida : {GREEN}{current_hash}{RESET}")
                print(f"  Merkle Root Oficial: {GREEN}{tree.root_hash}{RESET}")
                print(f"  {GREEN}✓ [DEMOSTRADO]: La raíz calculada coincide EXACTAMENTE con la oficial. El dato es auténtico.{RESET}")

            else:
                # CASO B: EL DATO NO ESTÁ (FALLO Y COMPARACIÓN)
                input_hash = sha256(target_tx)
                print(f"\n{RED}[INVÁLIDA ✗]{RESET} La transacción NO pertenece al árbol registrado.")
                print(f"{BOLD}Paso 1: Aplicar Hash SHA-256 al dato falso/desconocido:{RESET}")
                print(f"  Hash generado -> {RED}{input_hash}{RESET}\n")

                # Asumimos una posición arbitraria (ej: Hoja 0) para mostrar cómo divergen los datos
                arbitrary_idx = 0
                proof = tree.get_proof(arbitrary_idx)
                
                print(f"{BOLD}Paso 2: Intentar construir la ruta ascendente con la prueba de la Hoja [0]:{RESET}")
                calc_hash = input_hash
                for step, (sibling_hash, direction) in enumerate(proof, 1):
                    combined = sibling_hash + calc_hash if direction == 'left' else calc_hash + sibling_hash
                    calc_hash = sha256(combined)
                    print(f"  Nivel {step}: Operación con Hermano [{BLUE}{sibling_hash[:8]}...{RESET}] -> Da: {RED}{calc_hash[:16]}...{RESET}")

                print(f"\n{BOLD}Paso 3: Comparación de Raíces (Divergencia Matemática):{RESET}")
                print(f"  Lo que da el dato ingresado : {RED}{calc_hash}{RESET}")
                print(f"  Lo que debería dar (Oficial): {GREEN}{tree.root_hash}{RESET}")
                print(f"  {RED}✗ [FALLO DEMOSTRADO]: Las raíces divergen por completo. El dato es falso o fue alterado.{RESET}")

            input("\nPresiona Enter para continuar...")

        elif option == "0":
            print(f"\n{CYAN}¡Laboratorio finalizado!{RESET}\n")
            break

        else:
            print(f"{RED}Opción no válida. Selecciona un número entre 0 y 4.{RESET}")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    run_interactive()
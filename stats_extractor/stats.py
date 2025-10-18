import json
from collections import Counter
import os

def analyze_dataset_formats(json_file_path):
    """
    Analiza un archivo JSON con datasets y proporciona estadísticas sobre los formatos
    de las distribuciones.
    
    Args:
        json_file_path (str): Ruta al archivo JSON
    
    Returns:
        dict: Diccionario con las estadísticas
    """
    
    # Verificar que el archivo existe
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"El archivo {json_file_path} no existe")
    
    # Leer el archivo JSON
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error al decodificar el JSON: {e}")
    except Exception as e:
        raise Exception(f"Error al leer el archivo: {e}")
    
    # Inicializar contadores
    total_datasets = 0
    total_distributions = 0
    format_counter = Counter()
    
    # Verificar estructura del JSON
    if 'result' not in data or 'items' not in data['result']:
        raise ValueError("Estructura JSON no válida. Se esperaba 'result.items'")
    
    items = data['result']['items']
    total_datasets = len(items)
    
    # Procesar cada dataset
    for item in items:
        # Verificar si tiene distribuciones
        if 'distribution' in item and item['distribution']:
            distributions = item['distribution']
            
            # Asegurar que distributions es una lista
            if not isinstance(distributions, list):
                distributions = [distributions]
            
            total_distributions += len(distributions)
            
            # Procesar cada distribución
            for dist in distributions:
                if 'format' in dist and dist['format']:
                    format_info = dist['format']
                    
                    # Extraer el valor del formato
                    if isinstance(format_info, dict):
                        if 'value' in format_info:
                            format_value = format_info['value']
                        else:
                            # Si no hay 'value', usar toda la información disponible
                            format_value = str(format_info)
                    else:
                        format_value = str(format_info)
                    
                    format_counter[format_value] += 1
                else:
                    # Distribución sin formato especificado
                    format_counter['Sin formato especificado'] += 1
    
    # Crear el diccionario de resultados
    results = {
        'total_datasets': total_datasets,
        'total_distributions': total_distributions,
        'formats': dict(format_counter),
        'format_count': len(format_counter)
    }
    
    return results

def print_statistics(stats):
    """
    Imprime las estadísticas de manera formateada
    
    Args:
        stats (dict): Diccionario con las estadísticas
    """
    print("=" * 60)
    print("ESTADÍSTICAS DE DATASETS Y FORMATOS")
    print("=" * 60)
    print(f"Total de datasets: {stats['total_datasets']}")
    print(f"Total de distribuciones: {stats['total_distributions']}")
    print(f"Número de formatos diferentes: {stats['format_count']}")
    print("\n" + "-" * 40)
    print("DISTRIBUCIÓN POR FORMATO:")
    print("-" * 40)
    
    # Ordenar por número de ocurrencias (descendente)
    sorted_formats = sorted(stats['formats'].items(), key=lambda x: x[1], reverse=True)
    
    for format_name, count in sorted_formats:
        percentage = (count / stats['total_distributions']) * 100
        print(f"{format_name:<40} | {count:>6} ({percentage:.1f}%)")
    
    print("=" * 60)

def main():
    """
    Función principal para ejecutar el análisis
    """
    # Solicitar la ruta del archivo al usuario
    file_path = input("Ingrese la ruta del archivo JSON: ").strip()
    
    # Si no se proporciona ruta, usar una por defecto
    if not file_path:
        file_path = "catalogo.json"
        print(f"Usando archivo por defecto: {file_path}")
    
    try:
        # Analizar el archivo
        print(f"\nAnalizando archivo: {file_path}")
        stats = analyze_dataset_formats(file_path)
        
        # Mostrar resultados
        print_statistics(stats)
        
        # Guardar resultados en un archivo opcional
        save_option = input("\n¿Desea guardar los resultados en un archivo? (s/n): ").strip().lower()
        if save_option in ['s', 'si', 'yes', 'y']:
            output_file = input("Nombre del archivo de salida (por defecto: estadisticas_formatos.json): ").strip()
            if not output_file:
                output_file = "estadisticas_formatos.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            print(f"Resultados guardados en: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

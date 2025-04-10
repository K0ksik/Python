import random
import time
import multiprocessing
import psutil
import logging
import threading
from collections import Counter
from typing import List, Tuple, Dict
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class ListAnalyzer:
    def __init__(self, data: List[int]):
        self.data = data
        self.sorted_data = sorted(data)
        self.length = len(data)
        self.counter = Counter(data)

    def most_common_element(self) -> Tuple[int, int]:
        element, count = self.counter.most_common(1)[0]
        return element, count

    def least_common_element(self) -> Tuple[int, int]:
        element, count = self.counter.most_common()[-1]
        return element, count

    def sum_of_elements(self) -> int:
        return sum(self.data)

    def average(self) -> float:
        return self.sum_of_elements() / self.length if self.length > 0 else 0

    def median(self) -> float:
        if self.length == 0:
            return 0
        if self.length % 2 == 1:
            return self.sorted_data[self.length // 2]
        else:
            return (self.sorted_data[self.length // 2 - 1] + self.sorted_data[self.length // 2]) / 2

def save_results_in_thread(results: Dict, filename: str):
    def save():
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
            logging.info(f"Результаты сохранены в {filename}")
        except Exception as e:
            logging.error(f"Ошибка сохранения в {filename}: {str(e)}")
    
    thread = threading.Thread(target=save, daemon=True)
    thread.start()
    return thread

def worker_task(data: List[int], task_type: str, return_dict: Dict, lock):
    try:
        analyzer = ListAnalyzer(data)
        task_names = {
            "most_common": ("Наиболее частый элемент", analyzer.most_common_element),
            "least_common": ("Наименее частый элемент", analyzer.least_common_element),
            "sum": ("Сумма элементов", analyzer.sum_of_elements),
            "average": ("Среднее арифметическое", analyzer.average),
            "median": ("Медиана", analyzer.median)
        }
        
        if task_type not in task_names:
            logging.error(f"Неизвестный тип задачи: {task_type}")
            return

        name, method = task_names[task_type]
        result = method()
        
        with lock:
            return_dict[task_type] = result
        
        
        save_thread = save_results_in_thread(
            {task_type: result}, 
            f"result_{task_type}.json"
        )
        save_thread.join() 
        
        logging.info(f"Задача '{name}' завершена. Результат: {result}")
    except Exception as e:
        logging.error(f"Ошибка в задаче {task_type}: {str(e)}")

class AnalysisManager:
    def __init__(self):
        self.cpu_cores = psutil.cpu_count(logical=True)
        self.cpu_percent = psutil.cpu_percent(interval=1)
        self.max_processes = self._calculate_available_processes()
        self.manager = multiprocessing.Manager()
        self.results = self.manager.dict()
        self.lock = self.manager.Lock()

    def _calculate_available_processes(self) -> int:
        used_cores = max(1, int(self.cpu_cores * (self.cpu_percent / 100)))
        available_cores = max(1, self.cpu_cores - used_cores)
        return min(self.cpu_cores, available_cores)

    def generate_random_list(self, size: int) -> List[int]:
        return [random.randint(1, 100) for _ in range(size)]

    def run_analysis(self, data_size: int, process_count: int = None):
        if process_count is None:
            process_count = self.max_processes
        else:
            process_count = min(max(1, process_count), self.max_processes)

        data = self.generate_random_list(data_size)
        logging.info(f"Сгенерирован список из {data_size} элементов")
        logging.info(f"Используется {process_count} из {self.max_processes} доступных процессов")

        tasks = [
            "most_common",
            "least_common", 
            "sum",
            "average",
            "median"
        ]

        processes = []
        for i in range(process_count):
            task_type = tasks[i % len(tasks)]
            p = multiprocessing.Process(
                target=worker_task,
                args=(data, task_type, self.results, self.lock),
                name=f"Процесс-{i+1}-{task_type}"
            )
            processes.append(p)
            p.start()
            logging.info(f"Запущен {p.name}")

        for p in processes:
            p.join()

        save_results_in_thread(dict(self.results), "final_results.json")
        logging.info("Все задачи выполнены")

    def shutdown(self):
        logging.info("Анализ завершен. Все результаты сохранены")

def main():
    try:
        manager = AnalysisManager()
        
        print(f"\nДоступно ядер процессора: {manager.cpu_cores}")
        print(f"Текущая загрузка CPU: {manager.cpu_percent:.1f}%")
        print(f"Доступно процессов для анализа: {manager.max_processes}")

        while True:
            try:
                data_size = int(input("Введите размер списка для анализа (минимум 10): "))
                if data_size >= 10:
                    break
                print("Размер списка должен быть не менее 10")
            except ValueError:
                print("Ошибка: введите целое число")

        while True:
            try:
                process_count = int(
                    input(f"Введите количество процессов (1-{manager.max_processes}): ")
                )
                if 1 <= process_count <= manager.max_processes:
                    break
                print(f"Введите число от 1 до {manager.max_processes}")
            except ValueError:
                print("Ошибка: введите целое число")

        start_time = time.time()
        manager.run_analysis(data_size, process_count)
        end_time = time.time()

        print(f"\nАнализ завершен за {end_time - start_time:.2f} секунд")
        print("Результаты сохранены в файлах result_*.json и final_results.json")
        
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")
    finally:
        manager.shutdown()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
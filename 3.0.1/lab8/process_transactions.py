# process_transactions.py
import asyncio
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Tuple

class TransactionProcessor:
    def __init__(self, threshold: float = 5000.0):
        self.threshold = threshold  # Порог для предупреждения о превышении расходов
        self.category_totals = defaultdict(float)
        self.category_transactions = defaultdict(list)
    
    async def read_transactions_file(self, file_path: Path):
        """Асинхронное чтение файла с транзакциями"""
        # В реальном приложении здесь может быть асинхронное чтение файла
        # Для простоты используем обычное чтение, но в async контексте
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    async def process_transaction(self, transaction: Dict[str, Any]):
        """Обработка одной транзакции"""
        category = transaction['category']
        amount = transaction['amount']
        
        # Группировка по категориям
        self.category_totals[category] += amount
        self.category_transactions[category].append(transaction)
        
        # Проверка на превышение порога
        if self.category_totals[category] > self.threshold:
            await self.notify_threshold_exceeded(category)
    
    async def notify_threshold_exceeded(self, category: str):
        """Уведомление о превышении расходов"""
        print(f"⚠️  ВНИМАНИЕ: Превышен порог расходов в категории '{category}'!")
        print(f"   Текущая сумма: ${self.category_totals[category]:.2f}")
        print(f"   Установленный порог: ${self.threshold:.2f}")
        print("-" * 50)
    
    async def process_transaction_stream(self, transactions: List[Dict[str, Any]]):
        """Обработка потока транзакций"""
        tasks = []
        
        for transaction in transactions:
            # Создаем задачу для обработки каждой транзакции
            task = asyncio.create_task(self.process_transaction(transaction))
            tasks.append(task)
        
        # Ждем завершения всех задач
        await asyncio.gather(*tasks)
    
    def get_category_summary(self) -> List[Tuple[str, float, int]]:
        """Получение сводки по категориям"""
        summary = []
        for category, total in self.category_totals.items():
            count = len(self.category_transactions[category])
            summary.append((category, total, count))
        
        # Сортировка по убыванию суммы
        return sorted(summary, key=lambda x: x[1], reverse=True)
    
    def print_summary(self):
        """Вывод сводки в консоль"""
        print("\n" + "=" * 60)
        print("СВОДКА ПО КАТЕГОРИЯМ")
        print("=" * 60)
        
        summary = self.get_category_summary()
        
        for category, total, count in summary:
            avg = total / count if count > 0 else 0
            print(f"{category:15} | ${total:10.2f} | {count:3} транзакций | "
                  f"Среднее: ${avg:.2f}")
        
        print("=" * 60)
        print(f"Всего транзакций: {sum(len(t) for t in self.category_transactions.values())}")
        print(f"Общая сумма: ${sum(self.category_totals.values()):.2f}")

async def main():
    if len(sys.argv) != 2:
        print("Использование: python process_transactions.py <путь_к_файлу_или_папке>")
        return
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"Ошибка: Путь '{input_path}' не существует")
        return
    
    processor = TransactionProcessor(threshold=3000.0)  # Порог $3000
    
    # Определяем, что обрабатывать: файл или папку
    if input_path.is_file():
        files_to_process = [input_path]
    else:
        files_to_process = list(input_path.glob("*.json"))
    
    print(f"Обработка {len(files_to_process)} файлов...")
    print("=" * 50)
    
    for file_path in files_to_process:
        print(f"📁 Обработка файла: {file_path.name}")
        
        try:
            # Чтение транзакций из файла
            transactions = await processor.read_transactions_file(file_path)
            
            # Обработка потока транзакций
            await processor.process_transaction_stream(transactions)
            
            print(f"✓ Обработано {len(transactions)} транзакций")
            
        except Exception as e:
            print(f"✗ Ошибка при обработке файла {file_path}: {e}")
    
    # Вывод финальной сводки
    processor.print_summary()
    
    # Дополнительно: сохранение результатов в файл
    await save_results_to_file(processor)

async def save_results_to_file(processor: TransactionProcessor):
    """Сохранение результатов обработки в файл"""
    results = {
        "threshold": processor.threshold,
        "category_summary": [
            {
                "category": category,
                "total_amount": total,
                "transaction_count": len(processor.category_transactions[category]),
                "average_amount": total / len(processor.category_transactions[category])
            }
            for category, total in processor.category_totals.items()
        ],
        "total_transactions": sum(len(t) for t in processor.category_transactions.values()),
        "total_amount": sum(processor.category_totals.values())
    }
    
    output_file = Path("processing_results.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Результаты сохранены в файл: {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
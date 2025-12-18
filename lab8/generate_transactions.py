# generate_transactions.py
import asyncio
import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

class TransactionGenerator:
    def __init__(self):
        self.categories = [
            "Food", "Transport", "Entertainment", "Shopping",
            "Utilities", "Healthcare", "Education", "Travel"
        ]
        self.output_dir = Path("transactions")
        self.output_dir.mkdir(exist_ok=True)
        self.file_counter = 0
    
    async def generate_transaction(self) -> Dict[str, Any]:
        """Генерация одной транзакции"""
        timestamp = datetime.now() - timedelta(
            minutes=random.randint(0, 10080)  # До 7 дней назад
        )
        
        return {
            "timestamp": timestamp.isoformat(),
            "category": random.choice(self.categories),
            "amount": round(random.uniform(10, 1000), 2)
        }
    
    async def generate_transaction_stream(self, total_transactions: int):
        """Генерация потока транзакций"""
        transaction_count = 0
        batch = []
        
        while transaction_count < total_transactions:
            # Генерация транзакции
            transaction = await self.generate_transaction()
            batch.append(transaction)
            transaction_count += 1
            
            # Обработка батча по 10 записей
            if len(batch) >= 10:
                await self.process_batch(batch)
                batch = []
            
            # Небольшая задержка для имитации реального потока
            await asyncio.sleep(0.01)
        
        # Обработка оставшихся транзакций
        if batch:
            await self.process_batch(batch)
    
    async def process_batch(self, batch: List[Dict[str, Any]]):
        """Обработка батча транзакций"""
        # Сохранение в файл
        filename = self.output_dir / f"transactions_{self.file_counter:03d}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(batch, f, indent=2, ensure_ascii=False)
        
        # Вывод информации в консоль
        total_amount = sum(t['amount'] for t in batch)
        print(f"✓ Файл {filename} сохранен")
        print(f"  Количество транзакций: {len(batch)}")
        print(f"  Общая сумма в батче: ${total_amount:.2f}")
        print(f"  Категории: {set(t['category'] for t in batch)}")
        print("-" * 50)
        
        self.file_counter += 1

async def main():
    if len(sys.argv) != 2:
        print("Использование: python generate_transactions.py <количество_транзакций>")
        return
    
    try:
        total_transactions = int(sys.argv[1])
        if total_transactions <= 0:
            print("Количество транзакций должно быть положительным числом")
            return
    except ValueError:
        print("Пожалуйста, укажите целое число")
        return
    
    print(f"Генерация {total_transactions} транзакций...")
    print("=" * 50)
    
    generator = TransactionGenerator()
    await generator.generate_transaction_stream(total_transactions)
    
    print("\n" + "=" * 50)
    print(f"Генерация завершена! Создано {generator.file_counter} файлов")
    
    # Создание общего JSON файла со всеми транзакциями
    await create_combined_json(generator.output_dir)

async def create_combined_json(directory: Path):
    """Создание общего JSON файла со всеми транзакциями"""
    all_transactions = []
    
    for file_path in directory.glob("*.json"):
        with open(file_path, 'r', encoding='utf-8') as f:
            transactions = json.load(f)
            all_transactions.extend(transactions)
    
    combined_file = directory / "all_transactions.json"
    with open(combined_file, 'w', encoding='utf-8') as f:
        json.dump(all_transactions, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Создан общий файл: {combined_file}")
    print(f"  Всего транзакций: {len(all_transactions)}")

if __name__ == "__main__":
    asyncio.run(main())
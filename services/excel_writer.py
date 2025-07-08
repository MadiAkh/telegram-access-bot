from openpyxl import Workbook
import asyncio
from services.api_client import get_avr_data
import datetime

async def save_avr_to_excel(file_path: str = "C:/Users/22671/Desktop/PROJECTS/bot_1C/output.xlsx"):
    # print("✅ Функция save_avr_to_excel вызвана")
    data = await get_avr_data()
    documents = data.get("документы", [])

    if not documents:
        # print("⚠️ Нет данных для записи.")
        return
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Данные из 1С"

    ws.append(["Дата составления", 
               "Состояние", 
               "Контрагент",
               "Итого стоимость с учетом косвенных налогов",
               "Дата выполнения работ"
               
    ])

    ws.column_dimensions['A'].width=20
    ws.column_dimensions['B'].width=20
    ws.column_dimensions['C'].width=90
    ws.column_dimensions['D'].width=45
    ws.column_dimensions['E'].width=25

    for doc in documents:
        date_sostavleniya = doc.get("датаСоставления", "")
        if date_sostavleniya:
            date_obj = datetime.datetime.strptime(date_sostavleniya, "%Y-%m-%d")
            date_sostavleniya_formatted = date_obj.strftime("%d.%m.%Y")
        else:
            date_sostavleniya_formatted = ""

        date_vypolneniya = doc.get("датаВыполненияРабот", "")
        if date_vypolneniya:
            date_obj = datetime.datetime.strptime(date_sostavleniya, "%Y-%m-%d")
            date_vypolneniya_formatted = date_obj.strftime("%d.%m.%Y")
        else:
            date_vypolneniya_formatted = ""


        total_cost = doc.get("итогоСтоимостьСУчетомКосвенныхНалогов", "")
    
        ws.append([
            date_sostavleniya_formatted,
            doc.get("статус", ""),
            doc.get("контрагент", ""),
            total_cost,
            date_vypolneniya_formatted
        ])
    # print("💾 Сохраняем файл...")
    wb.save(file_path)
    # print(f"✅ Данные сохранены в файл: {file_path}")

if __name__ == "__main__":
    asyncio.run(save_avr_to_excel())

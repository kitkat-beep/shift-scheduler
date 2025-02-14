import pandas as pd
import streamlit as st

# Функция для создания графика
def create_schedule(masters, operators, machine1_operators, machine2_operators, days):
    # Списки для хранения графика
    schedule = {
        "День": [],
        "Смена": [],
        "Мастер смены": [],
        "Аппаратчики": [],
        "Машина 1 (2 человека)": [],
        "Машина 2 (3 человека)": []
    }

    # Цикл по дням
    for day in range(1, days + 1):
        # Определение смены
        shift_type = "Ночная" if (day % 4 == 1 or day % 4 == 2) else "Дневная"
        
        # Выбор мастера смены
        master = masters[(day - 1) % len(masters)]
        
        # Распределение аппаратчиков
        operators_shift = operators[(day - 1) % len(operators): (day - 1) % len(operators) + 6]
        if len(operators_shift) < 6:
            operators_shift += operators[:6 - len(operators_shift)]
        
        # Распределение операторов для машин
        machine1 = machine1_operators[(day - 1) % len(machine1_operators): (day - 1) % len(machine1_operators) + 2]
        if len(machine1) < 2:
            machine1 += machine1_operators[:2 - len(machine1)]
        
        machine2 = machine2_operators[(day - 1) % len(machine2_operators): (day - 1) % len(machine2_operators) + 3]
        if len(machine2) < 3:
            machine2 += machine2_operators[:3 - len(machine2)]
        
        # Запись в график
        schedule["День"].append(day)
        schedule["Смена"].append(shift_type)
        schedule["Мастер смены"].append(master)
        schedule["Аппаратчики"].append(", ".join(operators_shift))
        schedule["Машина 1 (2 человека)"].append(", ".join(machine1))
        schedule["Машина 2 (3 человека)"].append(", ".join(machine2))
    
    return pd.DataFrame(schedule)

# Веб-интерфейс с использованием Streamlit
def main():
    st.title("График смен для персонала")

    # Ввод данных
    st.sidebar.header("Введите данные")
    days = st.sidebar.number_input("Количество дней для графика", min_value=1, value=28)
    
    masters = st.sidebar.text_area("Мастера смен (через запятую)", "Мастер 1, Мастер 2, Мастер 3, Мастер 4, Мастер 5").split(", ")
    operators = st.sidebar.text_area("Аппаратчики (через запятую)", "Оператор 1, Оператор 2, Оператор 3, Оператор 4, Оператор 5, Оператор 6, Оператор 7, Оператор 8, Оператор 9, Оператор 10, Оператор 11, Оператор 12, Оператор 13, Оператор 14, Оператор 15, Оператор 16, Оператор 17, Оператор 18").split(", ")
    machine1_operators = st.sidebar.text_area("Операторы для Машины 1 (через запятую)", "Оператор 1, Оператор 2, Оператор 3, Оператор 4").split(", ")
    machine2_operators = st.sidebar.text_area("Операторы для Машины 2 (через запятую)", "Оператор 5, Оператор 6, Оператор 7, Оператор 8, Оператор 9").split(", ")

    # Создание графика
    if st.sidebar.button("Создать график"):
        schedule_df = create_schedule(masters, operators, machine1_operators, machine2_operators, days)
        st.write("График смен:")
        st.dataframe(schedule_df)

        # Экспорт в CSV
        csv = schedule_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать график (CSV)",
            data=csv,
            file_name="schedule.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
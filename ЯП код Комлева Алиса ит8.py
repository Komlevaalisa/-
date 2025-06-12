class DominoNode:
    """Узел двусвязного списка для кости домино"""
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DominoList:
    """Двусвязный список для хранения ряда домино"""
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        """Добавление элемента в конец списка"""
        new_node = DominoNode(value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail # Устанавливаем связь с предыдущим элементом
            self.tail.next = new_node # Предыдущий элемент ссылается на новый
            self.tail = new_node # Новый элемент становится хвостом

    def to_list(self):
        """Преобразование списка в Python-список значений"""
        result = []
        current = self.head
        while current: # Проходим по всем узлам
            result.append(current.value)
            current = current.next
        return result

    def __str__(self):
        return ", ".join(self.to_list()) # Красивое строковое представление

    def copy(self):
        """Создать копию списка"""
        new_list = DominoList()
        current = self.head
        while current:
            new_list.append(current.value) # Добавляем значения в новый список
            current = current.next
        return new_list


class DominoSolver:
    """Основной класс для решения задачи"""
    def __init__(self, dominoes):
        self.dominoes = dominoes
        self.used = [False] * len(dominoes) # Отметки об использовании костей
        self.solution = None

    def is_valid_domino(self, domino):
        """Проверка корректности кости: длина 2, цифры от 0 до 6"""
        if len(domino) != 2:
            return False
        if not (domino[0].isdigit() and domino[1].isdigit()):
            return False
        if not (0 <= int(domino[0]) <= 6 and 0 <= int(domino[1]) <= 6):
            return False
        return True

    def validate_input(self):
        """Проверка всех костей"""
        if not self.dominoes:
            return False
        for d in self.dominoes:
            if not self.is_valid_domino(d):
                return False
        return True

    def can_connect(self, a, b, reverse=False):
        """
        Проверяет, можно ли соединить кость b после кости a.
        Если reverse=True, кость b рассматривается перевёрнутой.
        """
        if not reverse:
            return a[1] == b[0]
        else:
            return a[1] == b[1]

    def find_chain(self, current_list):
        """Рекурсивный поиск цепочки домино с backtracking"""
        if all(self.used): # Все кости использованы - решение найдено
            self.solution = current_list.copy()
            return True

        last_value = current_list.tail.value # Последняя кость в текущей цепочке
        for i, domino in enumerate(self.dominoes):
            if not self.used[i]:
                # Попытка добавить в обычном порядке
                if self.can_connect(last_value, domino):
                    self.used[i] = True
                    current_list.append(domino)
                    if self.find_chain(current_list):
                        return True
                    # Откат
                    current_list.tail = current_list.tail.prev
                    if current_list.tail:
                        current_list.tail.next = None
                    else:
                        current_list.head = None
                    self.used[i] = False
                # Попытка добавить перевёрнутую кость
                elif self.can_connect(last_value, domino, reverse=True):
                    self.used[i] = True
                    reversed_domino = domino[1] + domino[0]
                    current_list.append(reversed_domino)
                    if self.find_chain(current_list):
                        return True
                    # Откат
                    current_list.tail = current_list.tail.prev
                    if current_list.tail:
                        current_list.tail.next = None
                    else:
                        current_list.head = None
                    self.used[i] = False
        return False

    def solve(self):
        """Основной метод решения"""
        if not self.validate_input():
            return "некорректные входные данные"
        for i in range(len(self.dominoes)):
            self.used = [False] * len(self.dominoes)
            self.used[i] = True
            # Пробуем начать с кости в обычном порядке
            domino_list = DominoList()
            domino_list.append(self.dominoes[i])
            if self.find_chain(domino_list):
                return f"можно, {self.solution}"
            # Пробуем начать с кости в перевёрнутом порядке
            self.used[i] = False
            self.used[i] = True
            domino_list = DominoList()
            reversed_domino = self.dominoes[i][1] + self.dominoes[i][0]
            domino_list.append(reversed_domino)
            if self.find_chain(domino_list):
                return f"можно, {self.solution}"
        return "нельзя выложить в ряд"

def print_menu():
    """Выводит меню программы"""
    print("\n" + "=" * 50)
    print("МЕНЮ ПРОГРАММЫ ДОМИНО".center(50))
    print("=" * 50)
    print("1. Проверить возможность построения цепочки")
    print("2. Показать примеры ввода")
    print("3. О программе")
    print("4. Выход")
    print("=" * 50)

def show_examples():
    """Показывает примеры работы программы"""
    print("\nПримеры корректного ввода:")
    print("- 02, 04, 42 → можно, 04, 42, 20")
    print("- 11, 22, 33 → нельзя выложить в ряд")
    print("\nПримеры некорректного ввода:")
    print("- 31, 00, 13 → некорректные входные данные")
    print("- 7, 12, 34 → цифры должны быть от 0 до 6")
    print("- abc, 12 → должно быть две цифры")

def about_program():
    """Информация о программе"""
    print("\nПрограмма для проверки возможности выстроить")
    print("ряд из заданных костей домино по правилам:")
    print("- соседние кости должны соприкасаться одинаковыми числами")
    print("- кости можно переворачивать")

def main():
    print("\nДобро пожаловать в программу проверки домино!")
    print("Цифры на костях должны быть от 0 до 6 (включительно).")
    while True:
        print_menu()
        try:
            choice = input("Выберите пункт меню (1-4): ").strip()
            if choice == "1":
                input_str = input("\nВведите кости домино через запятую: ").strip()
                dominoes = [d.strip() for d in input_str.split(",") if d.strip()]
                solver = DominoSolver(dominoes)
                result = solver.solve()
                print("\nРезультат:", result)
                input("\nНажмите Enter чтобы продолжить...")
            elif choice == "2":
                show_examples()
                input("\nНажмите Enter чтобы продолжить...")
            elif choice == "3":
                about_program()
                input("\nНажмите Enter чтобы продолжить...")
            elif choice == "4":
                print("\nСпасибо за использование программы. До свидания!")
                break
            else:
                print("\nОшибка: выберите пункт меню от 1 до 4")
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            print("Пожалуйста, попробуйте еще раз.")
            input("Нажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    main()
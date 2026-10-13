#1
bugs = [
 {"id": 1, "title": "Не работает вход",
 "severity": "high", "status": "open"},
 {"id": 2, "title": "Опечатка на главной странице",
 "severity": "low", "status": "closed"},
 {"id": 3, "title": "Не сохраняется расписание",
 "severity": "high", "status": "open"},
 {"id": 4, "title": "Неверный цвет кнопки",
 "severity": "medium", "status": "open"}
]
def find_bug(bugs_list, bug_id):
    for bug in bugs_list:
        if bug["id"] == bug_id:
            return bug
    return None
#2
def filter_bugs(bugs_list, status, severity):
    norm_status = status.strip().lower()
    norm_severity = severity.strip().lower()
    valid_statys = {"open","in_progress","closed"}
    valid_severity = {"low","medium","high"}
    if norm_status not in valid_statys or norm_severity not in valid_severity:
        return[]
    result = []
    for bug in bugs_list:
        if bug["status"] == norm_status and bug["severity"] == norm_severity:
            result.append(bug)
    return result 
#3
def add_bug (bugs_list, title, severity):
    clean_title = title.strip()
    if len(clean_title) < 5:
        return None
    norm_severity = severity.strip().lower()
    if norm_severity not in {"low","medium","high"}:
        return None
    if not bugs_list:
        new_id = 1
    else:
        max_id = max(bug["id"] for  bug in bugs)
        new_id = max_id + 1
    new_bugs = {
        "id":new_id,
        "title": clean_title,
        "severity":norm_severity,
        "status": open
    }
    bugs_list.append(new_bugs)
    return new_id
#4
def change_status(bugs_list, bug_id, new_status):
    norm_status = new_status.strip().lower()
    valid_statys = {"open","in_progress","closed"}
    if norm_status not  in valid_statys:
        return "invalid_statys"
    bug = find_bug(bugs_list,bug_id)
    if bug is None:
        return "not_found"
    current_statys = bug["status"]
    allowed_transitions = {
        "open": {"in_progress"},
        "in_progress": {"open", "closed"},
        "closed": {"open"}
    }
    if norm_status not in allowed_transitions.get(current_statys, set()):
        return "forbidden"
    bug["status"] = norm_status
    return "updated"
#5
def build_report(bugs_list):
    total = len(bugs_list)
    by_status = {"open": 0, "in_progress": 0, "closed": 0}
    by_severity = {"low": 0, "medium": 0, "high": 0}
    unresolved_high = 0
    for bug in bugs_list:
        st = bug["status"]
        sev = bug["severity"]
        if st in by_status:
            by_status[st] += 1
        if sev in by_severity:
            by_severity[sev] += 1
        if sev == "high" and st != "closed":
            unresolved_high += 1
    return {
        "total": total,
        "by_status": by_status,
        "by_severity": by_severity,
        "unresolved_high": unresolved_high
    }
#6
def start_selected(bugs_list, ids):
    if not ids:
        return False
    if len(ids) != len(set(ids)):
        return False
    target_bugs = []
    for bug_id in ids:
        bug = find_bug(bugs_list, bug_id)
        if bug is None:
            return False
        if bug["status"] != "open":
            return False
        target_bugs.append(bug)
    for bug in target_bugs:
        bug["status"] = "in_progress"
    return True
def main():
    global bugs
    while True:
        print("\n--- Меню трекера ошибок ---")
        print("1. Показать все ошибки")
        print("2. Найти по ID")
        print("3. Отфильтровать")
        print("4. Добавить ошибку")
        print("5. Изменить статус")
        print("6. Показать отчёт")
        print("7. Назначить несколько ошибок в работу")
        print("0. Выход")
        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            for b in bugs:
                print(b)
        elif choice == "2":
            try:
                b_id = int(input("Введите ID ошибки: "))
                print(find_bug(bugs, b_id))
            except ValueError:
                print("Ошибка: ID должен быть целым числом.")
        elif choice == "3":
            st = input("Введите статус (open, in_progress, closed): ")
            sev = input("Введите серьёзность (low, medium, high): ")
            print(filter_bugs(bugs, st, sev))
        elif choice == "4":
            title = input("Введите название ошибки: ")
            sev = input("Введите серьёзность (low, medium, high): ")
            res = add_bug(bugs, title, sev)
            print(f"Результат: создан ID {res}" if res else "Ошибка добавления.")
        elif choice == "5":
            try:
                b_id = int(input("Введите ID ошибки: "))
                st = input("Введите новый статус: ")
                print("Результат:", change_status(bugs, b_id, st))
            except ValueError:
                print("Ошибка: введите корректные данные.")
        elif choice == "6":
            print(build_report(bugs))
        elif choice == "7px" or choice == "7":
            raw_ids = input("Введите ID через пробел: ").split()
            try:
                ids_list = [int(x) for x in raw_ids]
                print("Результат:", start_selected(bugs, ids_list))
            except ValueError:
                print("Ошибка: ID должны быть числами.")
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")
if __name__ == "__main__":
    main()
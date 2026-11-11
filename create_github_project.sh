#!/usr/bin/env bash
# Creates a GitHub Project with the 16-item Product Backlog.
# Requirements: gh (GitHub CLI) + jq, and:  gh auth refresh -s project
set -euo pipefail
OWNER="@me"
TITLE="Навчальний Sprint 1 — online-store"

PROJ=$(gh project create --owner "$OWNER" --title "$TITLE" --format json)
NUM=$(echo "$PROJ" | jq -r .number)
PID=$(echo "$PROJ" | jq -r .id)
echo "Created project #$NUM"

gh project field-create "$NUM" --owner "$OWNER" --name "Type" --data-type SINGLE_SELECT \
  --single-select-options "Feature,Defect,Refactoring,Test,Tech task,Improvement,Requirement" >/dev/null
gh project field-create "$NUM" --owner "$OWNER" --name "Priority" --data-type SINGLE_SELECT \
  --single-select-options "P1,P2,P3" >/dev/null
gh project field-create "$NUM" --owner "$OWNER" --name "Sprint" --data-type SINGLE_SELECT \
  --single-select-options "Sprint 1,Next" >/dev/null
gh project field-create "$NUM" --owner "$OWNER" --name "Estimate, год" --data-type NUMBER >/dev/null
gh project field-create "$NUM" --owner "$OWNER" --name "Origin" --data-type TEXT >/dev/null

FIELDS=$(gh project field-list "$NUM" --owner "$OWNER" --format json)
fid()  { echo "$FIELDS" | jq -r --arg n "$1" '.fields[]|select(.name==$n)|.id'; }
oid()  { echo "$FIELDS" | jq -r --arg n "$1" --arg o "$2" '.fields[]|select(.name==$n)|.options[]|select(.name==$o)|.id'; }

# ID | Title | Type | Priority | Estimate | Sprint | Origin
while IFS='|' read -r ID NAME TYPE PRIO EST SPR ORIGIN; do
  [ -z "$ID" ] && continue
  ITEM=$(gh project item-create "$NUM" --owner "$OWNER" --title "$ID. $NAME" --format json | jq -r .id)
  gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$(fid Type)"     --single-select-option-id "$(oid Type "$TYPE")"     >/dev/null
  gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$(fid Priority)" --single-select-option-id "$(oid Priority "$PRIO")" >/dev/null
  gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$(fid "Estimate, год")" --number "$EST" >/dev/null
  gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$(fid Origin)"   --text "$ORIGIN" >/dev/null
  if [ -n "$SPR" ]; then
    gh project item-edit --id "$ITEM" --project-id "$PID" --field-id "$(fid Sprint)" --single-select-option-id "$(oid Sprint "$SPR")" >/dev/null
  fi
  echo "Added $ID"
done <<'DATA'
PB-01|Рефакторинг order_calc.py без зміни поведінки|Refactoring|P1|4|Sprint 1|ЛР № 7
PB-02|Unit-тести валідації кількості (1–100)|Test|P2|2|Sprint 1|ЛР № 8
PB-03|Unit-тести розрахунку вартості замовлення|Test|P2|3|Sprint 1|ЛР № 8
PB-04|Налаштувати Ruff і виконати статичний аналіз|Tech task|P2|2|Sprint 1|ЛР № 9
PB-05|Усунути F821: невизначене ім’я vip_rate|Defect|P1|1|Sprint 1|ЛР № 9
PB-06|Скоротити довгі рядки docstring (E501)|Tech task|P3|1|Sprint 1|ЛР № 9
PB-07|Замінити прапорець bonus_enabled == 1 на булеве значення|Improvement|P3|2||ЛР № 7, review
PB-08|Прибрати порівняння is_active == True (E712)|Improvement|P3|1||ЛР № 9
PB-09|Визначити правило VIP-знижки (відсоток)|Requirement|P2|1||ЛР № 9
PB-10|Реєстрація користувача|Feature|P2|5||Функціональний backlog
PB-11|Каталог товарів із пошуком|Feature|P2|6||Функціональний backlog
PB-12|Кошик: додавання й видалення позицій|Feature|P1|6||Функціональний backlog
PB-13|Підключити is_valid_quantity до кошика|Feature|P2|3||Функціональний backlog
PB-14|Оформлення замовлення|Feature|P1|8||Функціональний backlog
PB-15|Історія замовлень|Feature|P3|5||Функціональний backlog
PB-16|Запуск тестів і Ruff у GitHub Actions|Tech task|P3|3||Технічний борг
DATA
echo "Done. Open: gh project view $NUM --owner $OWNER --web"

records = [
    {"id": "EQ-001", "status": "completed"},
    {"id": "EQ-002", "status": "pending"},
    {"id": "EQ-003", "status": "processing"},
   {"id": "EQ-004", "status": "waiting"},
    {"id": "EQ-005",},
    {"status": "pending"}
]

def validate_record(record):
    if "id" not in record:
        return False, "缺少id"

    if "status" not in record:
        return False, "缺少status"
        
    if not isinstance(record["id"], str):
        return False, "id必須是字串"
        
    if not isinstance(record["status"], str):
        return False, "status必須是字串"

    if record["id"].strip() == "":
        return False, "id不可為空白"
        
    if record["status"].strip() == "":
        return False, "status不可為空白"
    
    return True, None
    
def find_record_by_id(records, target_id):
    for record in records:
        if record.get("id") == target_id:
            return record

    return None
def update_record_status(records, target_id, new_status):
    record = find_record_by_id(records, target_id)

    if record is None:
        return False, "查無此設備紀錄"

    allowed_statuses = ["pending", "processing", "completed"]

    if new_status not in allowed_statuses:
        return False, "狀態值不在允許範圍內"

    record["status"] = new_status
    return True, None
    
def search_record(records):
    target_id = input("請輸入設備ID：").strip()

    if target_id == "":
        print("設備ID不可為空白")
        return

    record = find_record_by_id(records, target_id)

    if record is None:
        print("查無此設備紀錄")
        return

    print("查詢結果：")
    print(f"設備ID：{record['id']}")
    print(f"狀態：{record.get('status', '未提供')}")
    
def classify_records(records):
    pending_records = []
    processing_records = []
    completed_records = []
    unknown_records = []

    for record in records:
        is_valid, error_reason = validate_record(record)

        if not is_valid:
            record["error"] = error_reason
            unknown_records.append(record)
            continue

        status = record["status"]

        if status == "pending":
            pending_records.append(record)
        elif status == "processing":
            processing_records.append(record)
        elif status == "completed":
            completed_records.append(record)
        else:
            record["error"] = "狀態值不在分類規則內"
            unknown_records.append(record)

    return (
        pending_records,
        processing_records,
        completed_records,
        unknown_records,
    )


def create_summary(pending, processing, completed, unknown):
    total = (
        len(pending)
        + len(processing)
        + len(completed)
        + len(unknown)
    )

    if total > 0:
        completion_rate = len(completed) / total * 100
    else:
        completion_rate = 0

    return {
        "總紀錄數": total,
        "待處理數量": len(pending),
        "處理中數量": len(processing),
        "已完成數量": len(completed),
        "未知狀態數量": len(unknown),
        "完成率": f"{completion_rate:.1f}%",
    }
def validate_v01(summary):
    assert summary["總紀錄數"] == 6
    assert summary["待處理數量"] == 1
    assert summary["處理中數量"] == 1
    assert summary["已完成數量"] == 1
    assert summary["未知狀態數量"] == 3
    assert summary["完成率"] == "16.7%"

def display_summary(summary, unknown):
    print("總紀錄數：", summary["總紀錄數"])
    print("待處理數量：", summary["待處理數量"])
    print("處理中數量：", summary["處理中數量"])
    print("已完成數量：", summary["已完成數量"])
    print("未知狀態數量：", summary["未知狀態數量"])
    print("完成率：", summary["完成率"])

    if len(unknown) == 0:
        print("資料檢查通過")
    else:
        for record in unknown:
            record_id = record.get("id", "未提供")
            status = record.get("status", "未提供")
            error_reason = record.get(
                "error",
                "狀態值不在分類規則內"
            )

            print(
                "未知狀態：",
                record_id,
                status,
                error_reason
            )

        print("警告：發現未知狀態，請檢查資料")

def create_action_message(summary):
    if summary["未知狀態數量"] > 0:
        return "優先處理：檢查未知狀態"

    elif summary["處理中數量"] > 0:
        return "優先處理：追蹤處理中紀錄"

    elif summary["待處理數量"] > 0:
        return "下一步：開始處理待處理紀錄"

    else:
        return "目前沒有待處理工作"
        
def run_v01_test():
    pending, processing, completed, unknown = classify_records(records)
    summary = create_summary(
        pending,
        processing,
        completed,
        unknown,
    )
    validate_v01(summary)
    print("v0.1 基準驗收：PASS")   
     
def run_detail_test():
    pending, processing, completed, unknown = classify_records(records)

    actual_errors = [record["error"] for record in unknown]

    expected_errors = [
        "狀態值不在分類規則內",
        "缺少status",
        "缺少id",
    ]

    assert actual_errors == expected_errors, "未知原因不符合預期"

    summary = create_summary(
        pending, processing, completed, unknown
    )

    assert (
        create_action_message(summary)
        == "優先處理：檢查未知狀態"
    ), "優先處理提示不符合預期"

    print("未知原因與處理提示驗收：PASS")    
    
def display_pending(pending):
    if len(pending) == 0:
        print("目前沒有待處理紀錄")
        return

    print("待處理紀錄：")

    for record in pending:
        print(record["id"])
        
def display_processing(processing):
    if len(processing) == 0:
        print("目前沒有處理中紀錄")
        return

    print("處理中紀錄：")

    for record in processing:
        print(record["id"])
        
def display_completed(completed):
    if len(completed) == 0:
        print("目前沒有已完成紀錄")
        return

    print("已完成紀錄：")

    for record in completed:
        print(record["id"])
        
def update_record_interactively(records):
    target_id = input(
        "請輸入要更新的設備ID（直接Enter略過）："
    ).strip()

    if target_id == "":
        print("已略過狀態更新")
        return

    new_status = input(
        "請輸入新狀態（pending／processing／completed）："
    ).strip()

    success, error_message = update_record_status(
        records,
        target_id,
        new_status
    )

    if not success:
        print(f"更新失敗：{error_message}")
        return

    print(f"更新成功：{target_id} -> {new_status}")  
    
def add_record(records, new_id, new_status):
    new_record = {
        "id": new_id,
        "status": new_status
    }

    is_valid, error_reason = validate_record(new_record)

    if not is_valid:
        return False, error_reason

    if find_record_by_id(records, new_id) is not None:
        return False, "設備ID已存在"

    allowed_statuses = ["pending", "processing", "completed"]

    if new_status not in allowed_statuses:
        return False, "狀態值不在允許範圍內"

    records.append(new_record)
    return True, None
    
def add_record_interactively(records):
    new_id = input("請輸入新設備ID：").strip()

    new_status = input(
        "請輸入狀態（pending／processing／completed）："
    ).strip()

    success, error_reason = add_record(
        records,
        new_id,
        new_status
    )

    if not success:
        print(f"新增失敗：{error_reason}")
        return

    print(f"新增成功：{new_id} -> {new_status}")
    
def show_menu():
    print("\n設備異常紀錄整理器")
    print("1. 顯示紀錄摘要")
    print("2. 查詢設備")
    print("3. 更新設備狀態")
    print("4. 新增設備紀錄")
    print("0. 結束程式")

    return input("請選擇功能：").strip()
    
def display_all_records(records):
    pending, processing, completed, unknown = classify_records(records)

    summary = create_summary(
        pending,
        processing,
        completed,
        unknown,
    )

    display_summary(summary, unknown)
    display_pending(pending)
    display_processing(processing)
    display_completed(completed)

    action_message = create_action_message(summary)
    print(action_message)
    
def main():
    while True:
        choice = show_menu()

        if choice == "1":
            display_all_records(records)
        elif choice == "2":
            search_record(records)
        elif choice == "3":
            update_record_interactively(records)
        elif choice == "4":
            add_record_interactively(records)
        elif choice == "0":
            print("程式已結束")
            break
        else:
            print("無效選項，請重新輸入")
  
if __name__ == "__main__":
    main()
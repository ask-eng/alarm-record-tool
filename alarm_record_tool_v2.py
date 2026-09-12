records = [
    {"id": "EQ-001", "status": "completed"},
    {"id": "EQ-002", "status": "pending"},
    {"id": "EQ-003", "status": "processing"},
    {"id": "EQ-004", "status": "waiting"},
    {"id": "EQ-005"},
    {"status": "pending"}
]

def validate_record(record):
    if "id" not in record:
        return False, "缺少id"

    if "status" not in record:
        return False, "缺少status"

    return True, None
    
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
        "完成率": str(round(completion_rate, 1)) + "%",
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
    
def main():
    pending, processing, completed, unknown = classify_records(records)
    summary = create_summary(
        pending,
        processing,
        completed,
        unknown,
    )
    display_summary(summary, unknown)
    action_message =             create_action_message(summary)
    print(action_message)
        
if __name__ == "__main__":
    main()
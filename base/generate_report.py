import json

def generate_quiz_report(json_file):
    """
    生成測驗轉換報告
    """
    
    with open(json_file, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    
    questions = quiz_data["quiz"]["questions"]
    
    print("=" * 60)
    print("📊 測驗轉換完成報告")
    print("=" * 60)
    
    # 基本統計
    total_questions = len(questions)
    single_choice = [q for q in questions if q["type"] == "single_choice"]
    multiple_choice = [q for q in questions if q["type"] == "multiple_choice"]
    
    print(f"📝 總題數：{total_questions}")
    print(f"🔘 單選題：{len(single_choice)} 道 ({len(single_choice)/total_questions*100:.1f}%)")
    print(f"☑️  多選題：{len(multiple_choice)} 道 ({len(multiple_choice)/total_questions*100:.1f}%)")
    
    # 多選題詳細分析
    if multiple_choice:
        print(f"\n📋 多選題詳細分析：")
        for q in multiple_choice:
            correct_count = len(q["correct_answers"])
            total_options = len(q["options"])
            print(f"  題目 {q['id']}: {correct_count}/{total_options} 個正確答案")
    
    # JSON 結構說明
    print(f"\n📄 JSON 檔案結構：")
    print(f"├── quiz")
    print(f"│   ├── title: \"{quiz_data['quiz']['title']}\"")
    print(f"│   ├── description: \"{quiz_data['quiz']['description']}\"")
    print(f"│   └── questions: 陣列包含 {total_questions} 個題目")
    print(f"│       ├── 單選題欄位: id, question, options, correct_answer, type")
    print(f"│       └── 多選題欄位: id, question, options, correct_answers, type")
    
    print(f"\n✅ 轉換成功！檔案已儲存為：{json_file}")
    print("=" * 60)

# 執行報告
if __name__ == "__main__":
    generate_quiz_report("quiz_complete.json")

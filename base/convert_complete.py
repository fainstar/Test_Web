import json
import re

def parse_quiz_data_with_multiple_choice(input_file, output_file):
    """
    將測驗文件轉換為JSON格式，支援單選和多選題
    - @ 標記正確答案
    - ! 分隔每一題
    - "請選取適用的所有答案" 表示多選題
    - "請只選取一個答案" 表示單選題
    """
    
    # 讀取原始檔案
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 用 ! 分割成各個題目
    questions_raw = content.split('!')
    
    quiz_data = {
        "quiz": {
            "title": "機器學習與AI服務測驗",
            "description": "關於機器學習概念和Azure AI服務的測驗題目",
            "questions": []
        }
    }
    
    question_number = 1
    single_choice_count = 0
    multiple_choice_count = 0
    
    for question_block in questions_raw:
        question_block = question_block.strip()
        
        # 跳過空白區塊
        if not question_block:
            continue
        
        # 分割成行
        lines = [line.strip() for line in question_block.split('\n') if line.strip()]
        
        if len(lines) < 2:
            continue
        
        # 判斷題目類型
        is_multiple_choice = any("請選取適用的所有答案" in line for line in lines)
        is_single_choice = any("請只選取一個答案" in line for line in lines)
        
        if not (is_multiple_choice or is_single_choice):
            continue  # 跳過無法識別類型的題目
        
        # 提取題目文字
        question_text = ""
        options = []
        correct_answers = []  # 多選題可能有多個正確答案
        
        # 找到題目文字的結束位置
        question_end_idx = 0
        for i, line in enumerate(lines):
            if "請選取適用的所有答案" in line or "請只選取一個答案" in line:
                question_end_idx = i
                break
        
        # 組合題目文字
        if question_end_idx > 0:
            question_text = " ".join(lines[:question_end_idx])
        else:
            # 如果沒找到標準結尾，假設前面幾行是題目
            question_text = " ".join(lines[:max(1, len(lines)//2)])
        
        # 提取選項（在題目之後的部分）
        for line in lines[question_end_idx+1:]:
            # 跳過空行和說明文字
            if not line or "請選取適用的所有答案" in line or "請只選取一個答案" in line:
                continue
            
            # 檢查是否為正確答案（以@開頭）
            if line.startswith('@'):
                answer_text = line[1:].strip()  # 移除@符號
                correct_answers.append(answer_text)
                options.append(answer_text)
            else:
                options.append(line)
        
        # 如果成功解析出題目和選項，則加入到結果中
        if question_text and options and correct_answers:
            if is_multiple_choice:
                question_data = {
                    "id": question_number,
                    "question": question_text,
                    "options": options,
                    "correct_answers": correct_answers,  # 多選題用陣列
                    "type": "multiple_choice"
                }
                multiple_choice_count += 1
            else:  # 單選題
                question_data = {
                    "id": question_number,
                    "question": question_text,
                    "options": options,
                    "correct_answer": correct_answers[0],  # 單選題只有一個答案
                    "type": "single_choice"
                }
                single_choice_count += 1
            
            quiz_data["quiz"]["questions"].append(question_data)
            question_number += 1
    
    # 寫入JSON檔案
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
    
    print(f"轉換完成！")
    print(f"總共處理了 {len(quiz_data['quiz']['questions'])} 道題目")
    print(f"單選題：{single_choice_count} 道")
    print(f"多選題：{multiple_choice_count} 道")
    print(f"結果已儲存至：{output_file}")
    
    return quiz_data

def show_examples(quiz_data):
    """顯示單選和多選題的範例"""
    questions = quiz_data["quiz"]["questions"]
    
    # 找一個單選題範例
    single_choice_example = next((q for q in questions if q["type"] == "single_choice"), None)
    if single_choice_example:
        print(f"\n=== 單選題範例（題目 {single_choice_example['id']}）===")
        print(f"題目：{single_choice_example['question']}")
        print("選項：")
        for i, option in enumerate(single_choice_example['options'], 1):
            marker = " ✓" if option == single_choice_example['correct_answer'] else ""
            print(f"  {i}. {option}{marker}")
    
    # 找一個多選題範例
    multiple_choice_example = next((q for q in questions if q["type"] == "multiple_choice"), None)
    if multiple_choice_example:
        print(f"\n=== 多選題範例（題目 {multiple_choice_example['id']}）===")
        print(f"題目：{multiple_choice_example['question']}")
        print("選項：")
        for i, option in enumerate(multiple_choice_example['options'], 1):
            marker = " ✓" if option in multiple_choice_example['correct_answers'] else ""
            print(f"  {i}. {option}{marker}")
        print(f"正確答案數量：{len(multiple_choice_example['correct_answers'])}")

# 主程式
if __name__ == "__main__":
    input_file = "test02.json"  # 原始檔案
    output_file = "quiz_complete02.json"  # 輸出檔案
    
    try:
        result = parse_quiz_data_with_multiple_choice(input_file, output_file)
        show_examples(result)
            
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 '{input_file}'")
    except Exception as e:
        print(f"錯誤：{e}")
        import traceback
        traceback.print_exc()

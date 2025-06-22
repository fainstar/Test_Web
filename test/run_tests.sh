#!/bin/bash

echo "🚀 線上測驗系統 - 測試執行器 (Linux/Mac)"
echo "======================================"

# 切換到腳本所在目錄
cd "$(dirname "$0")"

echo ""
echo "📋 執行測試清單:"
echo "  1. 多選題檢查"
echo "  2. 系統全面檢查"
echo ""

python3 run_all_tests.py

echo ""
echo "📝 測試完成"

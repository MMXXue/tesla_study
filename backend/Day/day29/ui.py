
# 编写前端面板
# 即便后端逻辑很复杂，通过 SDK 和这个 UI，前端人员只需要输入 VIN 码就能得到答案

import streamlit as st
import sys
import os

# --- 1. 依然是那个好用的路径黑魔法 ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sdk_path = os.path.join(current_dir, "tesla-ts-79-diagnostic-api-client")
if sdk_path not in sys.path:
    sys.path.insert(0, sdk_path)

from tesla_ts_79_diagnostic_api_client import Client
from tesla_ts_79_diagnostic_api_client.models import DiagnosticTask
from tesla_ts_79_diagnostic_api_client.api.diagnosis import analyze_vehicle_v1_analyze_post as api_module

# --- 2. 网页界面设计 ---
st.set_page_config(page_title="Tesla AI 诊断系统", page_icon="⚡")

st.title("⚡ Tesla 车辆 AI 智能诊断面板")
st.markdown("---")

# 左侧输入区域
with st.sidebar:
    st.header("输入车辆信息")
    vin = st.text_input("车辆 VIN 码", value="5YJ3E1EB123456789")
    fault_code = st.text_input("故障代码", value="BMS_a066")
    api_url = st.text_input("后端接口地址", value="http://127.0.0.1:8000")

# 右侧展示区域
st.subheader("诊断报告")

if st.button("开始 AI 诊断"):
    if not vin or not fault_code:
        st.warning("请输入完整的 VIN 码和故障代码")
    else:
        with st.spinner('正在通过 SDK 调用后端 AI...'):
            try:
                # 3. 使用 SDK 发送请求
                client = Client(base_url=api_url)
                task = DiagnosticTask(vin=vin, fault_code=fault_code)
                
                # 把 json_body 改成 body 试试
                response = api_module.sync(client=client, body=task)
                
                if response:
                    # 4. 漂亮地展示结果
                    st.success("诊断完成！")
                    st.balloons() # 庆祝一下成功调用
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("检测状态", "已完成")
                    with col2:
                        # 假设 SDK 模型里有 is_critical 这个字段
                        is_crit = getattr(response, 'is_critical', False)
                        st.error("危险程度：高") if is_crit else st.info("危险程度：正常")
                    
                    st.write("### 🤖 AI 建议内容：")
                    st.info(getattr(response, 'suggestion', '未返回建议'))
                    
            except Exception as e:
                st.error(f"调用失败！错误详情: {e}")
                st.info("💡 请确保后端 main.py 正在运行")

st.markdown("---")
st.caption("Tesla Full-stack AI Engineer 365 Days Challenge - Day 29")
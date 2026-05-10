import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

# =========================
# API KEY（⚠️换成你的）
# =========================
API_KEY = "ark-b6a4c4f0-e33a-4e76-bfdf-c08b4f77e6e9-c85a3"


# =========================
# 调用大模型（彻底修复版）
# =========================
def call_llm(prompt):
    # 建议换成这个更快的接口
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 结构标准化
    data = {
        "model": "doubao-seed-2-0-pro-260215", 
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # 增加超时时间到 60 秒
        response = requests.post(url, headers=headers, json=data, timeout=60)
        res_json = response.json()
        
        # 适配标准的 Chat Completions 解析逻辑
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        elif "output" in res_json: # 兼容你目前的接口结构
            return res_json["output"][-1]["content"][0]["text"]
        else:
            return f"解析失败，原始返回：{res_json}"

    except requests.exceptions.Timeout:
        return "⚠️ 服务器响应超时，请尝试缩短问题或增加系统超时时间。"
    except Exception as e:
        return f"❌ 出错啦：{str(e)}"# =========================
# 页面配置
# =========================
st.set_page_config(page_title="电力系统智能分析助手", layout="wide")

st.title("⚡ 电力系统智能分析助手")
st.write("云端大模型 + 电力计算 + 电网调度分析")

menu = st.sidebar.selectbox(
    "选择功能",
    ["电力知识问答", "三相功率计算", "负荷曲线分析"]
)

# =========================
# 1 电力知识问答
# =========================
if menu == "电力知识问答":

    st.header("📚 电力知识智能问答")

    query = st.text_input("请输入电力问题：")

    if query:

        prompt = f"""
你是一名电力系统工程师，请用专业术语回答问题：

问题：{query}

要求：
1. 使用电力专业术语
2. 表达清晰
3. 必要时给出原理说明
"""

        with st.spinner("AI正在分析中..."):
            response = call_llm(prompt)

        st.success("回答完成")
        st.write(response)


# =========================
# 2 三相功率计算（电气强化版）
# =========================
elif menu == "三相功率计算":

    st.header("⚡ 三相功率计算与分析")

    col1, col2 = st.columns(2)

    with col1:
        U = st.number_input("线电压 U (V)", value=380.0)
        I = st.number_input("电流 I (A)", value=10.0)

    with col2:
        cosphi = st.slider("功率因数 cosφ", 0.0, 1.0, 0.85)

    if st.button("计算"):

        P = np.sqrt(3) * U * I * cosphi
        S = np.sqrt(3) * U * I
        Q = np.sqrt(S**2 - P**2)

        st.subheader("📊 计算结果")

        st.metric("有功功率 P", f"{P:.2f} W")
        st.metric("无功功率 Q", f"{Q:.2f} Var")
        st.metric("视在功率 S", f"{S:.2f} VA")

        # 功率三角形
        fig, ax = plt.subplots()
        ax.plot([0, P], [0, 0])
        ax.plot([P, P], [0, Q])
        ax.plot([0, P], [0, Q])

        ax.set_title("功率三角形")
        ax.set_xlabel("P")
        ax.set_ylabel("Q")

        st.pyplot(fig)

        # AI分析（重点）
        prompt = f"""
已知三相系统参数：

电压={U}V
电流={I}A
功率因数={cosphi}

请分析：
1. 系统运行状态
2. 功率因数水平是否合理
3. 是否需要无功补偿
"""

        st.subheader("🤖 AI运行分析")

        with st.spinner("AI分析中..."):
            ai = call_llm(prompt)

        st.write(ai)


# =========================
# 3 负荷曲线分析（核心电气模块）
# =========================
elif menu == "负荷曲线分析":

    st.header("📈 电网负荷曲线分析")

    load_data = st.text_area(
        "输入24小时负荷（逗号分隔）",
        "300,320,350,370,400,420,450,480,500,520,540,560,580,600,620,640,660,680,700,720,700,650,600,500"
    )

    if st.button("分析负荷"):

        try:
            loads = [float(x) for x in load_data.split(",")]
        except:
            st.error("❌ 输入格式错误")
            st.stop()

        hours = list(range(1, len(loads)+1))

        fig, ax = plt.subplots()
        ax.plot(hours, loads, marker='o')

        ax.set_title("24小时负荷曲线")
        ax.set_xlabel("时间 (小时)")
        ax.set_ylabel("负荷 (MW)")

        st.pyplot(fig)

        # ===== 电力指标 =====
        max_load = max(loads)
        min_load = min(loads)
        avg_load = sum(loads) / len(loads)

        load_factor = avg_load / max_load
        peak_valley = max_load - min_load

        st.subheader("📊 电网运行特性")

        st.write(f"最大负荷: {max_load:.2f} MW")
        st.write(f"最小负荷: {min_load:.2f} MW")
        st.write(f"平均负荷: {avg_load:.2f} MW")
        st.write(f"负荷率: {load_factor:.2f}")
        st.write(f"峰谷差: {peak_valley:.2f} MW")

        peak_hour = loads.index(max_load) + 1
        valley_hour = loads.index(min_load) + 1

        st.write(f"峰值时间: 第 {peak_hour} 小时")
        st.write(f"谷值时间: 第 {valley_hour} 小时")

        # ===== AI调度分析（毕设亮点）=====
        prompt = f"""
以下为某电网负荷数据（单位MW）：

{loads}

请从电力系统角度分析：
1. 负荷变化规律
2. 峰谷特性
3. 调度优化建议
"""

        st.subheader("🤖 电网调度分析")

        with st.spinner("AI分析中..."):
            ai_analysis = call_llm(prompt)

        st.write(ai_analysis)
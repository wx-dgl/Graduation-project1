import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.prompts import PromptTemplate

st.title("⚡ 电力系统智能分析助手")
st.write("RAG + 本地大模型 + 电力计算")

# 左侧功能选择
menu = st.sidebar.selectbox(
    "选择功能",
    ["电力知识问答", "三相功率计算", "负荷曲线分析"]
)

# =========================
# 1 电力知识问答
# =========================

if menu == "电力知识问答":

    st.header("📚 电力知识智能问答")

    embedding = OllamaEmbeddings(model="nomic-embed-text")

    vectordb = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = OllamaLLM(model="llama3")

    template = """
请根据以下电力系统资料回答问题。

如果答案不在资料中，请回答：未在知识库中找到。

{context}

问题: {question}
"""

    prompt = PromptTemplate.from_template(template)

    query = st.text_input("请输入电力问题：")

    if query:

        docs = retriever.invoke(query)

        context = "\n".join([doc.page_content for doc in docs])

        formatted_prompt = prompt.format(
            context=context,
            question=query
        )

        response = llm.invoke(formatted_prompt)

        st.subheader("📌 回答")
        st.write(response)

        st.subheader("📄 引用来源")

        for i, doc in enumerate(docs):
            page = doc.metadata.get("page", "未知页")
            st.write(f"来源{i+1} - 第{page+1}页")

# =========================
# 2 三相功率计算
# =========================

# =========================
# 3 负荷曲线分析
# =========================

elif menu == "负荷曲线分析":

    st.header("📈 电网负荷曲线分析")

    load_data = st.text_area(
        "输入24小时负荷（逗号分隔）",
        "300,320,350,370,400,420,450,480,500,520,540,560,580,600,620,640,660,680,700,720,700,650,600,500"
    )

    if st.button("生成负荷曲线"):

        loads = [float(x) for x in load_data.split(",")]

        hours = list(range(1, len(loads)+1))

        fig, ax = plt.subplots()

        ax.plot(hours, loads, marker='o')

        ax.set_xlabel("时间 (小时)")
        ax.set_ylabel("负荷 (MW)")
        ax.set_title("24小时负荷曲线")

        st.pyplot(fig)

        # =========================
        # 电力系统负荷分析
        # =========================

        max_load = max(loads)
        min_load = min(loads)
        avg_load = sum(loads) / len(loads)

        load_factor = avg_load / max_load
        peak_valley = max_load - min_load

        st.subheader("📊 电网负荷特性分析")

        st.write(f"最大负荷: {max_load:.2f} MW")
        st.write(f"最小负荷: {min_load:.2f} MW")
        st.write(f"平均负荷: {avg_load:.2f} MW")
        st.write(f"负荷率: {load_factor:.2f}")
        st.write(f"峰谷差: {peak_valley:.2f} MW")

        # =========================
        # 峰值时间
        # =========================

        peak_hour = loads.index(max_load) + 1
        valley_hour = loads.index(min_load) + 1

        st.write(f"峰值出现时间: 第 {peak_hour} 小时")
        st.write(f"谷值出现时间: 第 {valley_hour} 小时")

        # =========================
        # AI电网分析
        # =========================

        llm = OllamaLLM(model="llama3")

        analysis_prompt = f"""
以下是某电网24小时负荷数据（单位MW）：

{loads}

请从电力系统角度分析：

1. 负荷变化特点
2. 峰值负荷出现时间
3. 是否存在明显峰谷差
4. 对电网调度提出建议
"""

        ai_analysis = llm.invoke(analysis_prompt)

        st.subheader("🤖 AI电网调度分析")

        st.write(ai_analysis)
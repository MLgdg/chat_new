import gradio as gr
import openai

# 设置 OpenAI API 密钥
openai.api_key = "你的 OpenAI API 密钥"

# 定义聊天函数
def chat_with_gpt(message, history, selected_role, selected_personality, selected_gender, selected_hobby, history_dict):
    history = history or []

    # 角色描述
    role_descriptions = {
        "猫": "你是一个猫，你非常喜欢安静，喜欢午睡，并且在别人靠近时可能会发出咕噜声。",
        "狗": "你是一个狗，喜欢互动和玩耍，经常在主人身边蹭来蹭去。",
        "鱼": "你是一个鱼，喜欢水中的寂静，偶尔会游来游去，观察水草。",
        "龟": "你是一个龟，动作缓慢，喜欢在阳光下晒太阳，沉静而悠闲。"
    }

    # 性格描述
    personality_descriptions = {
        "暴力": "你非常激动，容易愤怒，喜欢争斗。",
        "温柔": "你很温柔，关心别人，喜欢和别人友好相处。",
        "高冷": "你显得很冷漠，不容易和别人亲近。",
        "冷漠": "你对别人没有太多兴趣，保持距离。",
        "粘人": "你非常依赖别人，总是想要得到别人陪伴。"
    }

    # 性别描述
    gender_descriptions = {
        "男": "你是男性。",
        "女": "你是女性。",
        "其他": "你是非二元性别。"
    }

    # 爱好描述
    hobby_descriptions = {
        "吃饭": "你特别喜欢吃各种美味的食物。",
        "睡觉": "你非常喜欢睡觉，享受安静的休息时间。",
        "玩": "你喜欢玩耍和互动，尤其喜欢和人一起玩。"
    }

    # 组合系统消息
    system_message = (f"你是一个{role_descriptions.get(selected_role, '宠物')}，"
                      f"性格是{personality_descriptions.get(selected_personality, '正常')}，"
                      f"性别是{gender_descriptions.get(selected_gender, '不明确')}，"
                      f"你最喜欢{hobby_descriptions.get(selected_hobby, '做事情')}。"
                      "你将以此角色和特征回答问题。")
    
    # 获取或创建该角色的聊天历史
    if selected_role not in history_dict:
        history_dict[selected_role] = []
    
    messages = [{"role": "system", "content": system_message}]
    for user_msg, bot_msg in history_dict[selected_role]:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    messages.append({"role": "user", "content": message})

    # 调用 OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    bot_message = response['choices'][0]['message']['content']
    
    # 将新的消息添加到该角色的历史中
    history_dict[selected_role].append((message, bot_message))

    return history_dict[selected_role], history_dict

# 查看聊天记录
def view_chat_history(selected_role, history_dict):
    # 返回该角色的聊天记录
    if selected_role in history_dict:
        return "\n".join([f"用户: {user_msg}\n机器人: {bot_msg}" for user_msg, bot_msg in history_dict[selected_role]])
    return "该角色没有聊天记录。"

# 创建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 自定义角色聊天机器人（猫、狗、鱼、龟）")

    # 使用 Row 横向排列所有选择框
    with gr.Row():
        role_select = gr.Dropdown(
            choices=["猫", "狗", "鱼", "龟"], 
            label="选择一个角色", 
            value="猫",  # 默认选择猫
            elem_id="role_select"
        )
        personality_select = gr.Dropdown(
            choices=["暴力", "温柔", "高冷", "冷漠", "粘人"],
            label="选择角色性格",
            value="温柔",  # 默认选择温柔
            elem_id="personality_select"
        )
        gender_select = gr.Dropdown(
            choices=["男", "女", "其他"],
            label="选择性别",
            value="女",  # 默认选择女
            elem_id="gender_select"
        )
        hobby_select = gr.Dropdown(
            choices=["吃饭", "睡觉", "玩"],
            label="选择爱好",
            value="玩",  # 默认选择玩
            elem_id="hobby_select"
        )

    # 聊天组件
    with gr.Row():
        chatbot = gr.Chatbot(label="聊天窗口", elem_id="chatbot")
    with gr.Row():
        user_input = gr.Textbox(placeholder="请输入消息...", label="你的消息", elem_id="user_input")
    with gr.Row():
        send_btn = gr.Button("发送消息", elem_id="send_btn")  # 发送按钮
        clear_btn = gr.Button("清空对话", elem_id="clear_btn")
        view_history_btn = gr.Button("查看聊天记录", elem_id="view_history_btn")
        chat_history = gr.Textbox(label="聊天记录", interactive=False, elem_id="chat_history")

    # 新增历史角色选择框
    with gr.Row():
        history_role_select = gr.Dropdown(
            label="选择历史角色", 
            choices=["猫", "狗", "鱼", "龟"],
            value="猫",  # 默认选择猫
            elem_id="history_role_select"
        )

    state = gr.State([])  # 用于保存对话历史
    history_dict = gr.State({})  # 用于保存多个角色的聊天历史

    # 定义交互逻辑
    send_btn.click(chat_with_gpt, 
                   [user_input, state, role_select, personality_select, gender_select, hobby_select, history_dict], 
                   [chatbot, history_dict])

    # 查看聊天记录
    view_history_btn.click(view_chat_history, inputs=[history_role_select, history_dict], outputs=chat_history)

    # 清空对话按钮
    clear_btn.click(lambda: ([], {}), None, [chatbot, history_dict])


# 添加自定义 CSS 修改聊天框背景
demo.css = """
#title {
    font-size: 18px;
    text-align: center;
    margin-bottom: 10px;
}

#chatbot {
    height: 400px;
    max-width: 95%;
    margin: 0 auto;
    background-color: #f0f8ff; /* 设置聊天框背景为浅蓝色 */
    border-radius: 10px; /* 圆角边框 */
    padding: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
    overflow-y: auto; /* 允许滚动 */
}

#chatbot .message.user {
    background-color: #d1e7dd; /* 用户消息背景色 */
    color: #0f5132;
    border-radius: 8px;
    padding: 8px;
    margin: 5px 0;
}

#chatbot .message.bot {
    background-color: #fff3cd; /* 机器人消息背景色 */
    color: #664d03;
    border-radius: 8px;
    padding: 8px;
    margin: 5px 0;
}

#user_input {
    max-width: 95%;
    margin: 0 auto;
}

#clear_btn {
    max-width: 95%;
    margin: 10px auto;
}
"""

# 启动应用
demo.launch(server_name="0.0.0.0", server_port=8080)

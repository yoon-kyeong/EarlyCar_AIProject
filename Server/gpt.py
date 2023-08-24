!pip install openai
!pip install python-dotenv
openai.Model.list()

openai.api_key = '?'

def chat(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens=2048
    )
    return completions.choices[0].text.strip()

chat("한국말 할 수 있어?")
chat("빨간불일 때 비보호 좌회전 해도 되나요?")

completion = openai.Completion.create(
    model = "text-davinci-003",
    prompt = "비보호 좌회전이 가능한 교차로에서 파란불에 대기중이야. 좌회전 해도 돼?",
    max_tokens = 200,
    temperature = 0
)
print(completion['choices'][0]['text'])

completion = openai.Completion.create(
    model = 'davinci:ft-personal-2023-07-02-15-52-59',
    prompt = "비보호 좌회전이 가능한 교차로에서 파란불에 대기중이야. 건너편에서 차가 오고 있는데 좌회전 해도 돼?",
    max_tokens = 30,
    temperature = 0
)
print(completion['choices'][0]['text'])

# fine-tuning 모델
completion = openai.Completion.create(
    model = 'davinci:ft-personal-2023-07-02-15-52-59',
    prompt = "비보호 좌회전이 가능한 교차로에서 파란불에 대기중이야. 좌회전 해도 돼?",
    max_tokens = 200,
    temperature = 0
)
print(completion['choices'][0]['text'])

completion = openai.Completion.create(
    model = 'davinci:ft-personal-2023-07-02-15-52-59',
    prompt = "비보호 좌회전이 가능한 교차로에서 파란불에 대기중이야. 건너편에서 차가 오고 있는데 좌회전 해도 돼?",
    max_tokens = 150,
    temperature = 0
)
print(completion['choices'][0]['text'])
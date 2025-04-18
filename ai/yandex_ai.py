from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk.search_indexes import TextSearchIndexType
import os, random

load_dotenv()

sdk = YCloudML(
    folder_id=os.getenv("YANDEX_FOLDER_ID"),
    auth=os.getenv("YANDEX_API_KEY"),
)

class Analyzer:
    def __init__(self, system_prompt:str=None, path:str=None, base=True, memory=None):
        if system_prompt and path:
            raise "Должен быть указан только один из параметров: text или path"
        self.path = path
        self.system_prompt = system_prompt
        self.base = base
        self.memory = [] if memory else memory
        if not base:
            self.name = "temp/" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10)) + '.txt'
            open(self.name, 'w', encoding='UTF-8').write(system_prompt)

            file = sdk.files.upload(self.name)
            operation = sdk.search_indexes.create_deferred([file], index_type=TextSearchIndexType())
            text_index = operation.wait()
            text_tool = sdk.tools.search_index(text_index)
            model = sdk.models.completions("yandexgpt-lite", model_version="rc")
            assistant = sdk.assistants.create(model, tools=[text_tool])

            self.id_model = assistant.id

    def question(self, query:str):
        """Вопрос к созданной модели, возвращает ответ"""
        if self.base:
            return self.question_base(query)
        return self.question_prepared_text(query)

    def question_prepared_text(self, query):
        assistant = sdk.assistants.get(self.id_model)
        text_index_thread = sdk.threads.create()
        text_index_thread.write(query)
        run = assistant.run(text_index_thread)

        answer = ""
        result = run.wait().message
        for part in result.parts:
            answer += part + " "
        return answer
    
    def question_base(self, query):
        model = sdk.models.completions('yandexgpt', model_version='rc')
        model.configure(temperature=0.5)

        if self.memory is not None:
            if self.memory:
                self.memory.append({'role': 'user', 'text': query})
            else:
                self.memory = [
                {'role': 'system', 'text': self.system_prompt},
                {'role': 'user', 'text': query},
            ]
            operation = model.run_deferred(self.memory)
        else:
            messages = [
                {'role': 'system', 'text': self.system_prompt},
                {'role': 'user', 'text': query},
            ]
            operation = model.run_deferred(messages)
        result = operation.wait()
        if self.memory is not None:
            self.memory.append({'role': 'assistant', 'text': result.text})
        return result.text
    
# ai = Analyzer("Ты — помощник по выбору вуза. Предоставь структурированную информацию в формате:Название вуза | Специальность | Проходной балл (мин./ср./макс.) | Бюджетные места | Город | Особенности (например, аккредитация, рейтинг, наличие общежития). Не отвечай ничего лишнего.",memory=True)
# print(ai.question("Я даун, который планирую сдать егэ на 200 баллов, люблю физру и живу в Казани"))

class Psychologist(Analyzer):
    def __init__(self):
        super().__init__(system_prompt="Ты  -- психолог для поступающего в вуз. Помоги мне и окажи сеанс психотерапии.", memory=True)
    def user_ask(self, prompt):
        x = self.question(prompt)
        return x
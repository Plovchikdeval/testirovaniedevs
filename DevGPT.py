__version__ = (8, 0, 0)
# change-log: ADD NEW MODELS! MORE DETAILS IN .dgmodels

"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P" 
                                                           
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @kshmods
# meta banner: https://kappa.lol/nfF_A
# requires: requests

import logging
import io
import os
import inspect
import aiohttp
import json
import requests

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class DevGPT(loader.Module):
	"""DevGPT - позволяет вам общаться с chatgpt и генерировать фото."""

	strings = {
		"name": "DevGPT",
		"wait": "<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>The server is processing the request, please wait...</b></blockquote>",
		"update_whats_new": "\n\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Change-log:</b><code>{whats_new}</code>\n\n</blockquote>",
		"quest": "\n\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Your request:</b> {args}</blockquote>",
		"quest_img": "<blockquote><b><emoji document_id=5877465816030515018>😀</emoji> Link: <a href='{img_url}'>image</a></b></blockquote>\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Prompt:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Model:</b> <code>{mdl}</code></blockquote>",
		"args_err": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Usage: {prefix}dgpt/dimg <model> <request></b></blockquote>",
		"query_err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>The request cannot be empty!</b></blockquote>",
		"server_err": "<blockquote><emoji document_id=5881702736843511327>⚠️</emoji> <b>Server error: {error}</b></blockquote>",
		"image_err": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Error generating image: {error}</b>",
		"models_list": "<blockquote><emoji document_id=5879841310902324730>😀</emoji><b>Text</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote><emoji document_id=5775949822993371030>🖼</emoji> <b>Images</b></blockquote>\n\n<blockquote>{img_models}</blockquote>\n\n<blockquote><emoji document_id=5343545593807521643>❤️‍🔥</emoji><emoji document_id=5220081566268536865>😮</emoji><b>New text models: </b></blockquote>\n\n<blockquote>{neeew_model}</blockquote>",
		"model_not_found": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Model not found! List of available models: {prefix}dgmodels</b></blockquote>",
		"no_url": "No image URL received",
		"no_server_respond": "No response from the server",
		"fetch_failed": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> <b>Fetching data failed</b></blockquote>",
		"actual_version": "<blockquote> <emoji document_id=5208763618773978162>✅</emoji>You have actual DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote><emoji document_id=5875291072225087249>📊</emoji> You have old DevGPT ({ver}) </b></blockquote>\n\n<blockquote><emoji document_id=5879883461711367869>⬇️</emoji> <b>New version: {new_ver} <b></blockquote>",
		"update_command": "\n\n<blockquote><emoji document_id=5877410604225924969>🔄</emoji> To update type:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",
		"ban": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> You are banned! Reason: {reason}</blockquote>",
	}

	strings_ua = {
		"wait": "<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Сервер обробляє запит, будь ласка, зачекайте...</b></blockquote>",
		"quest": "\n\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Ваш запит:</b> {args}</blockquote>",
		"update_whats_new": "\n\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Список изменений:</b><code>{whats_new}</code>\n\n</blockquote>",
		"quest_img": "<blockquote><b><emoji document_id=5877465816030515018>😀</emoji> Посилання: <a href='{img_url}'>зображення</a></b></blockquote>\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Запит:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Модель:</b> <code>{mdl}</code></blockquote>",
		"args_err": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Використання {prefix}dgpt/dimg <модель> <запит></b></blockquote>",
		"query_err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Запит не може бути порожнім!</b></blockquote>",
		"server_err": "<blockquote><emoji document_id=5881702736843511327>⚠️</emoji> <b>Помилка сервера: {error}</b></blockquote>",
		"image_err": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Помилка при генерації зображення: {error}</b>",
		"models_list": "<blockquote><emoji document_id=5879841310902324730>😀</emoji><b>Текст</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote><emoji document_id=5775949822993371030>🖼</emoji> <b>Зображення</b></blockquote>\n\n<blockquote>{img_models}</blockquote>\n\n<blockquote><emoji document_id=5343545593807521643>❤️‍🔥</emoji><emoji document_id=5220081566268536865>😮</emoji><b>Нові текстові моделі: </b></blockquote>\n\n<blockquote>{neeew_model}</blockquote>",
		"model_not_found": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Модель не знайдена! Список доступних моделей {prefix}dgmodels</b></blockquote>",
		"no_url": "Не отримано URL зображення",
		"no_server_respond": "Немає відповіді від сервера",
		"fetch_failed": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> <b>Не вдалося отримати дані</b></blockquote>",
		"actual_version": "<blockquote> <emoji document_id=5208763618773978162>✅</emoji>У вас актуальна версія DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote><emoji document_id=5875291072225087249>📊</emoji> У вас застаріла версія DevGPT ({ver}) </b></blockquote>\n\n<blockquote><emoji document_id=5879883461711367869>⬇️</emoji> <b>Нова версія: {new_ver} <b></blockquote>",
		"update_command": "\n\n<blockquote><emoji document_id=5877410604225924969>🔄</emoji> Для оновлення введіть:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",
		"ban": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> Вас забанено! З причини: {reason}</blockquote>",
	}

	strings_ru = {
		"wait": "<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Сервер обрабатывает запрос, подождите...</b></blockquote>",
		"quest": "\n\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Ваш запрос:</b> {args}</blockquote>",
		"update_whats_new": "\n\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Список изменений:</b><code>{whats_new}</code>\n\n</blockquote>",
		"quest_img": "<blockquote><b><emoji document_id=5877465816030515018>😀</emoji> Ссылка: <a href='{img_url}'>изображение</a></b></blockquote>\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Запрос:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Модель:</b> <code>{mdl}</code></blockquote>",
		"args_err": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Использование {prefix}dgpt/dimg <модель> <запрос></b></blockquote>",
		"query_err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Запрос не может быть пустым!</b></blockquote>",
		"server_err": "<blockquote><emoji document_id=5881702736843511327>⚠️</emoji> <b>Ошибка сервера: {error}</b></blockquote>",
		"image_err": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Ошибка при генерации изображения: {error}</b>",
		"models_list": "<blockquote><emoji document_id=5879841310902324730>😀</emoji><b>Текст</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote><emoji document_id=5775949822993371030>🖼</emoji> <b>Изображения</b></blockquote>\n\n<blockquote>{img_models}</blockquote>\n\n<blockquote><emoji document_id=5343545593807521643>❤️‍🔥</emoji><emoji document_id=5220081566268536865>😮</emoji><b>Новые текстовые модели: </b></blockquote>\n\n<blockquote>{neeew_model}</blockquote>",
		"model_not_found": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Модель не найдена! Список доступных моделей {prefix}dgmodels</b></blockquote>",
		"no_url": "Не получен URL изображения",
		"no_server_respond": "Нет ответа от сервера",
		"fetch_failed": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> <b>Не удалось получить данные</b></blockquote>",
		"actual_version": "<blockquote> <emoji document_id=5208763618773978162>✅</emoji>У вас актуальная версия DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote><emoji document_id=5875291072225087249>📊</emoji> У вас устаревшая версия DevGPT ({ver}) </b></blockquote>\n\n<blockquote><emoji document_id=5879883461711367869>⬇️</emoji> <b>Новая версия: {new_ver} <b></blockquote>",
		"update_command": "\n\n<blockquote><emoji document_id=5877410604225924969>🔄</emoji> Для обновления введите:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",
		"ban": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> Вы забанены! По причине: {reason}</blockquote>",
	}

	async def client_ready(self, client, _):
		# self.server_url = "https://api.vysssotsky.ru"
		self.server_url = "https://api.vysssotsky.ru/"
		self.server_url_images = "https://v1.vysssotsky.ru/v1/{model_name}/generate"
		self.server_url_images_v2 = "https://v2.vysssotsky.ru/v1/generate"
		self.additional_server_url = "http://146.19.48.160:25701/generate_image"
		self.server_url_v2 = "http://77.223.103.8:9999/api/generate"
		self.deep_url = "https://openrouter.ai/api/v1/chat/completions"

		self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

		self.repo = "https://raw.githubusercontent.com/Plovchikdeval/dev_modules/main/"

		self._client = client
		self.prefix = self._client.loader.get_prefix()

		self.text_models = ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "o1-preview", "hermes-2-pro", "phi-2", "gemini-pro", "gemini-flash", "gemma-2b", "claude-3-haiku", "claude-3.5-sonnet", "blackboxai", "llava-13b", "openchat-3.5", "sonar-chat", "german-7b", "any-uncensored"]
		self.text_models_2 = ["gemma2", "mistral", "dolphin-phi", "openchat", "phi4", "llama3.2", "deepseek-coder-v2"]
		self.image_models = ["sd-3", "flux-pro", "flux-realism", "flux-anime", "flux-disney", "flux-pixel", "flux-4o", "any-dark", "flux"]
		self.additional_image_models = ["anything-v5", "dreamshaper-v6", "dreamshaper-v5", "meina-v9"]
		self.deepseek = ["deepseek-r1"]

	async def generate_text(self, message, args):
		model = args.split()[0]
		content = args.replace(model, "").strip()

		if len(content) <= 1:
			await utils.answer(message, self.strings("query_err"))
			return

		if model in self.text_models:
			try:
				payload = {
					"model": model,
					"messages": [{"role": "user", "content": content}],
					"max_tokens": 2048,
					"temperature": 0.7,
					"top_p": 1,
				}

				async with aiohttp.ClientSession() as session:
					async with session.post(f"{self.server_url}/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, json=payload) as response:
						response.raise_for_status()

						if response.status == 200:
							data = await response.json()
							answer = data.get("choices", [{}])[0].get("message", {}).get("content", self.strings("no_server_respond"))
							answer = f"<blockquote>{answer}</blockquote>"

							await utils.answer(message, answer + self.strings("quest").format(args=content))
						else:
							await utils.answer(message, self.strings("server_err").format(error=f"HTTP {response.status}"))
			except Exception as e:
				await utils.answer(message, self.strings("server_err").format(error=str(e)))

		elif model in self.text_models_2:
			try:
				data = {
					"model": model,
					"prompt": content,
					"stream": False
				}
				headers = {"Content-Type": "application/json"}

				async with aiohttp.ClientSession() as session:
					async with session.post(self.server_url_v2, headers=headers, json=data) as response:
						response.raise_for_status()

						if response.status == 200:
							data = await response.json()
							answer = data.get("response", self.strings("no_server_respond"))
							answer = f"<blockquote>{answer}</blockquote>"

							await utils.answer(message, answer + self.strings("quest").format(args=content))
						else:
							await utils.answer(message, self.strings("server_err").format(error=f"HTTP {response.status_code}"))
			except Exception as e:
				await utils.answer(message, self.strings("server_err").format(error=str(e)))
			
		elif model in self.deepseek:
			try:
				data = {
					"model": "deepseek-r1:8b",
					"prompt": content,
					"stream": False
				}
				headers = {"Content-Type": "application/json"}

				async with aiohttp.ClientSession() as session:
					async with session.post(self.server_url_v2, headers=headers, json=data) as response:
						response.raise_for_status()

						if response.status == 200:
							data = await response.json()
							answer = data.get("response", self.strings("no_server_respond"))
							answer = f"<blockquote>{answer}</blockquote>"

							await utils.answer(message, answer + self.strings("quest").format(args=content))
						else:
							await utils.answer(message, self.strings("server_err").format(error=f"HTTP {response.status_code}"))
			except Exception as e:
				await utils.answer(message, self.strings("server_err").format(error=str(e)))
		else:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))

	async def generate_image(self, message, args):
		model = args.split()[0]
		prompt = args.replace(model, "").strip()

		if len(prompt) <= 1:
			await utils.answer(message, self.strings("query_err"))
			return

		if model in self.image_models:
			try:
				payload = {
					"prompt": prompt
				}

				async with aiohttp.ClientSession() as session:
					async with session.post(self.server_url_images.format(model_name=model), headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, data=json.dumps(payload)) as response:
						if response.status == 200:
							data = await response.json()
							image_url = data.get("data", [{}])[0].get("url", None)

							if image_url:
								try:
									async with session.get(image_url) as generated_image:
										file_name = "dgimage.png"
										with open(file_name,'wb') as file:
											file.write(await generated_image.read())

									await utils.answer_file(message, file_name, caption=(self.strings('quest_img').format(img_url=image_url, prmpt=prompt, mdl=model)))
								finally:
									if os.path.exists(file_name):
										os.remove(file_name)
							else:
								await utils.answer(message, self.strings("image_err").format(error=self.strings("no_url")))
						elif model not in ["sd-3", "any-dark"]:
							logger.warning("v1 API down! Trying to use v2 instead", exc_info=True)
							payload_v2 = {
								"model": model,
								"prompt": prompt
							}
							async with session.post(self.server_url_images_v2, headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}, data=json.dumps(payload_v2)) as response_v2:
								if response_v2.status == 200:
									
									image_v2 = await response_v2.text()

									try:
										image_v2 = json.loads(image_v2)
										image_v2_url = image_v2.get("link")
									except json.JSONDecodeError:
										image_v2_url = image_v2.strip()

									async with session.get(image_v2_url) as image_v2_response:
										image_v2_response.raise_for_status()
										image_v2_content = io.BytesIO(await image_v2_response.read())
									await utils.answer_file(message, image_v2_content, caption=(self.strings('quest_img').format(img_url=image_v2_url, prmpt=prompt, mdl=model)))
								else:
									err_data = await response_v2.json()
									ban_reason = err_data.get("reason")
									await utils.answer(message, self.strings("ban").format(reason=ban_reason))
						elif response.status == 403:
							err_data = await response.json()
							ban_reason = err_data.get("reason")
							await utils.answer(message, self.strings("ban").format(reason=ban_reason))
						else:
							await utils.answer(message, self.strings("image_err").format(error=f"HTTP {response.status}"))

			except Exception as e:
				await utils.answer(message, self.strings("image_err").format(error=str(e)))
		elif model in self.additional_image_models:
			try:
				data = {
				"prompt": prompt,
				"model": model
				}
				headers = {"Content-Type": "application/json"}
				response = requests.post(self.additional_server_url, json=data, headers=headers)
				response.raise_for_status()
				result = response.json()
				image_url = result.get("image_url", "")
				image_response = requests.get(image_url)

				image = io.BytesIO(image_response.content)
				image.name = "generated_image.png"

				await utils.answer(message, image, caption=(self.strings("quest_img").format(img_url=image_url, prmpt=prompt, mdl=model)))
			except requests.exceptions.RequestException as e:
				await utils.answer(message, self.strings("image_err").format(error=e))
			except Exception as e:
				await utils.answer(message, self.strings("image_err").format(error=e))
		else:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))			
			
	@loader.command(en_doc="Ask gpt for something", ru_doc="Спросите gpt о чем-нибудь", ua_doc="Запитайте gpt про щось")
	async def dgpt(self, message: Message):
		"""Ask gpt for something"""
		args = utils.get_args_raw(message)
		if not args:
			await utils.answer(message, self.strings("args_err").format(prefix=self.prefix))
			return

		await utils.answer(message, self.strings("wait"))

		await self.generate_text(message, args)

	@loader.command(en_doc="Generate image", ru_doc="Сгенерировать изображение", ua_doc="Згенерувати зображення")
	async def dimg(self, message: Message):
		"""Generate image"""
		args = utils.get_args_raw(message)
		if not args:
			await utils.answer(message, self.strings("args_err").format(prefix=self.prefix))
			return

		await utils.answer(message, self.strings("wait"))

		await self.generate_image(message, args)

	@loader.command(en_doc="Display models list", ru_doc="Показать список моделей", ua_doc="Показати список моделей")
	async def dgmodels(self, message: Message):
		"""Display models list"""
		combined_list = self.image_models + self.additional_image_models
		devsss = self.text_models_2 + self.deepseek
		t_mdl = '\n'.join(self.text_models)
		i_mdl = '\n'.join(combined_list)
		dev = "\n".join(devsss)
		await utils.answer(message, self.strings("models_list").format(txt_models=t_mdl, img_models=i_mdl, neeew_model=dev))

	@loader.command(en_doc="Check for updates", ru_doc="Проверить обновления", ua_doc="Перевірити оновлення")
	async def dgcheck(self, message: Message):
		"""Check for updates"""
		module_name = self.strings("name")
		module = self.lookup(module_name)
		sys_module = inspect.getmodule(module)

		local_file = io.BytesIO(sys_module.__loader__.data)
		local_file.name = f"{module_name}.py"
		local_file.seek(0)
		local_first_line = local_file.readline().strip().decode("utf-8")

		correct_version = sys_module.__version__
		correct_version_str = ".".join(map(str, correct_version))

		async with aiohttp.ClientSession() as session:
			async with session.get(f"{self.repo}/{local_file.name}") as response:
				if response.status == 200:
					remote_content = await response.text()
					remote_lines = remote_content.splitlines()
					what_new = remote_lines[1].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[1].startswith("# change-log:") else ""
					new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
				else:
					await utils.answer(message, self.strings("fetch_failed"))
					return

		if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
			await utils.answer(message, self.strings("actual_version").format(ver=correct_version_str))
		else:
			update_message = self.strings("old_version").format(ver=correct_version_str, new_ver=new_version)
			update_message += self.strings("update_command").format(prefix=self.prefix, upd_file=f"{self.repo}/{local_file.name}")
			if what_new:
				update_message += self.strings("update_whats_new").format(whats_new=what_new)
			await utils.answer(message, update_message)

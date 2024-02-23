from flask import Flask, request, send_file
from translator import PDFTranslator
from model import GLMModel, OpenAIModel
from utils import ArgumentParser, ConfigLoader, LOG

app = Flask(__name__)


# 定义 API 路由，使用 POST 方法接收文件和请求参数
@app.route('/translate_pdf', methods=['POST'])
def translate_pdf():
    # 获取语言参数，默认为中文
    target_language = request.form.get('language', '中文')

    # 获取文件格式参数，默认为pdf
    output_format = request.form.get('format', 'pdf')

    # 获取上传的 PDF 文件
    pdf_file = request.files['file']
    print(pdf_file)
    # 保存上传的文件到本地
    uploaded_file_path = 'D:\\github\\openai-translator\\temp\\api_file.pdf'
    pdf_file.save(uploaded_file_path)

    # 翻译后的文件保存路径
    output_file_path = uploaded_file_path.replace('.pdf', f'_translated.pdf')

    # 调用已有翻译接口
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)
    config = config_loader.load_config()
    model_name = config['OpenAIModel']['model']
    api_key = config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(uploaded_file_path, output_format, target_language, output_file_path)
    
    # 返回翻译后文件
    return send_file(output_file_path)


if __name__ == '__main__':
    app.run()
